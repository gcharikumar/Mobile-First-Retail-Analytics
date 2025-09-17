# backend/app/tests/conftest.py
"""
Pytest fixtures: Test DB (SQLite in-memory), client, override deps.
Uses pytest-asyncio for async if needed.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from ..main import app
from ..db.base import Base, get_db
from ..core.security import create_access_token
from ..core.config import settings

# In-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # :memory: for true in-mem
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Yield test DB session, rollback after."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db_session):
    """Override get_db dep with test session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def super_token():
    """Mock JWT for super user."""
    return create_access_token(data={"user_id": "test_id", "tenant_id": "test_tenant"})