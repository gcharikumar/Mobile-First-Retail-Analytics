# backend/app/main.py
"""
FastAPI application entry point.
Includes middleware for RLS session var, CORS, logging.
Mounts routers, includes OpenAPI docs with auth.
Production: Add HTTPS, rate limiting (slowapi).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn

from .core.config import settings
from .core.logging import setup_logging  # Structlog
from .db.base import engine, Base
from .db.init_db import create_tables, apply_rls_policies  # Alembic alternative for init
from .api.v1.router import api_router
from .api.deps import get_db  # For lifespan

# Setup logging
setup_logging()

app = FastAPI(
    title="Retail Insights API",
    description="Mobile-first retail data insights platform with multi-tenancy.",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Prod: Restrict to mobile/PWA domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "api.retailinsights.com"])  # Prod hosts

# Mount static for PWA if served from backend (optional)
app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")

# Lifespan: Init DB on startup
@app.on_event("startup")
async def startup_event():
    """On startup: Create tables, apply RLS, seed if needed."""
    Base.metadata.create_all(bind=engine)
    create_tables()  # Custom if Alembic not used
    apply_rls_policies(engine)  # Run SQL policies

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup: Close DB connections."""
    pass  # Engine dispose if needed

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Root redirect to docs
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# Health check
@app.get("/health")
async def health():
    """Basic health endpoint for monitoring."""
    return {"status": "healthy", "version": "0.1.0"}

# Run: uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)