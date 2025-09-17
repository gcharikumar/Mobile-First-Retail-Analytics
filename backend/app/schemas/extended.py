# backend/app/schemas/extended.py
"""
Extended Schemas: DPDP consent, audit logs.
Granular consent: Purposes like 'loyalty', 'analytics'.
"""
class ConsentCreate(BaseSchema):
    purposes: List[str]  # e.g., ['loyalty', 'marketing']
    version: str = "1.0"
    revocable: bool = True

class AuditLogResponse(BaseSchema):
    id: UUID
    action: str  # e.g., 'bill.create'
    user_id: UUID
    tenant_id: UUID
    details: dict  # JSON
    timestamp: datetime