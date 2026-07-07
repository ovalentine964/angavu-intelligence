"""
App Channel Adapter — Msaidizi mobile app (voice + text).

The PRIMARY channel. Handles:
- Text messages from the app's chat interface
- Voice messages (audio → ASR transcript → unified message)
- Structured commands from app UI elements

The app is the authenticated identity anchor.
Worker's user_id is established here via phone+OTP+biometric auth.
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


class AppChannelAdapter(BaseChannelAdapter):
    """
    Adapter for the Msaidizi mobile app channel.

    The app is the PRIMARY channel — it establishes identity.
    Other channels (WhatsApp, SMS) resolve to the same user_id
    that was created through the app's auth flow.
    """

    @property
    def channel_type(self) -> ChannelType:
        return ChannelType.APP_TEXT

    @property
    def channel_name(self) -> str:
        return "Msaidizi App"

    async def parse_incoming(self, raw_data: dict[str, Any]) -> UnifiedMessage:
        """
        Parse incoming app message.

        Expected raw_data format:
        {
            "user_id": "uuid-string",
            "type": "text" | "voice" | "command",
            "content": "message text",
            "audio_url": "https://...",  # if voice
            "language": "sw",
            "session_id": "optional-session-id",
        }
        """
        worker_id = raw_data.get("user_id", "")
        content = raw_data.get("content", "")
        msg_type_str = raw_data.get("type", "text")

        # Map to unified message type
        type_map = {
            "text": MessageType.TEXT,
            "voice": MessageType.VOICE,
            "command": MessageType.COMMAND,
            "media": MessageType.MEDIA,
            "location": MessageType.LOCATION,
        }
        message_type = type_map.get(msg_type_str, MessageType.TEXT)

        msg = UnifiedMessage(
            worker_id=worker_id,
            channel=ChannelType.APP_VOICE if message_type == MessageType.VOICE else ChannelType.APP_TEXT,
            message_type=message_type,
            content=content,
            raw_content=raw_data,
            language=raw_data.get("language", "sw"),
            session_id=raw_data.get("session_id"),
        )

        # Voice-specific fields
        if message_type == MessageType.VOICE:
            msg.audio_url = raw_data.get("audio_url")
            msg.audio_duration = raw_data.get("audio_duration")
            msg.transcript = raw_data.get("transcript")  # ASR done client-side or by gateway

        # Location-specific
        if message_type == MessageType.LOCATION:
            msg.latitude = raw_data.get("latitude")
            msg.longitude = raw_data.get("longitude")

        return msg

    async def format_response(self, response: ChannelResponse) -> dict[str, Any]:
        """
        Format response for the app.

        The app supports rich formatting: text, audio, buttons, charts.
        """
        payload: dict[str, Any] = {
            "response_id": response.response_id,
            "worker_id": response.worker_id,
            "content": response.content,
            "content_type": response.content_type,
        }

        if response.media_url:
            payload["media_url"] = response.media_url

        if response.buttons:
            payload["buttons"] = response.buttons

        if response.quick_replies:
            payload["quick_replies"] = response.quick_replies

        # App supports longer messages — no aggressive truncation
        return payload

    async def deliver(self, payload: dict[str, Any], worker_id: str) -> bool:
        """
        Deliver response to the app.

        In production, this pushes via WebSocket/FCM to the app.
        For now, the response is returned via the HTTP request cycle.
        """
        # The app uses request-response for text, WebSocket for real-time.
        # The gateway returns the response; the API layer handles delivery.
        logger.info(f"Delivering app response to worker {worker_id}")
        return True

    async def resolve_worker_id(self, channel_identifier: str) -> Optional[str]:
        """
        For the app channel, the identifier IS the worker_id.
        Auth is handled at the API layer before messages reach the gateway.
        """
        return channel_identifier
