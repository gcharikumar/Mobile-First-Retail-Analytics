# backend/app/schemas/tenant.py

"""
Tenant Schemas: Input/output for tenant CRUD.
"""
from .base import BaseSchema
from uuid import UUID

class TenantCreate(BaseSchema):
    name: str
    domain: str

class TenantResponse(BaseSchema):
    id: UUID
    name: str
    domain: str
    created_at: datetime
