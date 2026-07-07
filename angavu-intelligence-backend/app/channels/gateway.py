"""
Multi-Channel Gateway — OpenClaw Pattern for Angavu Intelligence.

One agent system, multiple channels, same session.
Worker talks via app voice → continues via WhatsApp →
same memory, same context, same CFO.

This is the CENTRAL ROUTING HUB. All channel messages flow through here.
The gateway:
1. Receives unified messages from any channel adapter
2. Resolves worker identity
3. Gets/creates the worker's session (shared across channels)
4. Routes to the intelligence pipeline
5. Sends the response back through the appropriate channel

Architecture (OpenClaw pattern):
    Channel Adapter → [UnifiedMessage] → Gateway → Intelligence Pipeline
                                                  ↓
    Channel Adapter ← [ChannelResponse] ← Gateway ← Pipeline Response

The gateway NEVER touches raw channel data.
It only works with UnifiedMessages and ChannelResponses.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from .adapters.base import (
    BaseChannelAdapter,
    ChannelResponse,
    ChannelType,
    UnifiedMessage,
)
from .registry import ChannelRegistry, get_registry
from .session_sync import SessionSync, get_session_sync

logger = logging.getLogger(__name__)


@dataclass
class GatewayStats:
    """Gateway operational statistics."""
    messages_routed: int = 0
    sessions_created: int = 0
    channel_switches: int = 0
    errors: int = 0
    avg_response_time_ms: float = 0.0


class MultiChannelGateway:
    """
    OpenClaw-style multi-channel gateway for Angavu Intelligence.

    One agent system, multiple channels, same session.
    The worker's "AI CFO" is accessible from ANY channel,
    with full context preservation across channel switches.

    Usage:
        gateway = MultiChannelGateway()
        gateway.registry.register(AppChannelAdapter())
        gateway.registry.register(WhatsAppChannelAdapter())

        # Incoming message from any channel
        response = await gateway.route_message(
            channel=ChannelType.WHATSAPP,
            message="Ripoti ya leo",
            worker_id="worker-uuid",
        )
    """

    def __init__(
        self,
        registry: Optional[ChannelRegistry] = None,
        session_sync: Optional[SessionSync] = None,
    ):
        self.registry = registry or get_registry()
        self.session_sync = session_sync or get_session_sync()
        self.stats = GatewayStats()
        self._pipeline = None  # Lazy-loaded intelligence pipeline

    @property
    def pipeline(self):
        """Lazy-load the intelligence pipeline."""
        if self._pipeline is None:
            try:
                from app.agents.intelligence_pipeline import IntelligencePipeline
                self._pipeline = IntelligencePipeline()
                logger.info("Intelligence pipeline loaded")
            except ImportError:
                logger.warning("Intelligence pipeline not available")
                self._pipeline = _StubPipeline()
        return self._pipeline

    async def route_message(
        self,
        channel: ChannelType,
        message: str,
        worker_id: str,
        raw_data: Optional[dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Route a message from any channel through the agent system.

        This is the MAIN ENTRY POINT for all incoming messages.

        Args:
            channel: Which channel the message came from
            message: The message text (or transcript for voice)
            worker_id: Canonical worker ID (user_id)
            raw_data: Raw channel-specific data for the adapter

        Returns:
            Response text to send back, or None if no response
        """
        import time
        start_time = time.time()

        try:
            # 1. Get the channel adapter
            adapter = self.registry.get_adapter(channel)
            if not adapter:
                logger.error(f"No adapter registered for channel {channel.value}")
                self.stats.errors += 1
                return None

            # 2. Parse into unified message
            if raw_data:
                unified = await adapter.parse_incoming(raw_data)
            else:
                unified = UnifiedMessage(
                    worker_id=worker_id,
                    channel=channel,
                    content=message,
                )

            # 3. Track worker's channel usage
            self.registry.track_worker_channel(worker_id, channel)

            # 4. Get or create session (SAME session across channels)
            #    Check existing session's active channel BEFORE updating
            prev_session = self.session_sync.get_existing_session(worker_id)

            # Detect channel switch before session update
            if prev_session and prev_session.active_channel != channel.value:
                logger.info(
                    f"Channel switch detected for worker {worker_id}: "
                    f"{prev_session.active_channel} → {channel.value}"
                )
                self.stats.channel_switches += 1

            session = self.session_sync.get_or_create_session(worker_id, channel)

            unified.session_id = session.session_id

            # 5. Save worker's message to session history
            self.session_sync.save_message(
                session_id=session.session_id,
                role="worker",
                content=message,
                channel=channel,
                metadata=unified.metadata,
            )

            # 6. Route to intelligence pipeline
            response_text = await self._process_with_pipeline(
                unified=unified,
                session=session,
            )

            # 7. Save agent's response to session history
            if response_text:
                self.session_sync.save_message(
                    session_id=session.session_id,
                    role="agent",
                    content=response_text,
                    channel=channel,
                )

            # 8. Update stats
            elapsed_ms = (time.time() - start_time) * 1000
            self.stats.messages_routed += 1
            self.stats.avg_response_time_ms = (
                (self.stats.avg_response_time_ms * (self.stats.messages_routed - 1) + elapsed_ms)
                / self.stats.messages_routed
            )

            logger.info(
                f"Routed message for worker {worker_id} via {channel.value} "
                f"in {elapsed_ms:.0f}ms"
            )

            return response_text

        except Exception as e:
            logger.error(f"Gateway error for worker {worker_id}: {e}", exc_info=True)
            self.stats.errors += 1
            return "Samahani, kuna tatizo la kiufundi. Jaribu tena baadaye."

    async def send_response(
        self,
        channel: ChannelType,
        worker_id: str,
        response: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> bool:
        """
        Send a response to a worker through a specific channel.

        Used for proactive messages (alerts, reports, reminders).
        The gateway figures out the right channel if not specified.

        Args:
            channel: Channel to send through
            worker_id: Target worker ID
            response: Response text
            metadata: Additional metadata for the response

        Returns:
            True if delivery succeeded
        """
        adapter = self.registry.get_adapter(channel)
        if not adapter:
            logger.error(f"No adapter for channel {channel.value}")
            return False

        # Create channel response
        channel_response = ChannelResponse(
            worker_id=worker_id,
            channel=channel,
            content=response,
            metadata=metadata or {},
        )

        # Format for the specific channel
        payload = await adapter.format_response(channel_response)

        # Deliver
        success = await adapter.deliver(payload, worker_id)

        if success:
            # Also save to session
            session = self.session_sync.get_or_create_session(worker_id, channel)
            self.session_sync.save_message(
                session_id=session.session_id,
                role="agent",
                content=response,
                channel=channel,
            )

        return success

    async def send_to_preferred_channel(
        self,
        worker_id: str,
        response: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> bool:
        """
        Send a response to a worker through their preferred channel.

        Preferred channel = most recently active, or best available.
        Used for proactive messages where we don't know which
        channel the worker is currently using.
        """
        preferred = self.registry.get_preferred_channel(worker_id)
        return await self.send_response(
            channel=preferred,
            worker_id=worker_id,
            response=response,
            metadata=metadata,
        )

    async def broadcast_to_worker(
        self,
        worker_id: str,
        response: str,
        channels: Optional[list[ChannelType]] = None,
    ) -> dict[ChannelType, bool]:
        """
        Send a message to a worker on ALL their connected channels.

        Used for critical alerts (e.g., "Your stock is critically low").
        By default, sends to all channels the worker has used.
        """
        if channels is None:
            channels = self.registry.get_worker_channels(worker_id)

        results = {}
        for channel in channels:
            results[channel] = await self.send_response(
                channel=channel,
                worker_id=worker_id,
                response=response,
            )

        return results

    # ── Internal Processing ─────────────────────────────────────

    async def _process_with_pipeline(
        self,
        unified: UnifiedMessage,
        session: Any,  # SessionState
    ) -> Optional[str]:
        """
        Process a unified message through the intelligence pipeline.

        This is where the actual "thinking" happens.
        The gateway provides context; the pipeline produces the response.
        """
        from app.agents.intelligence_pipeline import PipelineRequest

        # Build context from session (includes cross-channel history)
        context = {
            "session_id": session.session_id,
            "channel": unified.channel.value,
            "language": unified.language,
            "conversation_history": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "channel": msg.channel,
                }
                for msg in session.get_recent_messages(limit=10)
            ],
            "session_context": session.context,
            "turn_count": session.turn_count,
            "is_channel_switch": session.active_channel != unified.channel.value,
        }

        # Create pipeline request
        request = PipelineRequest(
            request_id=unified.message_id,
            worker_id=unified.worker_id,
            query=unified.content,
            context=context,
        )

        # Process through pipeline
        response = self.pipeline.process(request)

        return response.response if response else None

    # ── Health & Status ─────────────────────────────────────────

    def status(self) -> dict[str, Any]:
        """Get gateway status for health checks."""
        return {
            "gateway": "active",
            "stats": {
                "messages_routed": self.stats.messages_routed,
                "sessions_created": self.stats.sessions_created,
                "channel_switches": self.stats.channel_switches,
                "errors": self.stats.errors,
                "avg_response_time_ms": round(self.stats.avg_response_time_ms, 1),
            },
            "registry": self.registry.status(),
            "sessions": self.session_sync.status(),
        }


class _StubPipeline:
    """Stub pipeline when the real one isn't available."""

    def process(self, request):
        """Return a simple echo response."""
        from app.agents.intelligence_pipeline import PipelineResponse
        return PipelineResponse(
            request_id=request.request_id,
            response=(
                f"Msaidizi anachambua ombi lako... "
                f"(Pipeline haijapatikana — ombi: '{request.query}')"
            ),
            confidence=0.5,
        )


# ── Singleton ────────────────────────────────────────────────────

_gateway: Optional[MultiChannelGateway] = None


def get_gateway() -> MultiChannelGateway:
    """Get or create the singleton MultiChannelGateway."""
    global _gateway
    if _gateway is None:
        _gateway = MultiChannelGateway()
    return _gateway
