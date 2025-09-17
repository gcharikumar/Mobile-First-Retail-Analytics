# backend/app/models/customer.py

"""
Customer Model: For loyalty tracking.
DPDP: Hashed phone, consent required.
"""
from sqlalchemy import Column, String, DateTime
from .base import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"
    name = Column(String)
    phone = Column(String, nullable=True)  # Hashed
    consent_given_at = Column(DateTime(timezone=True))  # DPDP
    consent_version = Column(String, default="1.0")