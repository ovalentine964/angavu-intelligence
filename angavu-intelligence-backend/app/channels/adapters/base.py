"""
Base Channel Adapter — Unified message interface.

Every channel (App, WhatsApp, SMS, Voice) implements this interface.
The gateway only works with UnifiedMessages — it never touches raw channel data.

OpenClaw Pattern: Channel Adapters normalize 20+ platforms into unified format.
Angavu Pattern: 4 channels, same idea, lighter weight.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

logger = logging.getLogger(__name__)


class ChannelType(str, Enum):
    """Supported channel types."""
    APP_TEXT = "app_text"
    APP_VOICE = "app_voice"
    WHATSAPP = "whatsapp"
    SMS = "sms"
    USSD = "ussd"
    VOICE_CALL = "voice_call"


class MessageType(str, Enum):
    """Unified message types."""
    TEXT = "text"
    VOICE = "voice"          # Audio message (voice note or call)
    COMMAND = "command"       # Structured command (e.g., USSD menu selection)
    MEDIA = "media"           # Image, document, etc.
    LOCATION = "location"     # GPS coordinates
    INTERACTIVE = "interactive"  # Button/menu response


@dataclass
class UnifiedMessage:
    """
    Channel-agnostic message representation.

    The gateway processes ONLY these. Adapters create them from raw channel data.
    Worker identity is always resolved to user_id — no channel-specific IDs leak.
    """

    message_id: str = field(default_factory=lambda: str(uuid4()))
    worker_id: str = ""                  # Canonical worker ID (user_id in DB)
    channel: ChannelType = ChannelType.APP_TEXT
    message_type: MessageType = MessageType.TEXT
    content: str = ""                    # Text content or transcript
    raw_content: Any = None              # Original channel-specific data
    language: str = "sw"                 # Detected or declared language
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

    # Voice-specific
    audio_url: Optional[str] = None      # URL to audio file (if voice message)
    audio_duration: Optional[float] = None  # Duration in seconds
    transcript: Optional[str] = None     # ASR transcript

    # Location-specific
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Context
    session_id: Optional[str] = None     # Gateway session ID
    in_reply_to: Optional[str] = None    # Message being replied to
    is_first_message: bool = False       # First message in a new session


@dataclass
class ChannelResponse:
    """
    Response to be delivered through a specific channel.

    The gateway produces a generic response; adapters format it
    for their channel (text length limits, media, buttons, etc.).
    """
    response_id: str = field(default_factory=lambda: str(uuid4()))
    worker_id: str = ""
    channel: ChannelType = ChannelType.APP_TEXT
    content: str = ""
    content_type: str = "text"           # "text", "audio", "structured"
    media_url: Optional[str] = None      # For audio/image responses
    metadata: dict[str, Any] = field(default_factory=dict)

    # Channel-specific formatting hints
    max_length: Optional[int] = None     # Character limit (SMS=160, WhatsApp=65536)
    buttons: Optional[list[dict]] = None # Interactive buttons (WhatsApp, App)
    quick_replies: Optional[list[str]] = None  # Quick reply options


class BaseChannelAdapter(ABC):
    """
    Abstract base for channel adapters.

    Each adapter:
    1. Parses incoming channel-specific messages into UnifiedMessage
    2. Formats outgoing ChannelResponse into channel-specific format
    3. Delivers messages through its channel's transport
    """

    @property
    @abstractmethod
    def channel_type(self) -> ChannelType:
        """The channel type this adapter handles."""
        ...

    @property
    @abstractmethod
    def channel_name(self) -> str:
        """Human-readable channel name."""
        ...

    @abstractmethod
    async def parse_incoming(self, raw_data: dict[str, Any]) -> UnifiedMessage:
        """
        Parse channel-specific incoming data into a UnifiedMessage.

        Args:
            raw_data: Raw webhook/callback data from the channel

        Returns:
            UnifiedMessage ready for the gateway

        Raises:
            ValueError: If raw_data is malformed
        """
        ...

    @abstractmethod
    async def format_response(self, response: ChannelResponse) -> dict[str, Any]:
        """
        Format a ChannelResponse for delivery through this channel.

        Args:
            response: Generic response from the gateway

        Returns:
            Channel-specific payload ready for delivery
        """
        ...

    @abstractmethod
    async def deliver(self, payload: dict[str, Any], worker_id: str) -> bool:
        """
        Deliver a formatted message through this channel.

        Args:
            payload: Channel-specific formatted payload
            worker_id: Target worker ID

        Returns:
            True if delivery succeeded
        """
        ...

    async def resolve_worker_id(self, channel_identifier: str) -> Optional[str]:
        """
        Resolve a channel-specific identifier to a canonical worker_id.

        E.g., WhatsApp JID → user_id, phone number → user_id.

        Returns None if worker not found.
        """
        # Default: identifier IS the worker_id (app channel)
        return channel_identifier
