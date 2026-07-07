"""
WhatsApp Connection API — Multi-Device Isolated

FIX 2: ALL database queries include user_id filter.
FIX 5: WhatsApp is OPTIONAL — worker can choose not to connect.
FIX: Connection/disconnection is graceful and doesn't affect app functionality.

Architecture:
- Msaidizi app = PRIMARY auth (phone + OTP + biometric)
- WhatsApp = SECONDARY (report delivery only)
- WhatsApp connection is optional per worker
- If WhatsApp disconnects, app still works fully
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.models.user import User
from app.security.phone_encryption import get_phone_encryption

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/whatsapp", tags=["whatsapp"])


# ── Request/Response Models ──────────────────────────────────────

class ConnectRequest(BaseModel):
    """Request to connect WhatsApp for a worker."""
    user_id: UUID = Field(..., description="Worker user ID")
    phone: str = Field(..., description="WhatsApp phone number")


class ConnectResponse(BaseModel):
    """Response after connecting WhatsApp."""
    success: bool
    message: str
    whatsapp_connected: bool
    phone_masked: str


class DisconnectResponse(BaseModel):
    """Response after disconnecting WhatsApp."""
    success: bool
    message: str
    whatsapp_connected: bool


class StatusResponse(BaseModel):
    """WhatsApp connection status for a worker."""
    user_id: str
    whatsapp_connected: bool
    phone_masked: Optional[str] = None
    connected_since: Optional[str] = None
    can_reconnect: bool = True
    message: str


class SendReportRequest(BaseModel):
    """Request to send a report via WhatsApp."""
    user_id: UUID = Field(..., description="Target worker user ID")
    report_type: str = Field(..., description="Report type: daily|weekly|monthly|annual")
    report_content: str = Field(..., description="Report text content")
    chart_base64: Optional[str] = Field(None, description="Chart image as base64 PNG")


# ── Dependency ───────────────────────────────────────────────────

def get_db():
    """Database session dependency."""
    # In production, this would be a proper SQLAlchemy session factory
    # Placeholder for the dependency injection pattern
    pass


# ── Endpoints ────────────────────────────────────────────────────

@router.post("/connect", response_model=ConnectResponse)
async def connect_whatsapp(
    request: ConnectRequest,
    db: Session = Depends(get_db),
):
    """
    Connect WhatsApp for a worker.

    This is OPTIONAL. The worker's app works fully without WhatsApp.
    WhatsApp is only used for report delivery.

    FIX 2: Query is scoped to the specific user_id.
    """
    # FIX 2: Query with user_id filter — no cross-user access
    user = db.query(User).filter(
        User.id == request.user_id,
        User.is_active == True,  # noqa: E712
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or inactive",
        )

    pe = get_phone_encryption()

    # Check if this WhatsApp number is already connected to another user
    existing = User.find_by_whatsapp_phone(db, request.phone)
    if existing and existing.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This WhatsApp number is already connected to another account",
        )

    # Mark as connected
    user.connect_whatsapp(db, request.phone)

    # Send test message via OpenWA
    try:
        await _send_via_openwa(
            user_id=str(user.id),
            phone=request.phone,
            message="Msaidizi imeunganishwa na WhatsApp! Ripoti zitafika hapa. 📊",
        )
    except Exception as e:
        logger.warning(f"Test message failed for user {user.id}: {e}")
        # Don't fail the connection just because test message failed

    return ConnectResponse(
        success=True,
        message="WhatsApp connected successfully. Reports will be delivered here.",
        whatsapp_connected=True,
        phone_masked=pe.mask_phone(pe.normalize_phone(request.phone)),
    )


@router.post("/disconnect", response_model=DisconnectResponse)
async def disconnect_whatsapp(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Disconnect WhatsApp for a worker.
    The app continues to work fully — WhatsApp is optional.
    """
    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True,  # noqa: E712
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.disconnect_whatsapp(db)

    return DisconnectResponse(
        success=True,
        message="WhatsApp disconnected. You can reconnect anytime from the app.",
        whatsapp_connected=False,
    )


@router.get("/status/{user_id}", response_model=StatusResponse)
async def get_whatsapp_status(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get WhatsApp connection status for a specific worker.

    FIX 2: Query scoped to user_id — no cross-user data leakage.
    """
    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True,  # noqa: E712
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    pe = get_phone_encryption()

    phone_masked = None
    if user.whatsapp_connected:
        try:
            phone = user.get_phone()
            phone_masked = pe.mask_phone(phone)
        except Exception:
            phone_masked = "****"

    return StatusResponse(
        user_id=str(user.id),
        whatsapp_connected=user.whatsapp_connected,
        phone_masked=phone_masked,
        connected_since=user.whatsapp_connected_at.isoformat() if user.whatsapp_connected_at else None,
        can_reconnect=True,
        message=(
            "WhatsApp connected. Reports will be delivered here."
            if user.whatsapp_connected
            else "WhatsApp not connected. Connect from the app to receive reports via WhatsApp."
        ),
    )


# ── Internal Helpers ─────────────────────────────────────────────

async def _send_via_openwa(user_id: str, phone: str, message: str) -> dict:
    """
    Send message via OpenWA service.

    FIX 1: Uses configurable URL from env var (Docker service name).
    """
    import httpx
    import os

    openwa_url = os.environ.get("OPENWA_URL", "http://openwa:3000")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{openwa_url}/send-message",
            json={
                "user_id": user_id,
                "phone": phone,
                "message": message,
            },
        )
        response.raise_for_status()
        return response.json()


async def _check_openwa_health() -> dict:
    """Check OpenWA service health."""
    import httpx
    import os

    openwa_url = os.environ.get("OPENWA_URL", "http://openwa:3000")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(f"{openwa_url}/health")
        return response.json()
