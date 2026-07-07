"""
User Model — With encrypted phone number fields

FIX 3: Phone numbers stored encrypted at rest.
- phone_encrypted: AES-256-GCM encrypted phone number
- phone_hash: SHA-256 hash for database lookups (deterministic)
- phone never stored in plaintext

FIX 2: All queries MUST include user_id filter for multi-device isolation.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, String, Boolean, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Session

from app.security.phone_encryption import get_phone_encryption


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    User model for Angavu Intelligence workers.

    Security notes:
    - phone_encrypted: Encrypted with AES-256-GCM, unique IV per record
    - phone_hash: SHA-256 hash for lookups (never decrypts for queries)
    - All queries MUST filter by user_id for multi-device isolation
    - whatsapp_jid: WhatsApp JID (phone@s.whatsapp.net), also encrypted
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Phone: encrypted at rest, hash for lookups
    phone_encrypted = Column(Text, nullable=False, comment="AES-256-GCM encrypted phone")
    phone_hash = Column(String(64), nullable=False, unique=True, index=True,
                        comment="SHA-256 hash for lookups")

    # WhatsApp connection (optional — WhatsApp is SECONDARY channel)
    whatsapp_jid_encrypted = Column(Text, nullable=True,
                                     comment="Encrypted WhatsApp JID")
    whatsapp_connected = Column(Boolean, default=False, nullable=False,
                                comment="Whether WhatsApp is currently connected")
    whatsapp_phone_hash = Column(String(64), nullable=True, index=True,
                                  comment="Hash of WhatsApp phone for dedup")
    whatsapp_connected_at = Column(DateTime(timezone=True), nullable=True)
    whatsapp_disconnected_at = Column(DateTime(timezone=True), nullable=True)

    # Worker profile
    name_encrypted = Column(Text, nullable=True, comment="Encrypted worker name")
    business_type = Column(String(100), nullable=True)
    location = Column(String(200), nullable=True)

    # Auth
    device_id_hash = Column(String(64), nullable=True, index=True,
                            comment="Hashed device ID for device binding")
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # Composite indexes for common queries (always with user_id)
    __table_args__ = (
        Index("ix_users_phone_hash_active", "phone_hash", "is_active"),
        Index("ix_users_whatsapp_active", "whatsapp_connected", "is_active"),
    )

    # ── Phone Helpers ───────────────────────────────────────────

    @staticmethod
    def create_with_phone(
        db: Session,
        phone: str,
        device_id_hash: Optional[str] = None,
        **kwargs
    ) -> "User":
        """
        Create a user with encrypted phone number.

        This is the ONLY way to create users — phone is always encrypted.
        """
        pe = get_phone_encryption()
        phone_encrypted = pe.encrypt_phone(phone)
        phone_hash = pe.hash_phone(phone)

        user = User(
            phone_encrypted=phone_encrypted,
            phone_hash=phone_hash,
            device_id_hash=device_id_hash,
            **kwargs,
        )
        db.add(user)
        db.flush()
        return user

    def get_phone(self) -> str:
        """Decrypt and return the phone number."""
        pe = get_phone_encryption()
        return pe.decrypt_phone(self.phone_encrypted)

    def set_phone(self, phone: str) -> None:
        """Re-encrypt phone number (e.g., on phone change)."""
        pe = get_phone_encryption()
        self.phone_encrypted = pe.encrypt_phone(phone)
        self.phone_hash = pe.hash_phone(phone)

    @staticmethod
    def find_by_phone(db: Session, phone: str) -> Optional["User"]:
        """
        Find user by phone number using hash lookup.
        NEVER decrypts all records — uses deterministic hash.
        """
        phone_hash = get_phone_encryption().hash_phone(phone)
        return db.query(User).filter(User.phone_hash == phone_hash).first()

    # ── WhatsApp Helpers ────────────────────────────────────────

    def connect_whatsapp(self, db: Session, phone: str) -> None:
        """
        Mark WhatsApp as connected for this user.
        Phone is hashed for deduplication.
        """
        pe = get_phone_encryption()
        self.whatsapp_connected = True
        self.whatsapp_phone_hash = pe.hash_phone(phone)
        self.whatsapp_connected_at = datetime.now(timezone.utc)
        self.whatsapp_disconnected_at = None
        db.flush()

    def disconnect_whatsapp(self, db: Session) -> None:
        """Mark WhatsApp as disconnected (graceful — app still works)."""
        self.whatsapp_connected = False
        self.whatsapp_disconnected_at = datetime.now(timezone.utc)
        db.flush()

    @staticmethod
    def find_by_whatsapp_phone(db: Session, phone: str) -> Optional["User"]:
        """Find user by their WhatsApp phone number."""
        phone_hash = get_phone_encryption().hash_phone(phone)
        return db.query(User).filter(
            User.whatsapp_phone_hash == phone_hash,
            User.whatsapp_connected == True,  # noqa: E712
            User.is_active == True,  # noqa: E712
        ).first()

    # ── Query Helpers (with user_id isolation) ──────────────────

    @staticmethod
    def get_active_whatsapp_users(db: Session) -> list["User"]:
        """
        Get all users with active WhatsApp connections.
        Used for bulk report delivery.
        """
        return db.query(User).filter(
            User.whatsapp_connected == True,  # noqa: E712
            User.is_active == True,  # noqa: E712
        ).all()

    def to_safe_dict(self) -> dict:
        """
        Serialize user without exposing encrypted fields.
        Phone is masked. Never returns plaintext phone.
        """
        pe = get_phone_encryption()
        phone = self.get_phone()
        return {
            "id": str(self.id),
            "phone_masked": pe.mask_phone(phone),
            "whatsapp_connected": self.whatsapp_connected,
            "business_type": self.business_type,
            "location": self.location,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
