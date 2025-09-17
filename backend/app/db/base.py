# backend/app/db/base.py

"""
SQLAlchemy DB setup: Engine, session factory.
Handles PostgreSQL connection with RLS support.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

# Create engine (PostgreSQL, Mumbai region for DPDP)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,  # Production-ready
    max_overflow=10,
    echo=False,  # Set True for debug
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    """Dependency: Yield DB session, ensure close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()