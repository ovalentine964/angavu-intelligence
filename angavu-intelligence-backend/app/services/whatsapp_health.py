"""
WhatsApp Health Monitoring Service

FIX 10: No health monitoring existed. Now monitors:
- OpenWA service health (HTTP + WhatsApp session)
- Connection state tracking
- Consecutive failure detection
- Alert thresholds

FIX 8: Session persistence verification
FIX 9: Connection recovery monitoring
"""

import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    """Current health status of WhatsApp service."""
    is_healthy: bool = False
    whatsapp_connected: bool = False
    openwa_reachable: bool = False
    session_exists: bool = False
    last_check: Optional[datetime] = None
    consecutive_failures: int = 0
    last_error: Optional[str] = None
    state: str = "unknown"  # connected | connecting | disconnected | logged_out


@dataclass
class HealthConfig:
    """Health monitoring configuration."""
    check_interval_seconds: int = 30
    alert_threshold: int = 2  # Alert after N consecutive failures
    openwa_url: str = ""
    admin_phone: Optional[str] = None


class WhatsAppHealthMonitor:
    """
    Monitors WhatsApp/OpenWA service health.

    Features:
    - Periodic health checks
    - Consecutive failure tracking
    - Alert generation when threshold exceeded
    - Session state monitoring
    - Connection recovery detection
    """

    def __init__(self, config: Optional[HealthConfig] = None):
        self.config = config or HealthConfig(
            openwa_url=os.environ.get("OPENWA_URL", "http://openwa:3000"),
        )
        self._status = HealthStatus()
        self._history: list[HealthStatus] = []

    @property
    def status(self) -> HealthStatus:
        """Current health status."""
        return self._status

    async def check_health(self) -> HealthStatus:
        """
        Perform a health check against OpenWA service.

        Checks:
        1. OpenWA HTTP endpoint reachable
        2. WhatsApp session connected
        3. Session data exists on disk
        """
        status = HealthStatus(last_check=datetime.now(timezone.utc))

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.config.openwa_url}/health")

                if response.status_code == 200:
                    data = response.json()
                    status.openwa_reachable = True
                    status.whatsapp_connected = data.get("whatsapp", {}).get("connected", False)
                    status.session_exists = data.get("whatsapp", {}).get("sessionExists", False)
                    status.state = data.get("whatsapp", {}).get("state", "unknown")
                    status.is_healthy = status.whatsapp_connected
                else:
                    status.openwa_reachable = True
                    status.is_healthy = False
                    status.state = "error"
                    status.last_error = f"HTTP {response.status_code}"

        except httpx.ConnectError:
            status.openwa_reachable = False
            status.is_healthy = False
            status.state = "unreachable"
            status.last_error = "OpenWA service unreachable"

        except Exception as e:
            status.is_healthy = False
            status.last_error = str(e)

        # Track consecutive failures
        if status.is_healthy:
            self._status.consecutive_failures = 0
        else:
            self._status.consecutive_failures = self._status.consecutive_failures + 1
            status.consecutive_failures = self._status.consecutive_failures

        self._status = status
        self._history.append(status)

        # Keep only last 100 checks
        if len(self._history) > 100:
            self._history = self._history[-100:]

        return status

    def should_alert(self) -> bool:
        """
        Check if an alert should be raised.

        Alert conditions:
        - Consecutive failures >= threshold
        - WhatsApp logged out (needs re-auth)
        """
        if self._status.consecutive_failures >= self.config.alert_threshold:
            return True

        if self._status.state == "logged_out":
            return True

        return False

    def get_alert_message(self) -> Optional[str]:
        """Generate alert message for admin notification."""
        if not self.should_alert():
            return None

        if self._status.state == "logged_out":
            return (
                "🔴 WhatsApp ALERT: Session logged out!\n"
                "Workers cannot receive reports via WhatsApp.\n"
                "Action needed: Re-scan QR code at OpenWA /qr endpoint."
            )

        if self._status.consecutive_failures >= self.config.alert_threshold:
            return (
                f"🔴 WhatsApp ALERT: {self._status.consecutive_failures} consecutive health check failures!\n"
                f"Last error: {self._status.last_error}\n"
                f"State: {self._status.state}\n"
                "Workers may not be receiving WhatsApp reports."
            )

        return None

    async def alert_admin(self, message: Optional[str] = None) -> None:
        """Send alert to admin (log + optional SMS/email)."""
        alert_msg = message or self.get_alert_message()
        if not alert_msg:
            return

        logger.critical(alert_msg)

        # TODO: Integrate with SMS/email notification
        # For now, just log the alert

    def get_status_summary(self) -> dict:
        """Get a summary of health status for API responses."""
        return {
            "is_healthy": self._status.is_healthy,
            "whatsapp_connected": self._status.whatsapp_connected,
            "openwa_reachable": self._status.openwa_reachable,
            "session_exists": self._status.session_exists,
            "state": self._status.state,
            "consecutive_failures": self._status.consecutive_failures,
            "last_check": self._status.last_check.isoformat() if self._status.last_check else None,
            "last_error": self._status.last_error,
            "should_alert": self.should_alert(),
            "history_count": len(self._history),
        }


# ── Singleton ────────────────────────────────────────────────────

_monitor: Optional[WhatsAppHealthMonitor] = None


def get_health_monitor() -> WhatsAppHealthMonitor:
    """Get or create the singleton health monitor."""
    global _monitor
    if _monitor is None:
        _monitor = WhatsAppHealthMonitor()
    return _monitor
