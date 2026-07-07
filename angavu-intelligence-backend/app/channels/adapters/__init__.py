"""
Channel Adapters — Normalize different channels into a unified message format.

Each adapter handles:
- Incoming message parsing (channel-specific format → unified Message)
- Outgoing response formatting (unified response → channel-specific format)
- Channel-specific auth and delivery mechanics

The gateway doesn't know about WhatsApp JIDs, SMS numbers, or voice DTMF.
It only sees unified Messages.
"""

from .base import BaseChannelAdapter, UnifiedMessage, ChannelResponse
from .app_adapter import AppChannelAdapter
from .whatsapp_adapter import WhatsAppChannelAdapter
from .sms_adapter import SMSChannelAdapter
from .voice_adapter import VoiceChannelAdapter

__all__ = [
    "BaseChannelAdapter",
    "UnifiedMessage",
    "ChannelResponse",
    "AppChannelAdapter",
    "WhatsAppChannelAdapter",
    "SMSChannelAdapter",
    "VoiceChannelAdapter",
]
