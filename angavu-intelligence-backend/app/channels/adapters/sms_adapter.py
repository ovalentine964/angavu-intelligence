"""
SMS/USSD Channel Adapter — Feature phone fallback.

Critical for workers with $20 feature phones (no smartphone, no WhatsApp).
Handles:
- SMS text messages (via Africa's Talking, Twilio, or local gateway)
- USSD menu sessions (structured navigation)

Academic basis: ECO 101 (Transaction Costs) —
reducing channel-switching costs means workers don't lose
their financial context when they switch from app to SMS.

This is a PLACEHOLDER adapter. The SMS/USSD gateway
(Africa's Talking or similar) will be integrated later.
"""

import logging
from typing import Any, Optional

from .base import (
    BaseChannelAdapter,
    ChannelType,
    ChannelResponse,
    MessageType,
    UnifiedMessage,
)

logger = logging.getLogger(__name__)


class SMSChannelAdapter(BaseChannelAdapter):
    """
    Adapter for SMS and USSD channels.

    SMS: Free-form text messages, 160 char limit per segment.
    USSD: Structured menu sessions (*123# style).

    Worker identity is resolved from phone number.
    """

    def __init__(self, sms_gateway_url: Optional[str] = None):
        self.sms_gateway_url = sms_gateway_url  # Africa's Talking / Twilio endpoint

    @property
    def channel_type(self) -> ChannelType:
        return ChannelType.SMS

    @property
    def channel_name(self) -> str:
        return "SMS"

    async def parse_incoming(self, raw_data: dict[str, Any]) -> UnifiedMessage:
        """
        Parse incoming SMS/USSD data.

        Expected raw_data (from SMS gateway webhook):
        {
            "from": "+254712345678",
            "text": "message text",
            "type": "sms" | "ussd",
            "session_id": "ussd-session-id",  # for USSD
            "ussd_code": "*123*1#",  # for USSD
        }
        """
        phone = raw_data.get("from", "")
        text = raw_data.get("text", "")
        msg_type_raw = raw_data.get("type", "sms")

        # Resolve phone to worker_id
        worker_id = await self.resolve_worker_id(phone)

        # Determine message type
        if msg_type_raw == "ussd":
            message_type = MessageType.COMMAND
        else:
            message_type = MessageType.TEXT

        msg = UnifiedMessage(
            worker_id=worker_id or "",
            channel=ChannelType.USSD if msg_type_raw == "ussd" else ChannelType.SMS,
            message_type=message_type,
            content=text,
            raw_content=raw_data,
            language="sw",
            metadata={
                "phone": phone,
                "sms_gateway_session": raw_data.get("session_id"),
            },
        )

        return msg

    async def format_response(self, response: ChannelResponse) -> dict[str, Any]:
        """
        Format response for SMS delivery.

        SMS constraints:
        - 160 chars per segment (GSM-7 encoding)
        - Concatenated SMS: 153 chars per segment (max ~5 segments practical)
        - No rich formatting
        - Keep responses SHORT and actionable
        """
        content = response.content

        # Strip all markdown/formatting for SMS
        content = content.replace("*", "").replace("_", "").replace("~", "")

        # Truncate aggressively — SMS users expect concise messages
        max_sms_length = 450  # ~3 SMS segments
        if len(content) > max_sms_length:
            content = content[:max_sms_length - 30] + "\n... Tumia programu kwa maelezo zaidi."

        payload: dict[str, Any] = {
            "to": response.metadata.get("phone", ""),
            "message": content,
        }

        return payload

    async def deliver(self, payload: dict[str, Any], worker_id: str) -> bool:
        """
        Deliver SMS via the SMS gateway.

        In production, integrates with Africa's Talking or Twilio.
        """
        if not self.sms_gateway_url:
            logger.warning("SMS gateway not configured — delivery skipped")
            return False

        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self.sms_gateway_url}/send",
                    json=payload,
                )
                resp.raise_for_status()
                logger.info(f"SMS delivered to worker {worker_id}")
                return True
        except Exception as e:
            logger.error(f"SMS delivery failed for {worker_id}: {e}")
            return False

    async def resolve_worker_id(self, channel_identifier: str) -> Optional[str]:
        """
        Resolve phone number to canonical worker_id.

        Uses phone hash lookup (same as WhatsApp adapter).
        """
        # Normalize phone
        phone = channel_identifier.strip().replace(" ", "").replace("-", "")
        if not phone.startswith("+"):
            phone = "+" + phone

        try:
            from app.models.user import User
            # In production: DB lookup via phone hash
            logger.info(f"Resolving SMS phone {phone} to worker_id")
            return None  # Requires DB session
        except Exception as e:
            logger.error(f"Failed to resolve SMS phone {phone}: {e}")
            return None
