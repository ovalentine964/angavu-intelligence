"""
Tests for the Multi-Channel Gateway.

Verifies the core OpenClaw pattern:
- One agent system, multiple channels, same session
- Worker starts on app → continues on WhatsApp → same memory
- Channel switches preserve context
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

# Add parent to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.channels.gateway import MultiChannelGateway
from app.channels.registry import ChannelRegistry
from app.channels.session_sync import SessionSync
from app.channels.adapters.base import ChannelType, UnifiedMessage, ChannelResponse


# ── Fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def session_sync():
    """In-memory session sync for testing."""
    return SessionSync(db_path=":memory:")


@pytest.fixture
def registry():
    """Empty registry for testing."""
    return ChannelRegistry()


@pytest.fixture
def gateway(registry, session_sync):
    """Gateway with test dependencies."""
    return MultiChannelGateway(registry=registry, session_sync=session_sync)


# ── Session Sync Tests ──────────────────────────────────────────

class TestSessionSync:
    """Test cross-channel session synchronization."""

    def test_create_session(self, session_sync):
        """Creating a session returns a valid SessionState."""
        session = session_sync.get_or_create_session(
            worker_id="worker-1",
            channel=ChannelType.APP_TEXT,
        )
        assert session.worker_id == "worker-1"
        assert session.active_channel == "app_text"
        assert session.session_id

    def test_same_session_across_channels(self, session_sync):
        """
        THE CORE TEST: Same worker gets the SAME session
        regardless of which channel they use.
        """
        # Worker starts on app
        session1 = session_sync.get_or_create_session(
            worker_id="worker-1",
            channel=ChannelType.APP_TEXT,
        )

        # Same worker switches to WhatsApp
        session2 = session_sync.get_or_create_session(
            worker_id="worker-1",
            channel=ChannelType.WHATSAPP,
        )

        # SAME SESSION!
        assert session1.session_id == session2.session_id
        assert session2.active_channel == "whatsapp"  # Updated to new channel

    def test_different_workers_different_sessions(self, session_sync):
        """Different workers get different sessions."""
        session1 = session_sync.get_or_create_session("worker-1", ChannelType.APP_TEXT)
        session2 = session_sync.get_or_create_session("worker-2", ChannelType.APP_TEXT)

        assert session1.session_id != session2.session_id

    def test_message_history_persists(self, session_sync):
        """Messages are saved and retrievable across channel switches."""
        session = session_sync.get_or_create_session("worker-1", ChannelType.APP_TEXT)

        # Worker sends message on app
        session_sync.save_message(
            session_id=session.session_id,
            role="worker",
            content="Ripoti ya leo",
            channel=ChannelType.APP_TEXT,
        )

        # Agent responds on app
        session_sync.save_message(
            session_id=session.session_id,
            role="agent",
            content="Hii ndio ripoti yako...",
            channel=ChannelType.APP_TEXT,
        )

        # Worker switches to WhatsApp and asks a follow-up
        session2 = session_sync.get_or_create_session("worker-1", ChannelType.WHATSAPP)

        # History is preserved!
        history = session_sync.get_session_history(session2.session_id)
        assert len(history) == 2
        assert history[0].content == "Ripoti ya leo"
        assert history[1].content == "Hii ndio ripoti yako..."

    def test_context_preserved_across_channels(self, session_sync):
        """Session context carries across channel switches."""
        session = session_sync.get_or_create_session("worker-1", ChannelType.APP_TEXT)

        # Set context (e.g., worker was discussing inventory)
        session_sync.update_session_context(session.session_id, {
            "topic": "inventory",
            "last_discussed_item": "tomatoes",
            "stock_level": "low",
        })

        # Switch to WhatsApp
        session2 = session_sync.get_or_create_session("worker-1", ChannelType.WHATSAPP)

        # Context is preserved!
        assert session2.context["topic"] == "inventory"
        assert session2.context["last_discussed_item"] == "tomatoes"

    def test_channel_stats(self, session_sync):
        """Channel usage statistics are tracked."""
        session = session_sync.get_or_create_session("worker-1", ChannelType.APP_TEXT)

        session_sync.save_message(session.session_id, "worker", "hello", ChannelType.APP_TEXT)
        session_sync.save_message(session.session_id, "agent", "hi", ChannelType.APP_TEXT)
        session_sync.save_message(session.session_id, "worker", "ripoti", ChannelType.WHATSAPP)

        stats = session_sync.get_channel_stats(session.session_id)
        assert stats["channel_counts"]["app_text"] == 2
        assert stats["channel_counts"]["whatsapp"] == 1
        assert "app_text" in stats["channels_used"]
        assert "whatsapp" in stats["channels_used"]


# ── Registry Tests ──────────────────────────────────────────────

class TestChannelRegistry:
    """Test channel adapter registration and worker tracking."""

    def test_register_adapter(self, registry):
        """Registering an adapter makes it available."""
        adapter = MagicMock()
        adapter.channel_type = ChannelType.APP_TEXT
        adapter.channel_name = "App"

        registry.register(adapter)
        assert registry.is_registered(ChannelType.APP_TEXT)
        assert registry.get_adapter(ChannelType.APP_TEXT) == adapter

    def test_worker_channel_tracking(self, registry):
        """Workers' channel usage is tracked."""
        registry.track_worker_channel("worker-1", ChannelType.APP_TEXT)
        registry.track_worker_channel("worker-1", ChannelType.WHATSAPP)

        channels = registry.get_worker_channels("worker-1")
        assert ChannelType.APP_TEXT in channels
        assert ChannelType.WHATSAPP in channels

    def test_active_channel_tracking(self, registry):
        """Most recently active channel is tracked."""
        registry.track_worker_channel("worker-1", ChannelType.APP_TEXT)
        registry.track_worker_channel("worker-1", ChannelType.WHATSAPP)

        assert registry.get_active_channel("worker-1") == ChannelType.WHATSAPP

    def test_preferred_channel_fallback(self, registry):
        """Preferred channel falls back through priority order."""
        # Only SMS is registered and used
        adapter = MagicMock()
        adapter.channel_type = ChannelType.SMS
        adapter.channel_name = "SMS"
        registry.register(adapter)

        registry.track_worker_channel("worker-1", ChannelType.SMS)

        preferred = registry.get_preferred_channel("worker-1")
        assert preferred == ChannelType.SMS


