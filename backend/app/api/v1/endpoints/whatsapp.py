# backend/app/api/v1/endpoints/whatsapp.py
"""
WhatsApp Business API: Send daily pulse, alerts.
Uses official Meta client or Twilio. Inspired by , , 
Requires webhook for inbound (e.g., confirmations).
DPDP: Opt-in only, revocable.
"""
from fastapi import APIRouter, BackgroundTasks
from whatsapp import WhatsApp  # pip install whatsapp-business-python or similar
from ...core.config import settings

wa_client = WhatsApp(access_token=settings.WHATSAPP_TOKEN, phone_number_id="your_id")

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

async def send_daily_pulse(tenant_id: UUID, owner_phone: str):
    """Background: Daily sales summary."""
    # Fetch from mart: top products, repeat customers %
    summary = "Daily Pulse: Top product: Saree (50 sold). Repeat customers: 25%."
    wa_client.send_message(to=owner_phone, text=summary)

@router.post("/alerts/low-stock")
async def send_low_stock_alert(product: str, qty: int, phone: str, background_tasks: BackgroundTasks):
    """
    Alert: Low stock via WhatsApp.
    """
    if not consent_check(phone):  # DPDP
        return {"error": "No consent"}
    msg = f"Low stock: {product} ({qty} left)"
    background_tasks.add_task(wa_client.send_message, to=phone, text=msg)
    return {"sent": True}