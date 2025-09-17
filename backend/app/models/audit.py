# backend/app/models/audit.py

"""
Audit Log Model: Tracks user actions (e.g., bill.create).
DPDP: No sensitive data in details.
"""
from sqlalchemy import Column, String, JSON
from .base import BaseModel
from uuid import UUID

class AuditLog(BaseModel):
    __tablename__ = "audits"
    action = Column(String, nullable=False)  # e.g., 'bill.create'
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    details = Column(JSON)  # Structured data, no PII