# ── Gateway Integration Test ────────────────────────────────────

class TestMultiChannelGateway:
    """Test the full gateway flow."""

    @pytest.mark.asyncio
    async def test_route_message_basic(self, gateway):
        """Basic message routing works."""
        # Register a mock adapter
        adapter = MagicMock()
        adapter.channel_type = ChannelType.APP_TEXT
        adapter.channel_name = "App"
        adapter.parse_incoming = AsyncMock(return_value=UnifiedMessage(
            worker_id="worker-1",
            channel=ChannelType.APP_TEXT,
            content="Salio",
        ))
        gateway.registry.register(adapter)

        # Route a message (will use stub pipeline since real one may not be importable)
        response = await gateway.route_message(
            channel=ChannelType.APP_TEXT,
            message="Salio",
            worker_id="worker-1",
        )

        # Should get a response (even if from stub pipeline)
        assert response is not None
        assert len(response) > 0

    @pytest.mark.asyncio
    async def test_cross_channel_session_continuity(self, gateway, session_sync):
        """
        THE INTEGRATION TEST: Message on app, then WhatsApp,
        both use the same session.
        """
        # Register mock adapters
        app_adapter = MagicMock()
        app_adapter.channel_type = ChannelType.APP_TEXT
        app_adapter.channel_name = "App"
        app_adapter.parse_incoming = AsyncMock(side_effect=lambda raw: UnifiedMessage(
            worker_id=raw.get("user_id", ""),
            channel=ChannelType.APP_TEXT,
            content=raw.get("content", ""),
        ))
        gateway.registry.register(app_adapter)

        wa_adapter = MagicMock()
        wa_adapter.channel_type = ChannelType.WHATSAPP
        wa_adapter.channel_name = "WhatsApp"
        wa_adapter.parse_incoming = AsyncMock(side_effect=lambda raw: UnifiedMessage(
            worker_id=raw.get("user_id", ""),
            channel=ChannelType.WHATSAPP,
            content=raw.get("text", ""),
        ))
        gateway.registry.register(wa_adapter)

        # Message 1: Worker uses app
        resp1 = await gateway.route_message(
            channel=ChannelType.APP_TEXT,
            message="Habari",
            worker_id="worker-42",
        )

        # Message 2: Same worker switches to WhatsApp
        resp2 = await gateway.route_message(
            channel=ChannelType.WHATSAPP,
            message="Ripoti ya leo",
            worker_id="worker-42",
        )

        # Both should succeed
        assert resp1 is not None
        assert resp2 is not None

        # Same session
        session = session_sync.get_or_create_session("worker-42", ChannelType.WHATSAPP)
        history = session_sync.get_session_history(session.session_id)
        assert len(history) >= 4  # 2 worker messages + 2 agent responses

        # Stats should reflect the channel switch
        assert gateway.stats.channel_switches >= 1

    @pytest.mark.asyncio
    async def test_send_response(self, gateway):
        """Sending a response through a channel works."""
        adapter = MagicMock()
        adapter.channel_type = ChannelType.WHATSAPP
        adapter.channel_name = "WhatsApp"
        adapter.format_response = AsyncMock(return_value={"message": "test"})
        adapter.deliver = AsyncMock(return_value=True)
        gateway.registry.register(adapter)

        success = await gateway.send_response(
            channel=ChannelType.WHATSAPP,
            worker_id="worker-1",
            response="Ripoti yako imefika!",
        )

        assert success
        adapter.format_response.assert_called_once()
        adapter.deliver.assert_called_once()


# ── Run ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
