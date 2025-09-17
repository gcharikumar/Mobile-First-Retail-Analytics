# backend/app/api/v1/endpoints/auth.py

"""
Authentication endpoints: Login, refresh, consent.
Uses JWT (RS256), Argon2 for passwords.
DPDP: Consent management for data usage.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ...core.security import create_access_token, verify_password, get_password_hash
from ...core.config import settings
from ...crud.user import user_crud
from ...schemas.extended import ConsentCreate
from ...api.deps import get_db_with_tenant

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_with_tenant),
):
    """
    Login: Validate credentials, issue JWT.
    Returns access token with tenant_id for RLS.
    """
    user = user_crud.get_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"user_id": str(user.id), "tenant_id": str(user.tenant_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/consent")
async def grant_consent(
    consent_in: ConsentCreate,
    db: Session = Depends(get_db_with_tenant),
    current_user: dict = Depends(get_current_user),
):
    """
    DPDP: Record user consent for data purposes.
    Update user model with timestamp, version.
    """
    user = user_crud.get(db, id=current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.consent_given_at = datetime.utcnow()
    user.consent_version = consent_in.version
    db.add(user)
    db.commit()
    return {"status": "consent granted", "purposes": consent_in.purposes}