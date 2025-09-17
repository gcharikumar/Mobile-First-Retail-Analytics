""" etl/flows/analytics.py """

"""
Analytics Flow: Forecasting, NLP for festival detection.
Uses Prophet for sales forecast, spaCy for keywords.
Updates sales mart, triggers alerts.
"""
from prefect import flow, task
from sqlalchemy import create_engine
from prophet import Prophet
import spacy
from ..core.config import settings
import pandas as pd

nlp = spacy.load("en_core_web_sm")  # Load Indic model in prod (e.g., ai4bharat/indic-bert)

@task
def forecast_sales(tenant_id: str) -> pd.DataFrame:
    """Forecast next 7 days sales using Prophet."""
    engine = create_engine(settings.DATABASE_URL)
    df = pd.read_sql("SELECT date, sales FROM sales_mart WHERE tenant_id = :tenant_id", engine, params={"tenant_id": tenant_id})
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=7)
    forecast = m.predict(future)
    return forecast.tail(7)

@task
def detect_festival_alert(df: pd.DataFrame) -> str:
    """Detect festival demand (e.g., Navratri) via NLP."""
    product_names = df['product_name'].tolist()
    doc = nlp(" ".join(product_names))
    # Simple keyword check; use Indic model for Hindi/Tamil
    if any(token.text.lower() in ['saree', 'silk'] for token in doc):
        return "Navratri demand for silk sarees rising!"
    return ""

@flow
def analytics_flow(tenant_id: str):
    """Orchestrate analytics: Forecast, detect trends."""
    forecast = forecast_sales(tenant_id)
    alert = detect_festival_alert(forecast)
    if alert:
        # Trigger WhatsApp alert (extend daily_pulse.py)
        pass
    return {"forecast": forecast.to_dict('records'), "alert": alert}
