# backend/app/models/base.py (shared)
"""
Base model for all tables: Includes tenant_id for RLS, timestamps, soft delete.
"""
from sqlalchemy import Column, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from uuid import UUID, uuid4

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    tenant_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # RLS key

