# backend/alembic/env.py

"""
Alembic migration environment: Connects to DB, runs migrations.
Uses SQLAlchemy models from app.models.
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from ..app.models import Base
from ..app.core.config import settings

# Config object from alembic.ini
config = context.config

# Setup logging
fileConfig(config.config_file_name)

# Add DB URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Connectable for migrations
connectable = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

# Run migrations
with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
    )
    
    with context.begin_transaction():
        context.run_migrations()