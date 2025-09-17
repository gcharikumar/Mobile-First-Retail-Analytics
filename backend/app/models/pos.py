# backend/app/models/pos.py

"""
POS Models: Bill, InventoryItem for transactions, stock tracking.
Includes tenant_id for RLS, triggers for low stock alerts.
"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
from uuid import UUID

class Bill(BaseModel):
    __tablename__ = "bills"
    total_amount = Column(Float, nullable=False)
    customer_phone = Column(String, nullable=True)  # Hashed for DPDP
    line_items = Column(JSON)  # List of {product_name, qty, price}

class InventoryItem(BaseModel):
    __tablename__ = "inventory_items"
    name = Column(String, index=True)  # Unified via NLP
    stock = Column(Integer, default=0)
    price = Column(Float)
    low_stock_threshold = Column(Integer, default=5)  # For alerts