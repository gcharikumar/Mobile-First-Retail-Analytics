#!/bin/bash
# scripts/migrate.sh
"""
Run Alembic migrations to apply schema changes.
Usage: ./migrate.sh
"""
cd backend
alembic upgrade head