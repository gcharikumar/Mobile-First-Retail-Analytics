# backend/app/crud/pos.py
"""
POS CRUD: Bills and inventory ops.
Integrates NLP unification, stock checks.
"""
from sqlalchemy import func, update
from sqlalchemy.orm import Session
from typing import Optional
from ..schemas.pos import BillCreate, BillResponse
from ..models.pos import Bill, InventoryItem  # Assume models defined similarly

bill_crud = CRUDBase[Bill, BillCreate, dict]  # Update schema as dict for partial

def create_bill(db: Session, obj_in: BillCreate) -> Bill:
    """Override: Unify names, check stock, calc total."""
    # NLP unification (fuzzywuzzy or spaCy)
    unified_items = [unify_product_name(item.product_name) for item in obj_in.line_items]
    
    # Check low stock
    for item in unified_items:
        stock = db.query(func.count(InventoryItem.id)).filter(InventoryItem.name == item, InventoryItem.stock > 0).scalar()
        if stock < item.quantity:
            raise ValueError(f"Low stock for {item}")
    
    bill = bill_crud.create(db, obj_in)
    # Update inventory
    for item in obj_in.line_items:
        stmt = update(InventoryItem).where(InventoryItem.name == item.product_name).values(stock=InventoryItem.stock - item.quantity)
        db.execute(stmt)
    db.commit()
    return bill

def unify_product_name(name: str) -> str:
    """Fuzzy match against catalog; placeholder for NLP."""
    # In prod: Use fuzzywuzzy.process.extractOne(catalog, name, score_cutoff=80)
    catalog = ["saree", "sari", "red saree", "cotton saree"]  # From DB
    # ... implement matching
    return name.lower().replace("sari", "saree").strip()  # Simple example