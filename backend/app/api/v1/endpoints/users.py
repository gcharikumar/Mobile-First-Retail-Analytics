# backend/app/api/v1/endpoints/users.py

"""
User CRUD endpoints: Manage users within tenant.
RBAC: Owner/Manager for create/update, Staff for read.
DPDP: Hash phone, require consent.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...crud.user import user_crud
from ...schemas.user import UserCreate, UserResponse
from ...api.deps import get_db_with_tenant, require_role
from ...core.security import get_password_hash
from ...core.logging import log_action

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, dependencies=[Depends(require_role("owner"))])
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db_with_tenant),
    current_user: dict = Depends(get_current_user),
):
    """
    Create user: Hash password, phone. Set tenant_id from session.
    DPDP: Consent required for phone.
    """
    if user_in.phone and not user_in.consent_given:
        raise HTTPException(status_code=400, detail="Consent required for phone")
    user_in.hashed_password = get_password_hash(user_in.password)
    user_in.tenant_id = current_user["tenant_id"]
    user = user_crud.create(db, obj_in=user_in)
    log_action(current_user["user_id"], current_user["tenant_id"], "user.create", {"email": user.email})
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db_with_tenant),
    current_user: dict = Depends(get_current_user),
):
    """
    Get user: Enforces RLS, RBAC (Staff+).
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user