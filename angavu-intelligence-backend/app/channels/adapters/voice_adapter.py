"""
Voice Call Channel Adapter — Accessibility for semi-literate workers.

Handles inbound voice calls where workers speak their queries.
The gateway receives ASR transcripts and responds with TTS audio.

This is the most critical channel for inclusivity —
many informal workers are semi-literate and prefer voice interaction.

Academic basis: ECO 101 (Transaction Costs) —
voice is the lowest-friction channel for workers who
can't easily type or read text.

This is a PLACEHOLDER adapter. Voice call integration
(Twilio Voice, Africa's Talking Voice, or local SIP) comes later.
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


class VoiceChannelAdapter(BaseChannelAdapter):
    """
    Adapter for voice call channel.

    Flow:
    1. Worker calls the Msaidizi number
    2. IVR/Voice gateway streams audio to ASR service
    3. ASR transcript arrives here as a UnifiedMessage
    4. Gateway processes and returns text response
    5. TTS service converts response to audio
    6. Audio played back to the worker

    Worker identity is resolved from the calling phone number.
    """

    def __init__(self, voice_gateway_url: Optional[str] = None):
        self.voice_gateway_url = voice_gateway_url  # Twilio/SIP endpoint

    @property
    def channel_type(self) -> ChannelType:
        return ChannelType.VOICE_CALL

    @property
    def channel_name(self) -> str:
        return "Voice Call"

    async def parse_incoming(self, raw_data: dict[str, Any]) -> UnifiedMessage:
        """
        Parse incoming voice data.

        Expected raw_data (from voice gateway):
        {
            "from": "+254712345678",
            "transcript": "ASR transcript of worker's speech",
            "audio_url": "https://...",  # raw audio for reference
            "confidence": 0.85,
            "language": "sw",
            "call_id": "unique-call-id",
        }
        """
        phone = raw_data.get("from", "")
        transcript = raw_data.get("transcript", "")
        worker_id = await self.resolve_worker_id(phone)

        msg = UnifiedMessage(
            worker_id=worker_id or "",
            channel=ChannelType.VOICE_CALL,
            message_type=MessageType.VOICE,
            content=transcript,
            raw_content=raw_data,
            language=raw_data.get("language", "sw"),
            audio_url=raw_data.get("audio_url"),
            metadata={
                "phone": phone,
                "call_id": raw_data.get("call_id"),
                "asr_confidence": raw_data.get("confidence", 0.0),
            },
        )

        return msg

    async def format_response(self, response: ChannelResponse) -> dict[str, Any]:
        """
        Format response for voice delivery.

        Voice constraints:
        - Must be spoken naturally (no markdown, no URLs, no emojis)
        - Short sentences (listeners can't re-read)
        - Numbers spoken clearly ("elfu tano" not "5,000")
        - Response delivered as TTS audio
        """
        content = response.content

        # Clean for voice: remove all visual formatting
        content = content.replace("*", "").replace("_", "").replace("~", "")
        content = content.replace("📊", "").replace("💰", "").replace("📋", "")
        content = content.replace("🤖", "").replace("✅", "").replace("❌", "")

        # Replace common abbreviations with spoken forms
        content = content.replace("KES", "shilingi za Kenya")
        content = content.replace("USD", "dola")

        # Shorten for voice — keep it under ~30 seconds of speech
        # ~150 words per minute in Swahili, ~30 seconds = ~75 words
        words = content.split()
        if len(words) > 100:
            content = " ".join(words[:100]) + ". Kwa maelezo zaidi, tumia programu ya Msaidizi."

        payload: dict[str, Any] = {
            "text": content,
            "language": response.metadata.get("language", "sw-KE"),
            "call_id": response.metadata.get("call_id"),
            "phone": response.metadata.get("phone"),
        }

        # If TTS audio is available, include it
        if response.media_url:
            payload["audio_url"] = response.media_url

        return payload

    async def deliver(self, payload: dict[str, Any], worker_id: str) -> bool:
        """
        Deliver voice response via the voice gateway.

        The voice gateway handles TTS conversion and audio playback.
        """
        if not self.voice_gateway_url:
            logger.warning("Voice gateway not configured — delivery skipped")
            return False

        try:
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    f"{self.voice_gateway_url}/respond",
                    json=payload,
                )
                resp.raise_for_status()
                logger.info(f"Voice response delivered to worker {worker_id}")
                return True
        except Exception as e:
            logger.error(f"Voice delivery failed for {worker_id}: {e}")
            return False

    async def resolve_worker_id(self, channel_identifier: str) -> Optional[str]:
        """Resolve phone number to canonical worker_id."""
        phone = channel_identifier.strip()
        if not phone.startswith("+"):
            phone = "+" + phone

        try:
            from app.models.user import User
            logger.info(f"Resolving voice call phone {phone} to worker_id")
            return None  # Requires DB session
        except Exception as e:
            logger.error(f"Failed to resolve voice phone {phone}: {e}")
            return None
