"""
Session Sync — Cross-channel session state management.

OpenClaw pattern: ONE agent system, multiple channels, SAME session.
A worker starts on app voice → continues on WhatsApp → same memory, same context.

This module manages:
1. Unified session IDs that span channels
2. Session state persistence (survives channel switches)
3. Conversation context that carries across channels
4. Last-active channel tracking for response routing

Academic basis: ECO 101 (Transaction Costs) —
reducing channel-switching costs for workers.
If a worker loses network on the app and switches to WhatsApp,
they shouldn't have to repeat their entire context.

Implementation: SQLite-based session store (Hermes L1/L2 pattern).
Sessions are keyed by worker_id, NOT by channel.
"""

import json
import logging
import sqlite3
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from .adapters.base import ChannelType

logger = logging.getLogger(__name__)


@dataclass
class SessionMessage:
    """A single message in a session's conversation history."""
    message_id: str
    role: str                    # "worker" or "agent"
    content: str
    channel: str                 # Which channel this message came from/was sent to
    timestamp: str               # ISO format
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionState:
    """
    Complete session state for a worker.

    This is the "shared brain" across all channels.
    When a worker switches from app to WhatsApp,
    this state carries over — same context, same CFO.
    """
    session_id: str
    worker_id: str
    created_at: str
    updated_at: str
    active_channel: str          # Current active channel
    conversation_history: list[SessionMessage] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)  # Working context
    intent: Optional[str] = None           # Current detected intent
    language: str = "sw"                   # Preferred language
    turn_count: int = 0                    # Total turns across all channels

    def add_message(self, message: SessionMessage) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append(message)
        self.turn_count += 1
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def get_recent_messages(self, limit: int = 20) -> list[SessionMessage]:
        """Get the most recent messages (for context window)."""
        return self.conversation_history[-limit:]

    def get_channel_summary(self) -> dict[str, int]:
        """Get message count per channel (useful for analytics)."""
        summary: dict[str, int] = {}
        for msg in self.conversation_history:
            summary[msg.channel] = summary.get(msg.channel, 0) + 1
        return summary


