# backend/app/models/tenant.py
"""
Tenant model: Core for multi-tenancy.
"""
from sqlalchemy import String
from .base import BaseModel

class Tenant(BaseModel):
    __tablename__ = "tenants"
    name = Column(String, nullable=False)
    domain = Column(String, unique=True)  # For subdomain isolation if needed

# backend/app/models/user.py
"""
User model with RBAC: Roles link to permissions.
DPDP: consent_given_at, consent_version.
"""
from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"
    name = Column(String, unique=True)  # e.g., 'super_user', 'owner', 'manager', 'staff'
    permissions = Column(String)  # JSON list: ['read:pos', 'write:inventory']

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone = Column(String)  # Hashed for DPDP
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    role = relationship("Role")
    consent_given_at = Column(DateTime(timezone=True))  # DPDP timestamp
    consent_version = Column(String, default="1.0")  # Track updates

