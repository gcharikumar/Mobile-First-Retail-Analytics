# scripts/seed_db.py
"""
Seed Script: Run manually or in CI.
Populates tenants, users, roles, sample products/inventory.
Use: python scripts/seed_db.py
"""
import sys
sys.path.append("backend")  # Add to path

from app.db.base import SessionLocal
from app.db.init_db import seed_data
from app.core.security import get_password_hash
from app.crud.product import product_crud  # Assume Product model/CRUD
from app.models.product import Product
from uuid import uuid4
from datetime import datetime
import json

db = SessionLocal()

# After seed_data() call (from init_db)
# Add sample products (localized)
products = [
    {"name": "Red Saree", "stock": 10, "price": 500.0, "tenant_id": "super_tenant_id"},
    {"name": "लाल साड़ी", "stock": 5, "price": 450.0, "tenant_id": "super_tenant_id"},  # Hindi
    {"name": "சிவப்பு சேலை", "stock": 8, "price": 480.0, "tenant_id": "super_tenant_id"},  # Tamil
]

for prod_data in products:
    if not db.query(Product).filter(Product.name == prod_data["name"]).first():
        product_crud.create(db, obj_in=prod_data)

# Sample customers (hashed phones)
# ...

db.commit()
db.close()
print("Database seeded with sample data.")