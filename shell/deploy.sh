#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed or is not on PATH." >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker is not running. Start Docker and retry." >&2
  exit 1
fi

if [[ ! -f "${ROOT_DIR}/.env" ]]; then
  echo "Missing .env file at ${ROOT_DIR}/.env." >&2
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
else
  echo "Docker Compose is not available." >&2
  exit 1
fi

echo "Validating Docker Compose configuration..."
"${COMPOSE[@]}" config >/dev/null

echo "Building SmartOps AI containers..."
"${COMPOSE[@]}" build

echo "Starting SmartOps AI stack..."
"${COMPOSE[@]}" up -d

echo
echo "Container status:"
"${COMPOSE[@]}" ps

echo
echo "Running health checks..."
if "${COMPOSE[@]}" ps kafka | grep -q "healthy"; then
  echo "Kafka: healthy"
else
  echo "Kafka: starting or unhealthy"
fi

if curl -fsS "http://localhost:5000/health" >/tmp/smartops-mcp-health.json 2>/dev/null; then
  echo "MCP server: healthy"
  cat /tmp/smartops-mcp-health.json
  echo
else
  echo "MCP server: health endpoint not ready yet"
fi

echo
echo "Next command to watch logs:"
echo "docker compose logs -f"
