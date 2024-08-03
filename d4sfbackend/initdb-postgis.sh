#!/bin/bash

set -e

# Define la función para ejecutar comandos SQL en la base de datos
run_sql() {
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" --command "$1"
}

# Comprueba si la extensión PostGIS ya está instalada
if ! run_sql "SELECT 1 FROM pg_extension WHERE extname = 'postgis';" | grep -q 1; then
    # Si la extensión PostGIS no está instalada, la instala
    run_sql "CREATE EXTENSION postgis;"
fi
