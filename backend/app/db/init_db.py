# backend/app/db/init_db.py
"""
DB Initialization: Create tables, apply RLS, seed.
Run on startup or manually.
"""
from sqlalchemy import text
from .base import engine
from ..models import *  # Import all models
from ...crud.audit import audit_crud  # For logging init

def create_tables():
    """Create all tables via SQLAlchemy."""
    Base.metadata.create_all(bind=engine)

def apply_rls_policies(engine):
    """Apply RLS policies from SQL file or inline."""
    with open("app/db/rls_policies.sql", "r") as f:
        policies_sql = f.read()
    with engine.connect() as conn:
        conn.execute(text(policies_sql))
        conn.commit()

def seed_data():
    """Seed initial data: Super user, sample tenant, roles."""
    from ...core.security import get_password_hash
    from ...crud.tenant import tenant_crud
    from ...crud.user import user_crud
    from ...crud.role import role_crud
    from ...models.role import Role
    from ...models.user import User
    from ...models.tenant import Tenant
    from uuid import uuid4

    db = SessionLocal()  # Assume SessionLocal defined in base.py

    # Roles
    roles = ["super_user", "owner", "manager", "staff"]
    for role_name in roles:
        if not db.query(Role).filter(Role.name == role_name).first():
            role_crud.create(db, obj_in={"name": role_name, "permissions": json.dumps([])})

    # Super tenant and user
    super_tenant = tenant_crud.create(db, obj_in={"name": "Super Admin", "domain": "super"})
    super_user = user_crud.create(
        db,
        obj_in={
            "email": "admin@retail.com",
            "hashed_password": get_password_hash("supersecret"),
            "full_name": "Super Admin",
            "phone": "hashed_phone",
            "role_id": db.query(Role).filter(Role.name == "super_user").first().id,
            "tenant_id": super_tenant.id,
            "consent_given_at": datetime.utcnow(),
        }
    )

    db.commit()
    db.close()
    print("Seeded super user: admin@retail.com / supersecret")