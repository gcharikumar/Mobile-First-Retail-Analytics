# backend/app/crud/user.py

"""
User CRUD: Manage users with RBAC, DPDP consent.
"""
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse
from .base import CRUDBase

user_crud = CRUDBase[User, UserCreate, dict](User)

def get_by_email(db: Session, email: str) -> User:
    """Get user by email (unique per tenant)."""
    return db.query(User).filter(User.email == email, User.is_deleted == False).first()
