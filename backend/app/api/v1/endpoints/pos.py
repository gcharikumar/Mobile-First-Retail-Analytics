# backend/app/api/v1/endpoints/pos.py
"""
POS/Billing CRUD: Create bill offline-sync compatible (idempotent).
Basic inventory update, customer capture.
DPDP: Consent check before storing phone.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from ...schemas.pos import BillCreate, BillResponse
from ...crud.pos import create_bill, update_inventory
from ...api.deps import get_db_with_tenant, require_role
from ...models.customer import Customer  # Hashed phone

router = APIRouter(prefix="/pos", tags=["POS"])

class LineItem(BaseModel):
    product_name: str  # For NLP unification
    quantity: int
    price: float

@router.post("/bills", response_model=BillResponse, dependencies=[Depends(require_role("staff"))])
async def create_pos_bill(
    bill_in: BillCreate,  # Includes line_items: List[LineItem], customer_phone: Optional[str]
    db: Session = Depends(get_db_with_tenant)
):
    """
    Create bill: Validate stock, unify product names (fuzzy match), update inventory.
    Offline-first: Use bill_id from client if provided (idempotency).
    Analytics trigger: Queue for ETL (top products).
    DPDP: If phone provided, require consent; hash it.
    """
    if bill_in.customer_phone and not bill_in.consent_given:
        raise HTTPException(status_code=400, detail="Consent required for customer data")
    
    # NLP: Unify product names (e.g., 'saree-red' -> 'red saree')
    unified_items = []  # Use fuzzywuzzy.process for matching against master catalog
    
    bill = create_bill(db, obj_in=bill_in)
    for item in bill_in.line_items:
        update_inventory(db, product_name=item.product_name, qty_delta=-item.quantity)
        unified_items.append(item)
    
    # Trigger audit log
    # ... (crud.audit.create)
    
    # Queue for WhatsApp low-stock alert if needed
    return bill