class SessionSync:
    """
    Cross-channel session synchronization.

    Core principle: Sessions are keyed by WORKER, not by CHANNEL.
    One worker = one active session = shared across all channels.

    Storage: SQLite (Hermes pattern — embedded, zero-dependency).
    This can run on-device (Android) or on the backend server.
    """

    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the session sync store.

        Args:
            db_path: Path to SQLite database. ":memory:" for in-memory (testing).
                     In production on Android: app's internal storage path.
        """
        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create the session tables if they don't exist."""
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency

        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                worker_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                active_channel TEXT NOT NULL,
                context TEXT DEFAULT '{}',
                intent TEXT,
                language TEXT DEFAULT 'sw',
                turn_count INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1
            );

            CREATE INDEX IF NOT EXISTS idx_sessions_worker
                ON sessions(worker_id, is_active);

            CREATE TABLE IF NOT EXISTS session_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                channel TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            );

            CREATE INDEX IF NOT EXISTS idx_messages_session
                ON session_messages(session_id, timestamp);
        """)
        self._conn.commit()

    def get_existing_session(self, worker_id: str) -> Optional[SessionState]:
        """
        Get the existing active session for a worker WITHOUT updating it.

        Used by the gateway to detect channel switches before the session
        is updated with the new channel.
        """
        cursor = self._conn.execute(
            "SELECT session_id FROM sessions WHERE worker_id = ? AND is_active = 1",
            (worker_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return self.get_or_create_session_by_id(row[0])

    def get_or_create_session(
        self,
        worker_id: str,
        channel: ChannelType,
    ) -> SessionState:
        """
        Get the active session for a worker, or create a new one.

        This is the KEY method. No matter which channel the message
        comes from, we get the SAME session for the same worker.
        """
        # Look for existing active session
        cursor = self._conn.execute(
            "SELECT session_id, created_at, updated_at, active_channel, "
            "context, intent, language, turn_count "
            "FROM sessions WHERE worker_id = ? AND is_active = 1",
            (worker_id,),
        )
        row = cursor.fetchone()

        if row:
            session_id = row[0]
            # Update active channel to the one that just sent a message
            self._conn.execute(
                "UPDATE sessions SET active_channel = ?, updated_at = ? WHERE session_id = ?",
                (channel.value, datetime.now(timezone.utc).isoformat(), session_id),
            )
            self._conn.commit()

            # Load conversation history
            history = self._load_history(session_id)

            return SessionState(
                session_id=session_id,
                worker_id=worker_id,
                created_at=row[1],
                updated_at=row[2],
                active_channel=channel.value,
                conversation_history=history,
                context=json.loads(row[4]) if row[4] else {},
                intent=row[5],
                language=row[6] or "sw",
                turn_count=row[7] or 0,
            )

        # Create new session
        session_id = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()

        self._conn.execute(
            "INSERT INTO sessions (session_id, worker_id, created_at, updated_at, "
            "active_channel, context, language) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (session_id, worker_id, now, now, channel.value, "{}", "sw"),
        )
        self._conn.commit()

        logger.info(f"Created new session {session_id} for worker {worker_id} on {channel.value}")

        return SessionState(
            session_id=session_id,
            worker_id=worker_id,
            created_at=now,
            updated_at=now,
            active_channel=channel.value,
            language="sw",
        )

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        channel: ChannelType,
        metadata: Optional[dict] = None,
    ) -> str:
        """
        Persist a message to the session history.

        Args:
            session_id: The session to add the message to
            role: "worker" or "agent"
            content: Message content
            channel: Which channel the message came from/was sent to
            metadata: Additional metadata

        Returns:
            The message_id
        """
        message_id = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()

        self._conn.execute(
            "INSERT INTO session_messages "
            "(session_id, message_id, role, content, channel, timestamp, metadata) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                session_id,
                message_id,
                role,
                content,
                channel.value,
                now,
                json.dumps(metadata or {}),
            ),
        )

        # Update session turn count and timestamp
        self._conn.execute(
            "UPDATE sessions SET turn_count = turn_count + 1, updated_at = ? "
            "WHERE session_id = ?",
            (now, session_id),
        )
        self._conn.commit()

        return message_id

    def update_session_context(
        self,
        session_id: str,
        context: dict[str, Any],
    ) -> None:
        """
        Update the session's working context.

        This is how context carries across channels.
        E.g., if the worker was discussing inventory on the app,
        and switches to WhatsApp, the inventory context is preserved.
        """
        self._conn.execute(
            "UPDATE sessions SET context = ?, updated_at = ? WHERE session_id = ?",
            (
                json.dumps(context),
                datetime.now(timezone.utc).isoformat(),
                session_id,
            ),
        )
        self._conn.commit()

    def set_session_intent(
        self,
        session_id: str,
        intent: str,
    ) -> None:
        """Set the current intent for the session."""
        self._conn.execute(
            "UPDATE sessions SET intent = ?, updated_at = ? WHERE session_id = ?",
            (intent, datetime.now(timezone.utc).isoformat(), session_id),
        )
        self._conn.commit()

    def close_session(self, session_id: str) -> None:
        """
        Mark a session as inactive (end of conversation).

        The session data is preserved for history/replay,
        but no new messages will be routed to it.
        """
        self._conn.execute(
            "UPDATE sessions SET is_active = 0, updated_at = ? WHERE session_id = ?",
            (datetime.now(timezone.utc).isoformat(), session_id),
        )
        self._conn.commit()
        logger.info(f"Closed session {session_id}")

    def get_session_history(
        self,
        session_id: str,
        limit: int = 50,
    ) -> list[SessionMessage]:
        """Get conversation history for a session."""
        return self._load_history(session_id, limit)

    def get_worker_sessions(
        self,
        worker_id: str,
        include_closed: bool = False,
    ) -> list[SessionState]:
        """Get all sessions for a worker."""
        query = "SELECT session_id FROM sessions WHERE worker_id = ?"
        params: list = [worker_id]

        if not include_closed:
            query += " AND is_active = 1"

        query += " ORDER BY updated_at DESC"

        cursor = self._conn.execute(query, params)
        sessions = []
        for row in cursor.fetchall():
            session = self.get_or_create_session_by_id(row[0])
            if session:
                sessions.append(session)

        return sessions

    def get_or_create_session_by_id(self, session_id: str) -> Optional[SessionState]:
        """Get a session by its ID."""
        cursor = self._conn.execute(
            "SELECT session_id, worker_id, created_at, updated_at, active_channel, "
            "context, intent, language, turn_count "
            "FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()

        if not row:
            return None

        history = self._load_history(session_id)

        return SessionState(
            session_id=row[0],
            worker_id=row[1],
            created_at=row[2],
            updated_at=row[3],
            active_channel=row[4],
            conversation_history=history,
            context=json.loads(row[5]) if row[5] else {},
            intent=row[6],
            language=row[7] or "sw",
            turn_count=row[8] or 0,
        )

    def get_channel_stats(self, session_id: str) -> dict[str, Any]:
        """
        Get channel usage statistics for a session.

        Useful for understanding how workers switch between channels.
        """
        cursor = self._conn.execute(
            "SELECT channel, COUNT(*) FROM session_messages "
            "WHERE session_id = ? GROUP BY channel",
            (session_id,),
        )
        channel_counts = dict(cursor.fetchall())

        cursor = self._conn.execute(
            "SELECT MIN(timestamp), MAX(timestamp) FROM session_messages "
            "WHERE session_id = ?",
            (session_id,),
        )
        time_range = cursor.fetchone()

        return {
            "channel_counts": channel_counts,
            "first_message": time_range[0] if time_range else None,
            "last_message": time_range[1] if time_range else None,
            "channels_used": list(channel_counts.keys()),
        }

    def _load_history(
        self,
        session_id: str,
        limit: int = 100,
    ) -> list[SessionMessage]:
        """Load conversation history from the database."""
        cursor = self._conn.execute(
            "SELECT message_id, role, content, channel, timestamp, metadata "
            "FROM session_messages WHERE session_id = ? "
            "ORDER BY timestamp ASC LIMIT ?",
            (session_id, limit),
        )

        messages = []
        for row in cursor.fetchall():
            messages.append(SessionMessage(
                message_id=row[0],
                role=row[1],
                content=row[2],
                channel=row[3],
                timestamp=row[4],
                metadata=json.loads(row[5]) if row[5] else {},
            ))

        return messages

    def cleanup_stale_sessions(self, max_age_hours: int = 24) -> int:
        """
        Close sessions that haven't been active for a while.

        Returns the number of sessions closed.
        """
        cutoff = datetime.now(timezone.utc).isoformat()  # TODO: subtract hours
        cursor = self._conn.execute(
            "UPDATE sessions SET is_active = 0 WHERE is_active = 1 "
            "AND updated_at < datetime('now', ?)",
            (f"-{max_age_hours} hours",),
        )
        self._conn.commit()
        closed = cursor.rowcount
        if closed > 0:
            logger.info(f"Closed {closed} stale sessions (>{max_age_hours}h inactive)")
        return closed

    def status(self) -> dict:
        """Get session sync status for health checks."""
        cursor = self._conn.execute(
            "SELECT COUNT(*) FROM sessions WHERE is_active = 1"
        )
        active_count = cursor.fetchone()[0]

        cursor = self._conn.execute(
            "SELECT COUNT(*) FROM session_messages"
        )
        total_messages = cursor.fetchone()[0]

        return {
            "active_sessions": active_count,
            "total_messages": total_messages,
            "db_path": self._db_path,
        }


# ── Singleton ────────────────────────────────────────────────────

_sync: Optional[SessionSync] = None


def get_session_sync(db_path: str = ":memory:") -> SessionSync:
    """Get or create the singleton SessionSync."""
    global _sync
    if _sync is None:
        _sync = SessionSync(db_path=db_path)
    return _sync
