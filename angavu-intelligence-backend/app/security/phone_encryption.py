"""
Phone Number Encryption — Field-Level Encryption for PII

FIX 3: Phone numbers were stored plaintext. Now encrypted at rest.

Architecture:
- AES-256-GCM encryption for phone numbers (same scheme as Android KeyManager)
- Each field gets a unique 12-byte IV
- Phone number hash (SHA-256) for database lookups (no plaintext queries)
- Encryption key from environment variable (KMS in production)

Design decisions:
- Uses cryptography library (same as jwt_config.py)
- IV prepended to ciphertext, Base64-encoded
- Hash is deterministic (for lookups), encryption is random (for confidentiality)
- Phone format normalized before encryption (254XXXXXXXXX)
"""

import base64
import hashlib
import logging
import os
import re
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

logger = logging.getLogger(__name__)

# Phone encryption constants
IV_SIZE_BYTES = 12  # 96-bit IV per NIST SP 800-38D
PHONE_KEY_ENV = "PHONE_ENCRYPTION_KEY"  # 32 bytes hex-encoded


class PhoneEncryption:
    """
    Field-level encryption for phone numbers.

    Usage:
        pe = PhoneEncryption()
        encrypted = pe.encrypt_phone("0712345678")
        decrypted = pe.decrypt_phone(encrypted)
        phone_hash = pe.hash_phone("0712345678")  # For DB lookups
    """

    def __init__(self, key_hex: Optional[str] = None):
        """
        Initialize with encryption key.

        Args:
            key_hex: 32-byte key as hex string. If None, reads from env var.
        """
        key_str = key_hex or os.environ.get(PHONE_KEY_ENV)
        if not key_str:
            raise ValueError(
                f"Phone encryption key not set. "
                f"Set {PHONE_KEY_ENV} environment variable (64 hex chars = 32 bytes)."
            )

        try:
            self._key = bytes.fromhex(key_str)
        except ValueError:
            raise ValueError(f"{PHONE_KEY_ENV} must be a hex-encoded 32-byte key")

        if len(self._key) != 32:
            raise ValueError(f"Encryption key must be 32 bytes, got {len(self._key)}")

        self._aesgcm = AESGCM(self._key)

    @staticmethod
    def normalize_phone(phone: str) -> str:
        """
        Normalize phone number to Kenyan format: 254XXXXXXXXX.

        Handles:
        - 0712345678 → 254712345678
        - +254712345678 → 254712345678
        - 254712345678 → 254712345678
        """
        digits = re.sub(r"\D", "", phone)

        if digits.startswith("254") and len(digits) == 12:
            return digits
        elif digits.startswith("0") and len(digits) == 10:
            return "254" + digits[1:]
        elif len(digits) == 9:
            return "254" + digits

        raise ValueError(f"Invalid phone number format: {phone}")

    def encrypt_phone(self, phone: str) -> str:
        """
        Encrypt a phone number.

        Returns: Base64-encoded [IV || ciphertext || GCM tag]
        """
        normalized = self.normalize_phone(phone)
        iv = os.urandom(IV_SIZE_BYTES)
        ciphertext = self._aesgcm.encrypt(iv, normalized.encode("utf-8"), None)
        # Combine IV + ciphertext
        combined = iv + ciphertext
        return base64.b64encode(combined).decode("ascii")

    def decrypt_phone(self, encrypted: str) -> str:
        """
        Decrypt an encrypted phone number.

        Args:
            encrypted: Base64-encoded encrypted phone from encrypt_phone()

        Returns: Normalized phone number (254XXXXXXXXX)
        """
        combined = base64.b64decode(encrypted)
        if len(combined) <= IV_SIZE_BYTES:
            raise ValueError("Invalid encrypted phone: too short")

        iv = combined[:IV_SIZE_BYTES]
        ciphertext = combined[IV_SIZE_BYTES:]

        plaintext = self._aesgcm.decrypt(iv, ciphertext, None)
        return plaintext.decode("utf-8")

    @staticmethod
    def hash_phone(phone: str) -> str:
        """
        Generate a deterministic hash of a phone number for database lookups.

        This allows querying by phone WITHOUT decrypting all records.
        The hash is SHA-256 of the normalized phone number.

        Returns: 64-char hex string
        """
        normalized = PhoneEncryption.normalize_phone(phone)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        Mask phone number for display (e.g., ****5678).
        """
        if len(phone) >= 4:
            return "*" * (len(phone) - 4) + phone[-4:]
        return "****"


# ── Singleton ────────────────────────────────────────────────────

_phone_encryption: Optional[PhoneEncryption] = None


def get_phone_encryption() -> PhoneEncryption:
    """Get or create the singleton PhoneEncryption instance."""
    global _phone_encryption
    if _phone_encryption is None:
        _phone_encryption = PhoneEncryption()
    return _phone_encryption
