# backend/app/schemas/user.py

"""
User Schemas: Input/output for user CRUD.
DPDP: Consent fields.
"""
from .base import BaseSchema
from uuid import UUID
from typing import Optional

class UserCreate(BaseSchema):
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    role_id: UUID
    consent_given: bool = False

class UserResponse(BaseSchema):
    id: UUID
    email: str
    full_name: str
    phone: Optional[str]
    role_id: UUID
    tenant_id: UUID
    consent_given_at: Optional[datetime]
    consent_version: str