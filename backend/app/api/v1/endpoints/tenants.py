# backend/app/api/v1/endpoints/tenants.py

"""
Tenant CRUD endpoints: Manage multi-tenancy.
RBAC: Restricted to super_user.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...crud.tenant import tenant_crud
from ...schemas.tenant import TenantCreate, TenantResponse
from ...api.deps import get_db_with_tenant, require_role

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.post("/", response_model=TenantResponse, dependencies=[Depends(require_role("super_user"))])
async def create_tenant(
    tenant_in: TenantCreate,
    db: Session = Depends(get_db_with_tenant),
):
    """
    Create new tenant: Assigns unique domain.
    Triggers audit log.
    """
    existing = tenant_crud.get_by_domain(db, domain=tenant_in.domain)
    if existing:
        raise HTTPException(status_code=400, detail="Domain already exists")
    tenant = tenant_crud.create(db, obj_in=tenant_in)
    # Log action
    from ...core.logging import log_action
    log_action(user_id="system", tenant_id=str(tenant.id), action="tenant.create", details={"name": tenant.name})
    return tenant

@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: UUID,
    db: Session = Depends(get_db_with_tenant),
    current_user: dict = Depends(get_current_user),
):
    """
    Get tenant details: Enforces RLS (tenant_id match).
    """
    tenant = tenant_crud.get(db, id=tenant_id)
    if not tenant or str(tenant.id) != current_user["tenant_id"]:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant