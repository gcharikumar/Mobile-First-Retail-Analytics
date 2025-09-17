# backend/app/api/v1/endpoints/analytics.py
"""
Analytics: Top 5 products, forecasting, festival alerts.
Uses SQL views for marts; Prophet for forecast.
NLP for season detection (e.g., 'Navratri' keywords).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from prophet import Prophet  # For forecasting
from ...api.deps import get_db_with_tenant, require_role

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/top-products")
async def get_top_products(db: Session = Depends(get_db_with_tenant), role=Depends(require_role("manager"))):
    """
    Top 5 products week vs last week.
    Query sales mart view.
    """
    result = db.execute("""
        SELECT product_name, sales_qty, prev_week_qty
        FROM sales_mart
        WHERE tenant_id = current_setting('app.current_tenant_id')::uuid
        ORDER BY sales_qty DESC LIMIT 5
    """).fetchall()
    # Format as dicts
    return [{"product": r[0], "this_week": r[1], "last_week": r[2]} for r in result]

@router.get("/forecast")
async def forecast_sales(db: Session = Depends(get_db_with_tenant)):
    """
    Forecast next week sales using Prophet.
    Load historical from mart, fit model.
    """
    df = pd.read_sql("SELECT date, sales FROM sales_mart WHERE tenant_id = ...", db.bind)
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=7)
    forecast = m.predict(future)
    return forecast.tail(7).to_dict('records')  # Return JSON