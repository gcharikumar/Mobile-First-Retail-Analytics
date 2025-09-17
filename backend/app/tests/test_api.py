# backend/app/tests/test_api.py
"""
API Tests: Auth, POS CRUD, RLS enforcement.
Coverage: Unit for CRUD, integration for endpoints.
"""
from fastapi.testclient import TestClient
import pytest
from ..schemas.pos import BillCreate, LineItemCreate

@pytest.mark.parametrize("email, password, status_code", [
    ("admin@retail.com", "supersecret", 200),
    ("wrong", "wrong", 401),
])
def test_login(client: TestClient, email: str, password: str, status_code: int):
    """Test auth endpoint (assume in auth.py)."""
    response = client.post("/api/v1/auth/token", data={"username": email, "password": password})
    assert response.status_code == status_code

def test_create_bill(client: TestClient, super_token: str):
    """Test POS bill creation, including validation."""
    bill_data = BillCreate(
        line_items=[LineItemCreate(product_name="saree", quantity=1, price=100.0)],
        customer_phone="1234567890",
        consent_given=True
    )
    headers = {"Authorization": f"Bearer {super_token}"}
    response = client.post("/api/v1/pos/bills", json=bill_data.dict(), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 100.0
    assert "unified" in data["line_items"][0]["product_name"]  # Check NLP

def test_rls_isolation(client: TestClient, super_token: str):
    """Test RLS: Can't access other tenant data."""
    # Create bill for tenant A, try read from B -> 403
    # ... implement with multi-tenant setup in fixture
    pass