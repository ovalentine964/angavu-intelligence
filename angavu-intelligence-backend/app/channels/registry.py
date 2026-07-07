"""
Channel Registry — Register and manage channels.

OpenClaw pattern: Central registry of all channel adapters.
The gateway queries the registry to find the right adapter for each message.

Also tracks which channels each worker has connected —
critical for routing responses back through the right channel.
"""

import logging
from typing import Optional

from .adapters.base import BaseChannelAdapter, ChannelType, UnifiedMessage

logger = logging.getLogger(__name__)


class ChannelRegistry:
    """
    Registry of all channel adapters.

    Manages:
    1. Adapter registration (App, WhatsApp, SMS, Voice)
    2. Worker → channel mapping (which channels does each worker use?)
    3. Adapter lookup by channel type
    4. Default/preferred channel per worker
    """

    def __init__(self):
        self._adapters: dict[ChannelType, BaseChannelAdapter] = {}
        self._worker_channels: dict[str, list[ChannelType]] = {}  # worker_id → [channels]
        self._worker_active_channel: dict[str, ChannelType] = {}  # worker_id → last active

    def register(self, adapter: BaseChannelAdapter) -> None:
        """Register a channel adapter."""
        channel = adapter.channel_type
        self._adapters[channel] = adapter
        logger.info(f"Registered channel adapter: {adapter.channel_name} ({channel.value})")

    def unregister(self, channel: ChannelType) -> None:
        """Unregister a channel adapter."""
        if channel in self._adapters:
            name = self._adapters[channel].channel_name
            del self._adapters[channel]
            logger.info(f"Unregistered channel adapter: {name}")

    def get_adapter(self, channel: ChannelType) -> Optional[BaseChannelAdapter]:
        """Get the adapter for a specific channel type."""
        return self._adapters.get(channel)

    def get_all_adapters(self) -> dict[ChannelType, BaseChannelAdapter]:
        """Get all registered adapters."""
        return dict(self._adapters)

    def is_registered(self, channel: ChannelType) -> bool:
        """Check if a channel adapter is registered."""
        return channel in self._adapters

    # ── Worker Channel Tracking ─────────────────────────────────

    def track_worker_channel(self, worker_id: str, channel: ChannelType) -> None:
        """
        Record that a worker has used a specific channel.

        Called by the gateway whenever a message arrives from a worker.
        This builds a map of which channels each worker uses.
        """
        if worker_id not in self._worker_channels:
            self._worker_channels[worker_id] = []

        if channel not in self._worker_channels[worker_id]:
            self._worker_channels[worker_id].append(channel)
            logger.info(f"Worker {worker_id} now has channel {channel.value}")

        # Update active channel (most recent)
        self._worker_active_channel[worker_id] = channel

    def get_worker_channels(self, worker_id: str) -> list[ChannelType]:
        """Get all channels a worker has used."""
        return self._worker_channels.get(worker_id, [])

    def get_active_channel(self, worker_id: str) -> Optional[ChannelType]:
        """
        Get the worker's most recently active channel.

        This is where responses should be sent by default —
        the worker is likely still on that channel.
        """
        return self._worker_active_channel.get(worker_id)

    def get_preferred_channel(self, worker_id: str) -> ChannelType:
        """
        Get the worker's preferred channel for receiving responses.

        Priority:
        1. Most recently active channel (worker just sent a message there)
        2. WhatsApp (most workers have it)
        3. SMS (fallback for feature phones)
        4. App (always available)
        """
        active = self.get_active_channel(worker_id)
        if active and self.is_registered(active):
            return active

        # Fallback priority
        fallback_order = [
            ChannelType.WHATSAPP,
            ChannelType.SMS,
            ChannelType.APP_TEXT,
        ]

        worker_channels = self.get_worker_channels(worker_id)
        for channel in fallback_order:
            if channel in worker_channels and self.is_registered(channel):
                return channel

        # Absolute fallback: whatever is registered
        if self._adapters:
            return list(self._adapters.keys())[0]

        return ChannelType.APP_TEXT  # Should never reach here

    # ── Status ──────────────────────────────────────────────────

    def status(self) -> dict:
        """Get registry status for health checks."""
        return {
            "registered_channels": [ch.value for ch in self._adapters],
            "total_workers_tracked": len(self._worker_channels),
            "adapters": {
                ch.value: {
                    "name": adapter.channel_name,
                    "registered": True,
                }
                for ch, adapter in self._adapters.items()
            },
        }


# ── Singleton ────────────────────────────────────────────────────

_registry: Optional[ChannelRegistry] = None


def get_registry() -> ChannelRegistry:
    """Get or create the singleton ChannelRegistry."""
    global _registry
    if _registry is None:
        _registry = ChannelRegistry()
    return _registry
