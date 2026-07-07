"""
WhatsApp Channel Adapter — Wraps existing OpenWA integration.

Converts between the existing WhatsAppBot format and the unified
message format used by the multi-channel gateway.

This adapter wraps the existing whatsapp_bot.py and whatsapp_connection.py
WITHOUT breaking them. The gateway sits ON TOP, not replacing them.
"""

import logging
import os
from typing import Any, Optional

import httpx

from .base import (
    BaseChannelAdapter,
    ChannelType,
    ChannelResponse,
    MessageType,
    UnifiedMessage,
)

logger = logging.getLogger(__name__)


class WhatsAppChannelAdapter(BaseChannelAdapter):
    """
    Adapter for WhatsApp channel via OpenWA.

    Wraps the existing WhatsAppBot/OpenWA infrastructure.
    Resolves WhatsApp JID → canonical worker_id (user_id).
    """

    def __init__(self):
        self.openwa_url = os.environ.get("OPENWA_URL", "http://openwa:3000")
        self._worker_cache: dict[str, str] = {}  # jid → user_id cache

    @property
    def channel_type(self) -> ChannelType:
        return ChannelType.WHATSAPP

    @property
    def channel_name(self) -> str:
        return "WhatsApp"

    async def parse_incoming(self, raw_data: dict[str, Any]) -> UnifiedMessage:
        """
        Parse incoming WhatsApp webhook data.

        Expected raw_data (from OpenWA webhook):
        {
            "from": "254712345678@s.whatsapp.net",
            "text": "message text",
            "user_id": "backend-user-id",
            "message_id": "wa-msg-id",
            "type": "text" | "audio" | "image",
        }
        """
        from_jid = raw_data.get("from", "")
        text = raw_data.get("text", "")
        user_id = raw_data.get("user_id", "")

        # Resolve worker_id from JID if not provided
        if not user_id:
            user_id = await self.resolve_worker_id(from_jid)

        # Determine message type
        msg_type_raw = raw_data.get("type", "text")
        type_map = {
            "text": MessageType.TEXT,
            "audio": MessageType.VOICE,
            "image": MessageType.MEDIA,
            "document": MessageType.MEDIA,
            "location": MessageType.LOCATION,
        }
        message_type = type_map.get(msg_type_raw, MessageType.TEXT)

        msg = UnifiedMessage(
            worker_id=user_id or "",
            channel=ChannelType.WHATSAPP,
            message_type=message_type,
            content=text,
            raw_content=raw_data,
            language="sw",  # Default to Swahili for WhatsApp
            metadata={
                "whatsapp_jid": from_jid,
                "whatsapp_message_id": raw_data.get("message_id"),
            },
        )

        # Voice-specific
        if message_type == MessageType.VOICE:
            msg.audio_url = raw_data.get("audio_url")
            msg.audio_duration = raw_data.get("duration")

        # Location-specific
        if message_type == MessageType.LOCATION:
            msg.latitude = raw_data.get("latitude")
            msg.longitude = raw_data.get("longitude")

        return msg

    async def format_response(self, response: ChannelResponse) -> dict[str, Any]:
        """
        Format response for WhatsApp delivery.

        WhatsApp formatting:
        - Bold: *text*
        - Italic: _text_
        - Max ~65536 chars per message
        - Supports images, documents
        - Supports buttons (via OpenWA interactive messages)
        """
        content = response.content

        # WhatsApp has a generous limit but we should still be concise
        if len(content) > 4000:
            # Truncate with a note
            content = content[:3950] + "\n\n... (ripoti ndefu — angalia programu kwa maelezo kamili)"

        payload: dict[str, Any] = {
            "user_id": response.worker_id,
            "message": content,
        }

        if response.media_url:
            payload["media_url"] = response.media_url

        return payload

    async def deliver(self, payload: dict[str, Any], worker_id: str) -> bool:
        """
        Deliver message via OpenWA.

        Uses the existing OpenWA send-message endpoint.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self.openwa_url}/send-message",
                    json=payload,
                )
                resp.raise_for_status()
                logger.info(f"WhatsApp message delivered to {worker_id}")
                return True
        except httpx.ConnectError:
            logger.error(f"OpenWA unreachable at {self.openwa_url}")
            return False
        except Exception as e:
            logger.error(f"WhatsApp delivery failed for {worker_id}: {e}")
            return False

    async def resolve_worker_id(self, channel_identifier: str) -> Optional[str]:
        """
        Resolve WhatsApp JID to canonical worker_id (user_id).

        Uses the existing User.find_by_whatsapp_phone() lookup.
        """
        # Check cache first
        if channel_identifier in self._worker_cache:
            return self._worker_cache[channel_identifier]

        # Extract phone from JID: "254712345678@s.whatsapp.net" → "254712345678"
        phone = channel_identifier.split("@")[0] if "@" in channel_identifier else channel_identifier

        try:
            # Import here to avoid circular dependency
            from app.models.user import User

            # In production, this would use a proper DB session
            # For now, we return None and rely on the webhook providing user_id
            logger.info(f"Resolving WhatsApp JID {channel_identifier} → phone {phone}")
            return None  # Webhook should provide user_id
        except Exception as e:
            logger.error(f"Failed to resolve WhatsApp JID {channel_identifier}: {e}")
            return None
