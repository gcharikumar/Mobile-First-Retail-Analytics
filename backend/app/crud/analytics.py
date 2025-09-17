# backend/app/crud/analytics.py

"""
Analytics CRUD: Materialized views for sales mart.
Triggers ETL updates for forecasting, NLP.
"""
from sqlalchemy import text
from sqlalchemy.orm import Session

def refresh_sales_mart(db: Session, tenant_id: str):
    """
    Refresh sales mart view for tenant.
    Used by ETL for analytics endpoints.
    """
    db.execute(text("""
        REFRESH MATERIALIZED VIEW sales_mart
        WITH DATA
        WHERE tenant_id = :tenant_id
    """), {"tenant_id": tenant_id})
    db.commit()