# backend/app/api/deps.py
"""
Dependencies: Auth, tenant resolution, RBAC checks.
Injects current_user, sets RLS session var.
RBAC: Check role has permission. Inspired by , , , , , 
"""
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Header
from ..crud.user import get_user_by_id
from ..db.base import get_db
from ..core.security import get_current_user
from ..models.user import User

async def get_db_with_tenant(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get DB session, set RLS tenant var."""
    db.execute("SELECT set_config('app.current_tenant_id', %s, false)", (current_user["tenant_id"],))
    return db

def require_role(required_role: str):
    """RBAC Decorator: Check user role."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            current_user = Depends(get_current_user)
            user = get_user_by_id(Depends(get_db), current_user["user_id"])
            if user.role.name != required_role:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage: @router.post("/bills", dependencies=[Depends(require_role("manager"))])