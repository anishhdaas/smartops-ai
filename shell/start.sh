#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${ROOT_DIR}/logs"
VECTOR_DB_DIR="${ROOT_DIR}/vector_db"
DBT_PROFILES_DIR="${ROOT_DIR}/.dbt"
KAFKA_BOOTSTRAP_SERVERS="${KAFKA_BOOTSTRAP_SERVERS:-localhost:9092}"
KAFKA_TOPIC="${KAFKA_TOPIC:-raw_incidents}"
KAFKA_CONSUMER_GROUP="${KAFKA_CONSUMER_GROUP:-validation_group}"
MCP_HTTP_HOST="${MCP_HTTP_HOST:-0.0.0.0}"
MCP_HTTP_PORT="${MCP_HTTP_PORT:-5000}"

PIDS=()

cd "${ROOT_DIR}"
mkdir -p "${LOG_DIR}" "${VECTOR_DB_DIR}" "${DBT_PROFILES_DIR}"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env"
  set +a
fi

required_vars=(
  OPENROUTER_API_KEY
  SNOWFLAKE_USER
  SNOWFLAKE_PASSWORD
  SNOWFLAKE_ACCOUNT
  SNOWFLAKE_DATABASE
  SNOWFLAKE_WAREHOUSE
  PINECONE_API_KEY
  PINECONE_HOST
  PINECONE_INDEX
)

for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "Missing required environment variable: ${var_name}" >&2
    exit 1
  fi
done

export KAFKA_BOOTSTRAP_SERVERS KAFKA_TOPIC KAFKA_CONSUMER_GROUP
export MCP_HTTP_HOST MCP_HTTP_PORT
export DBT_PROFILES_DIR

cleanup() {
  echo "Stopping SmartOps AI services..."
  for pid in "${PIDS[@]:-}"; do
    if kill -0 "${pid}" >/dev/null 2>&1; then
      kill "${pid}" >/dev/null 2>&1 || true
    fi
  done
  wait "${PIDS[@]:-}" 2>/dev/null || true
}

trap cleanup INT TERM EXIT

wait_for_kafka() {
  echo "Waiting for Kafka at ${KAFKA_BOOTSTRAP_SERVERS}..."
  python - <<'PY'
import os
import sys
import time
from kafka import KafkaAdminClient
from kafka.errors import KafkaError

servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(",")
deadline = time.time() + 120
last_error = None
while time.time() < deadline:
    try:
        client = KafkaAdminClient(bootstrap_servers=servers, request_timeout_ms=5000)
        client.close()
        sys.exit(0)
    except KafkaError as exc:
        last_error = exc
        time.sleep(3)
print(f"Kafka did not become ready: {last_error}", file=sys.stderr)
sys.exit(1)
PY
}

wait_for_snowflake() {
  echo "Waiting for Snowflake..."
  python - <<'PY'
import os
import sys
import time
import snowflake.connector

deadline = time.time() + 120
last_error = None
while time.time() < deadline:
    try:
        conn = snowflake.connector.connect(
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            database=os.environ["SNOWFLAKE_DATABASE"],
            warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
            role=os.getenv("SNOWFLAKE_ROLE") or None,
        )
        conn.cursor().execute("SELECT 1")
        conn.close()
        sys.exit(0)
    except Exception as exc:
        last_error = exc
        time.sleep(5)
print(f"Snowflake did not become ready: {last_error}", file=sys.stderr)
sys.exit(1)
PY
}

create_kafka_topic() {
  echo "Ensuring Kafka topic ${KAFKA_TOPIC} exists..."
  python - <<'PY'
import os
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(",")
topic = os.getenv("KAFKA_TOPIC", "raw_incidents")
client = KafkaAdminClient(bootstrap_servers=servers, client_id="smartops-topic-bootstrap")
try:
    if topic not in client.list_topics():
        client.create_topics([NewTopic(name=topic, num_partitions=3, replication_factor=1)])
except TopicAlreadyExistsError:
    pass
finally:
    client.close()
PY
}

write_dbt_profile() {
  cat > "${DBT_PROFILES_DIR}/profiles.yml" <<EOF
smartops_incidents:
  target: prod
  outputs:
    prod:
      type: snowflake
      account: "${SNOWFLAKE_ACCOUNT}"
      user: "${SNOWFLAKE_USER}"
      password: "${SNOWFLAKE_PASSWORD}"
      role: "${SNOWFLAKE_ROLE:-}"
      database: "${SNOWFLAKE_DATABASE}"
      warehouse: "${SNOWFLAKE_WAREHOUSE}"
      schema: "${SNOWFLAKE_SCHEMA:-ANALYTICS}"
      threads: 4
      client_session_keep_alive: false
EOF
}

start_service() {
  local name="$1"
  shift
  echo "Starting ${name}..."
  ("$@") >"${LOG_DIR}/${name}.log" 2>&1 &
  PIDS+=("$!")
  sleep 2
}

start_producer() {
  echo "Starting producer..."
  (
    python -u producer/log_generator.py 2>>"${LOG_DIR}/producer.err" | python -u -c '
import json
import os
import sys
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(","),
    value_serializer=lambda value: json.dumps(value, separators=(",", ":")).encode("utf-8"),
    linger_ms=50,
    retries=5,
)
topic = os.getenv("KAFKA_TOPIC", "raw_incidents")
for line in sys.stdin:
    line = line.strip()
    if line:
        producer.send(topic, json.loads(line))
producer.flush()
'
  ) >"${LOG_DIR}/producer.log" 2>&1 &
  PIDS+=("$!")
  sleep 2
}

wait_for_kafka
wait_for_snowflake
create_kafka_topic
write_dbt_profile

start_producer
start_service "consumer" python -u kafka/consumer.py
start_service "dbt" bash -c "while true; do dbt run --project-dir '${ROOT_DIR}/dbt' --profiles-dir '${DBT_PROFILES_DIR}'; sleep \"\${DBT_RUN_INTERVAL_SECONDS:-900}\"; done"
start_service "validation" bash -c "while true; do python -u scripts/run_validations.py; sleep \"\${DATA_QUALITY_INTERVAL_SECONDS:-1800}\"; done"
start_service "embeddings-refresh" bash -c "while true; do python -u rag/embeddings_refresher.py; sleep \"\${EMBEDDINGS_REFRESH_INTERVAL_SECONDS:-86400}\"; done"
start_service "mcp-server" python -u mcp/server.py --http

echo "SmartOps AI started. Logs are in ${LOG_DIR}."
echo "MCP health: http://localhost:${MCP_HTTP_PORT}/health"

while true; do
  for pid in "${PIDS[@]}"; do
    if ! kill -0 "${pid}" >/dev/null 2>&1; then
      echo "A SmartOps AI process exited. Stopping remaining services." >&2
      exit 1
    fi
  done
  sleep 5
done
