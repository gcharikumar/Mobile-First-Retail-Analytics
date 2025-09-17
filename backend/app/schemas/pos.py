# backend/app/schemas/pos.py
"""
POS Schemas: BillCreate for input, BillResponse for output.
Includes line items, customer (DPDP-aware).
"""
from .base import BaseSchema
from typing import List

class LineItemCreate(BaseSchema):
    product_name: str  # Raw input for NLP unification
    quantity: int = 1
    price: float

class BillCreate(BaseSchema):
    line_items: List[LineItemCreate]
    customer_phone: Optional[str] = None  # Hashed on server
    consent_given: bool = False  # DPDP: Required for phone
    total_amount: Optional[float] = None  # Auto-calc if omitted

class BillResponse(BaseSchema):
    id: UUID
    line_items: List[dict]  # Unified names
    customer_phone: Optional[str] = None  # Hashed
    total_amount: float
    created_at: datetime
    tenant_id: UUID