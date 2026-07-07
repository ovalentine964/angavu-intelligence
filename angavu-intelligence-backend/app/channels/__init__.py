"""
Multi-Channel Gateway — OpenClaw Pattern for Angavu Intelligence.

One agent system, multiple channels, same session.
Worker talks via app voice → continues via WhatsApp →
same memory, same context, same CFO.

Channels:
- Msaidizi App (voice + text) — PRIMARY
- WhatsApp (via OpenWA) — SECONDARY (reports + conversation)
- SMS/USSD — FALLBACK (feature phones)
- Voice calls — ACCESSIBILITY (semi-literate workers)
"""

from .gateway import MultiChannelGateway, get_gateway
from .registry import ChannelRegistry, get_registry
from .session_sync import SessionSync, get_session_sync

__all__ = [
    "MultiChannelGateway",
    "get_gateway",
    "ChannelRegistry",
    "get_registry",
    "SessionSync",
    "get_session_sync",
]
