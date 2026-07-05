#!/bin/bash

set -e

echo "========================================"
echo " SmartOps Secret Cleanup"
echo "========================================"

echo
echo "1. Creating .gitignore entries..."

touch .gitignore

grep -qxF ".env" .gitignore || echo ".env" >> .gitignore
grep -qxF ".env.*" .gitignore || echo ".env.*" >> .gitignore
grep -qxF "!.env.example" .gitignore || echo "!.env.example" >> .gitignore

echo "Done."

echo
echo "2. Creating .env.example..."

cat > .env.example <<EOF
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_WAREHOUSE=

OPENROUTER_API_KEY=

PINECONE_API_KEY=
PINECONE_HOST=
PINECONE_INDEX=

KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=raw_incidents
EVENTS_PER_HOUR=1080000
EOF

echo "Done."

echo
echo "3. Searching for possible secrets..."

grep -RniE \
"password|secret|token|apikey|api_key|OPENROUTER|PINECONE|SNOWFLAKE_PASSWORD|SNOWFLAKE_USER|SNOWFLAKE_ACCOUNT|sk-or-|pcsk_" \
. \
--exclude-dir=.git \
--exclude=.env \
--exclude=cleanup_secrets.sh || true

echo
echo "========================================"
echo "Finished."
echo "========================================"
