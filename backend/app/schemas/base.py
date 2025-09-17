# backend/app/schemas/base.py (shared)
"""
Pydantic schemas base: Validation, serialization.
Uses v2 for strict mode, Config for orm_mode.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True  # For SQLAlchemy ORM