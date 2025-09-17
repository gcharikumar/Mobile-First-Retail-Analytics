# backend/app/crud/base.py
"""
Base CRUD: Generic get/create/update/delete.
Uses SQLAlchemy session, handles soft delete.
"""
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import List, Optional, TypeVar, Generic
from uuid import UUID
from ..models.base import BaseModel as Model

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: UUID) -> Optional[ModelType]:
        """Fetch by ID, respect RLS via session var."""
        stmt = select(self.model).where(self.model.id == id, self.model.is_deleted == False)
        return db.scalar(stmt)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Fetch paginated list."""
        stmt = select(self.model).where(self.model.is_deleted == False).offset(skip).limit(limit)
        return db.scalars(stmt).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create instance, set timestamps."""
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """Update fields."""
        update_dict = obj_in.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: UUID) -> ModelType:
        """Soft delete: Set is_deleted=True."""
        obj = self.get(db, id)
        if obj:
            obj.is_deleted = True
            db.add(obj)
            db.commit()
        return obj