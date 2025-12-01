#!/bin/bash
# wait-for-db.sh


set -e
POSTGRES_HOST="$1"
POSTGRES_USER="$2"
POSTGRES_HOST_AUTH_METHOD="$3"
POSTGRES_DB="$4"
shift 4
cmd="$@"

echo "Waiting for PostgreSQL at $POSTGRES_HOST..."

until PGPASSWORD="$POSTGRES_HOST_AUTH_METHOD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd