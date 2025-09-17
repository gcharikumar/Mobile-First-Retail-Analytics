# backend/app/crud/audit.py

"""
Audit CRUD: Log actions for compliance.
DPDP: Ensure no PII in details.
"""
from sqlalchemy.orm import Session
from ..models.audit import AuditLog
from ..schemas.extended import AuditLogResponse
from .base import CRUDBase

audit_crud = CRUDBase[AuditLog, dict, dict](AuditLog)
