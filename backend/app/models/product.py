# backend/app/models/product.py

"""
Product Model: Master catalog for POS, inventory.
Used for NLP unification (e.g., 'saree' vs 'sari').
"""
from sqlalchemy import Column, String, Float
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    name = Column(String, index=True, unique=True)  # Unified name
    price = Column(Float)
