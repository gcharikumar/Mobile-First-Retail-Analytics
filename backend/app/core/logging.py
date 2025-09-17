# backend/app/core/logging.py

"""
Structured logging setup using structlog.
Logs to console and file (JSON for ELK/Prometheus).
Configurable via settings (log level, format).
DPDP: Log user actions without sensitive data.
"""
import structlog
import logging
from ..core.config import settings
from datetime import datetime
import os

def setup_logging():
    """Configure structlog for JSON output, integrate with FastAPI."""
    # Ensure logs dir exists
    os.makedirs("logs", exist_ok=True)
    
    # Shared processors
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # File handler (JSON logs for analysis)
    file_handler = logging.FileHandler(f"logs/app-{datetime.now().strftime('%Y%m%d')}.log")
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Root logger
    logging.getLogger().setLevel(settings.LOG_LEVEL)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(console_handler)
    
    return structlog.get_logger()

logger = setup_logging()

def log_action(user_id: str, tenant_id: str, action: str, details: dict = None):
    """Log user actions for audit (e.g., bill.create). DPDP: No PII."""
    logger.info(
        "action",
        user_id=user_id,
        tenant_id=tenant_id,
        action=action,
        details=details or {},
    )