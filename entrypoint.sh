#!/bin/bash
set -e

echo "Applying database migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn main:app --host ${ML_HOST:-0.0.0.0} --port ${ML_PORT:-8000} --reload
