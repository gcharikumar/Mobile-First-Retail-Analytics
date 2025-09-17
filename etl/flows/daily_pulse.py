""" etl/flows/daily_pulse.py """

"""
Daily Pulse Flow: Sends WhatsApp summary of sales, repeat customers.
Scheduled via prefect.yaml (daily midnight IST).
DPDP: Only sends to opted-in users.
"""
from prefect import flow, task
from sqlalchemy import create_engine
from ..core.config import settings
import pandas as pd
from whatsapp import WhatsApp

wa_client = WhatsApp(access_token=settings.WHATSAPP_TOKEN, phone_number_id="your_id")

@task
def fetch_daily_summary(tenant_id: str) -> dict:
    """Fetch sales, repeat customers from mart."""
    engine = create_engine(settings.DATABASE_URL)
    df = pd.read_sql("""
        SELECT product_name, SUM(quantity) as sales_qty,
               COUNT(DISTINCT customer_phone) as unique_customers,
               COUNT(DISTINCT CASE WHEN prior_purchases > 0 THEN customer_phone END) as repeat_customers
        FROM sales_mart
        WHERE tenant_id = :tenant_id AND date = CURRENT_DATE - INTERVAL '1 day'
        GROUP BY product_name
        ORDER BY sales_qty DESC LIMIT 1
    """, engine, params={"tenant_id": tenant_id})
    return {
        "top_product": df.iloc[0]['product_name'] if not df.empty else "N/A",
        "sales_qty": int(df.iloc[0]['sales_qty']) if not df.empty else 0,
        "repeat_pct": (df.iloc[0]['repeat_customers'] / df.iloc[0]['unique_customers'] * 100) if not df.empty and df.iloc[0]['unique_customers'] > 0 else 0,
    }

@task
def send_whatsapp_pulse(phone: str, summary: dict):
    """Send summary via WhatsApp."""
    msg = f"Daily Pulse: Top product: {summary['top_product']} ({summary['sales_qty']} sold). Repeat customers: {summary['repeat_pct']:.1f}%."
    wa_client.send_message(to=phone, text=msg)

@flow
def daily_pulse_flow(tenant_id: str, owner_phone: str):
    """Orchestrate daily pulse for tenant."""
    if not consent_check(owner_phone):  # DPDP
        return {"status": "skipped", "reason": "no consent"}
    summary = fetch_daily_summary(tenant_id)
    send_whatsapp_pulse(owner_phone, summary)