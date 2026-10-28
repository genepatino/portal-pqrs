#!/usr/bin/env bash
# Levanta PostgreSQL con Docker Compose y espera a que esté listo (healthy).
# Uso, desde cualquier carpeta:  bash backend/scripts/levantar_db.sh
set -euo pipefail

# Ir a la raíz del repositorio, donde está docker-compose.yml.
cd "$(dirname "$0")/../.."

docker compose up -d db

echo "Esperando a que PostgreSQL esté listo..."
for _ in $(seq 1 30); do
  estado=$(docker inspect -f '{{.State.Health.Status}}' pqrs-db)
  echo "  estado: $estado"
  if [ "$estado" = "healthy" ]; then
    docker compose ps db
    exit 0
  fi
  sleep 2
done

echo "PostgreSQL no quedó healthy. Revisa los logs: docker compose logs db" >&2
exit 1
