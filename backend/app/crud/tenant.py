# backend/app/crud/tenant.py

"""
Tenant CRUD: Manage tenants for multi-tenancy.
"""
from sqlalchemy.orm import Session
from ..models.tenant import Tenant
from ..schemas.tenant import TenantCreate, TenantResponse
from .base import CRUDBase

tenant_crud = CRUDBase[Tenant, TenantCreate, dict](Tenant)

def get_by_domain(db: Session, domain: str) -> Tenant:
    """Get tenant by unique domain."""
    return db.query(Tenant).filter(Tenant.domain == domain, Tenant.is_deleted == False).first()
