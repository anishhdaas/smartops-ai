FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

RUN addgroup --system app && \
    adduser --system --ingroup app --home ${APP_HOME} app && \
    apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY producer/requirements.txt /tmp/requirements/producer.txt
COPY kafka/requirements_consumer.txt /tmp/requirements/kafka-consumer.txt
COPY rag/requirements_rag.txt /tmp/requirements/rag.txt
COPY mcp/requirements.txt /tmp/requirements/mcp.txt

RUN pip install --upgrade pip setuptools wheel && \
    pip install \
      -r /tmp/requirements/producer.txt \
      -r /tmp/requirements/kafka-consumer.txt \
      -r /tmp/requirements/rag.txt \
      -r /tmp/requirements/mcp.txt \
      dbt-snowflake \
      great-expectations \
      pyarrow && \
    rm -rf /tmp/requirements

COPY --chown=app:app . ${APP_HOME}

RUN mkdir -p /app/logs /vector_db /app/.dbt && \
    chown -R app:app /app /vector_db

USER app

ENV DBT_PROFILES_DIR=/app/.dbt

CMD ["python", "mcp/server.py", "--http"]
