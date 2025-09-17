# backend/app/api/v1/router.py
"""
API Router: Mounts all endpoints.
Tags for organization, dependencies for global auth.
"""
from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.tenants import router as tenants_router
from .endpoints.users import router as users_router
from .endpoints.pos import router as pos_router
from .endpoints.analytics import router as analytics_router
from .endpoints.whatsapp import router as whatsapp_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["Authentication"])
api_router.include_router(tenants_router, tags=["Tenants"])
api_router.include_router(users_router, tags=["Users"])
api_router.include_router(pos_router, tags=["POS & Billing"])
api_router.include_router(analytics_router, tags=["Analytics"])
api_router.include_router(whatsapp_router, tags=["WhatsApp"])

# Global dependency: Optional auth for public endpoints
# api_router.dependencies = [Depends(get_current_user)]  # Uncomment for full auth