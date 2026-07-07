"""
Multi-Channel Gateway Webhook — Unified entry point for all channels.

This replaces the channel-specific webhook handling with a SINGLE
endpoint that routes through the multi-channel gateway.

OpenClaw pattern: ONE gateway serves ALL channels.

Routes:
- POST /api/v1/gateway/message — Unified message endpoint (all channels)
- POST /api/v1/gateway/whatsapp — WhatsApp-specific (wraps existing OpenWA webhook)
- GET  /api/v1/gateway/status — Gateway health and stats
"""

import logging
import os

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/gateway", tags=["multi-channel-gateway"])


# ── Request Models ───────────────────────────────────────────────

class GatewayMessageRequest(BaseModel):
    """Unified message from any channel."""
    channel: str                    # "app_text", "app_voice", "whatsapp", "sms", "voice_call"
    worker_id: str                  # Canonical worker ID
    content: str                    # Message text or transcript
    language: str = "sw"
    audio_url: Optional[str] = None
    metadata: Optional[dict] = None


class GatewayMessageResponse(BaseModel):
    """Response from the gateway."""
    success: bool
    response: Optional[str] = None
    session_id: str = ""
    channel: str = ""


# ── Unified Message Endpoint ─────────────────────────────────────

@router.post("/message", response_model=GatewayMessageResponse)
async def handle_gateway_message(request: GatewayMessageRequest):
    """
    Unified message endpoint — all channels route through here.

    The gateway handles:
    1. Session management (same session across channels)
    2. Context preservation (channel switches)
    3. Intelligence pipeline routing
    4. Response formatting for the source channel
    """
    from app.channels.gateway import get_gateway
    from app.channels.adapters.base import ChannelType

    gateway = get_gateway()

    # Map string to ChannelType
    channel_map = {
        "app_text": ChannelType.APP_TEXT,
        "app_voice": ChannelType.APP_VOICE,
        "whatsapp": ChannelType.WHATSAPP,
        "sms": ChannelType.SMS,
        "ussd": ChannelType.USSD,
        "voice_call": ChannelType.VOICE_CALL,
    }

    channel = channel_map.get(request.channel)
    if not channel:
        raise HTTPException(status_code=400, detail=f"Unknown channel: {request.channel}")

    # Route through gateway
    response_text = await gateway.route_message(
        channel=channel,
        message=request.content,
        worker_id=request.worker_id,
        raw_data={
            "user_id": request.worker_id,
            "content": request.content,
            "language": request.language,
            "audio_url": request.audio_url,
            **(request.metadata or {}),
        },
    )

    # Get session ID
    session = gateway.session_sync.get_or_create_session(request.worker_id, channel)

    return GatewayMessageResponse(
        success=True,
        response=response_text,
        session_id=session.session_id,
        channel=request.channel,
    )


# ── WhatsApp-Specific Endpoint ──────────────────────────────────

@router.post("/whatsapp")
async def handle_whatsapp_gateway(request: Request):
    """
    WhatsApp webhook handler — routes through multi-channel gateway.

    This replaces the direct whatsapp_bot.py handling.
    Now WhatsApp messages go through the SAME gateway as app messages.

    Same session, same memory, same CFO.
    """
    from app.channels.gateway import get_gateway
    from app.channels.adapters.base import ChannelType

    gateway = get_gateway()

    # Verify HMAC signature (reuse existing verification)
    from app.services.whatsapp_bot import get_whatsapp_bot
    bot = get_whatsapp_bot()

    signature = request.headers.get("X-Webhook-Signature", "")
    body = await request.body()
    body_str = body.decode("utf-8")

    if not bot.verify_signature(body_str, signature):
        logger.warning("Invalid WhatsApp webhook signature")
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = await request.json()
    from_jid = data.get("from", "")
    text = data.get("text", "")
    user_id = data.get("user_id", "")

    if not from_jid:
        raise HTTPException(status_code=400, detail="Missing 'from' field")

    # Route through multi-channel gateway
    response_text = await gateway.route_message(
        channel=ChannelType.WHATSAPP,
        message=text,
        worker_id=user_id,
        raw_data=data,
    )

    # Send response back via OpenWA
    if response_text:
        import httpx
        openwa_url = os.environ.get("OPENWA_URL", "http://openwa:3000")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                await client.post(
                    f"{openwa_url}/send-message",
                    json={
                        "user_id": user_id,
                        "phone": from_jid.split("@")[0],
                        "message": response_text,
                    },
                )
        except Exception as e:
            logger.error(f"Failed to send WhatsApp response: {e}")

    return {"status": "ok"}


# ── Gateway Status ───────────────────────────────────────────────

@router.get("/status")
async def get_gateway_status():
    """
    Gateway health and statistics.

    Shows: active channels, session count, message stats.
    """
    from app.channels.gateway import get_gateway

    gateway = get_gateway()
    return gateway.status()
