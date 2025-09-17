# backend/app/core/config.py
"""
Project-wide configuration using Pydantic Settings.
Handles env vars, secrets, and DPDP compliance flags.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    # Auth
    SECRET_KEY: str = Field(..., env="JWT_SECRET")  # RS256 private key for prod
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Tenancy
    ENABLE_RLS: bool = True
    # Storage
    S3_BUCKET: str = Field(..., env="S3_BUCKET")  # Mumbai region for DPDP
    # WhatsApp
    WHATSAPP_TOKEN: str = Field(..., env="WHATSAPP_TOKEN")
    # DPDP Compliance
    DPDP_CONSENT_REQUIRED: bool = True  # Enforce granular consent
    DATA_RETENTION_DAYS: int = 365  # Auto-purge after
    # Logging/Metrics
    LOG_LEVEL: str = "INFO"
    PROMETHEUS_PORT: int = 8001

    class Config:
        env_file = ".env"

settings = Settings()

