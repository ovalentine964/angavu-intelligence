"""
OTP Verification Service — Hardened

FIX 5: OTP verification was vulnerable:
- 6-digit code (1M combinations) → Now 6-digit with strict rate limiting
- No rate limiting → Now: 5 attempts per 10 min, 3 OTP requests per hour
- 10-minute expiry → Now: 5-minute expiry
- No lockout → Now: Account locked after 5 failed attempts

FIX: OTP is SECONDARY to Msaidizi app auth.
Msaidizi app uses phone + OTP + biometric. WhatsApp only uses OTP for initial connection.
"""

import hashlib
import logging
import os
import secrets
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class OTPConfig:
    """OTP configuration."""
    code_length: int = 6
    expiry_seconds: int = 300  # 5 minutes (was 10)
    max_attempts: int = 5  # Max verification attempts per OTP
    max_requests_per_hour: int = 3  # Max OTP requests per phone per hour
    lockout_duration_seconds: int = 1800  # 30 minutes lockout after max attempts


@dataclass
class OTPRecord:
    """Stored OTP record."""
    phone_hash: str
    code_hash: str  # SHA-256 hash of the code (never store plaintext)
    created_at: float
    expires_at: float
    attempts: int = 0
    is_used: bool = False


@dataclass
class OTPRequestRecord:
    """Track OTP requests for rate limiting."""
    phone_hash: str
    request_times: list = field(default_factory=list)


@dataclass
class LockoutRecord:
    """Account lockout state."""
    phone_hash: str
    locked_until: float
    reason: str = "too_many_attempts"


class OTPService:
    """
    OTP verification service with security hardening.

    Security measures:
    - OTP codes are hashed before storage (never plaintext)
    - Rate limiting: max 3 OTP requests per hour per phone
    - Attempt limiting: max 5 verification attempts per OTP
    - Short expiry: 5 minutes (reduced from 10)
    - Account lockout: 30 minutes after 5 failed attempts
    - Timing-safe comparison for code verification
    """

    def __init__(self, config: Optional[OTPConfig] = None):
        self.config = config or OTPConfig()
        self._otps: dict[str, OTPRecord] = {}  # phone_hash → OTPRecord
        self._requests: dict[str, OTPRequestRecord] = {}  # phone_hash → request history
        self._lockouts: dict[str, LockoutRecord] = {}  # phone_hash → lockout

    def request_otp(self, phone_hash: str) -> dict:
        """
        Generate and store an OTP for a phone number.

        Returns: { success, message, expires_in_seconds }
        """
        now = time.time()

        # Check lockout
        lockout = self._lockouts.get(phone_hash)
        if lockout and now < lockout.locked_until:
            remaining = int(lockout.locked_until - now)
            return {
                "success": False,
                "message": f"Account locked. Try again in {remaining // 60} minutes.",
                "locked_until": lockout.locked_until,
            }

        # Check rate limit (max requests per hour)
        request_record = self._requests.get(phone_hash)
        if request_record:
            # Remove requests older than 1 hour
            request_record.request_times = [
                t for t in request_record.request_times
                if now - t < 3600
            ]

            if len(request_record.request_times) >= self.config.max_requests_per_hour:
                return {
                    "success": False,
                    "message": "Too many OTP requests. Please wait before requesting again.",
                }
        else:
            request_record = OTPRequestRecord(phone_hash=phone_hash)
            self._requests[phone_hash] = request_record

        # Generate OTP code
        code = self._generate_code()
        code_hash = hashlib.sha256(code.encode()).hexdigest()

        # Store OTP
        self._otps[phone_hash] = OTPRecord(
            phone_hash=phone_hash,
            code_hash=code_hash,
            created_at=now,
            expires_at=now + self.config.expiry_seconds,
        )

        # Track request
        request_record.request_times.append(now)

        logger.info(f"OTP generated for phone hash {phone_hash[:8]}...")

        return {
            "success": True,
            "message": "OTP sent successfully",
            "expires_in_seconds": self.config.expiry_seconds,
        }

    def verify_otp(self, phone_hash: str, code: str) -> dict:
        """
        Verify an OTP code.

        Returns: { success, message }
        """
        now = time.time()

        # Check lockout
        lockout = self._lockouts.get(phone_hash)
        if lockout and now < lockout.locked_until:
            return {
                "success": False,
                "message": "Account locked due to too many failed attempts.",
            }

        # Get OTP record
        otp = self._otps.get(phone_hash)
        if not otp:
            return {
                "success": False,
                "message": "No OTP requested. Please request a new one.",
            }

        # Check expiry
        if now > otp.expires_at:
            del self._otps[phone_hash]
            return {
                "success": False,
                "message": "OTP expired. Please request a new one.",
            }

        # Check if already used
        if otp.is_used:
            return {
                "success": False,
                "message": "OTP already used. Please request a new one.",
            }

        # Check attempts
        if otp.attempts >= self.config.max_attempts:
            self._lock_account(phone_hash)
            del self._otps[phone_hash]
            return {
                "success": False,
                "message": "Too many failed attempts. Account locked for 30 minutes.",
            }

        # Increment attempts
        otp.attempts += 1

        # Timing-safe comparison
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        if not secrets.compare_digest(code_hash, otp.code_hash):
            remaining = self.config.max_attempts - otp.attempts
            if remaining <= 0:
                self._lock_account(phone_hash)
                del self._otps[phone_hash]
                return {
                    "success": False,
                    "message": "Too many failed attempts. Account locked for 30 minutes.",
                }
            return {
                "success": False,
                "message": f"Invalid code. {remaining} attempts remaining.",
            }

        # Success
        otp.is_used = True
        # Clean up
        del self._otps[phone_hash]

        return {
            "success": True,
            "message": "OTP verified successfully.",
        }

    def _generate_code(self) -> str:
        """Generate a cryptographically secure OTP code."""
        # Use secrets for cryptographic randomness
        digits = "0123456789"
        return "".join(secrets.choice(digits) for _ in range(self.config.code_length))

    def _lock_account(self, phone_hash: str) -> None:
        """Lock an account after too many failed attempts."""
        self._lockouts[phone_hash] = LockoutRecord(
            phone_hash=phone_hash,
            locked_until=time.time() + self.config.lockout_duration_seconds,
        )
        logger.warning(f"Account locked for phone hash {phone_hash[:8]}...")

    def cleanup_expired(self) -> int:
        """Clean up expired OTPs and lockouts. Returns count of cleaned items."""
        now = time.time()
        cleaned = 0

        # Clean expired OTPs
        expired_otps = [
            k for k, v in self._otps.items()
            if now > v.expires_at
        ]
        for k in expired_otps:
            del self._otps[k]
            cleaned += 1

        # Clean expired lockouts
        expired_lockouts = [
            k for k, v in self._lockouts.items()
            if now > v.locked_until
        ]
        for k in expired_lockouts:
            del self._lockouts[k]
            cleaned += 1

        return cleaned


# ── Singleton ────────────────────────────────────────────────────

_otp_service: Optional[OTPService] = None


def get_otp_service() -> OTPService:
    """Get or create the singleton OTPService."""
    global _otp_service
    if _otp_service is None:
        _otp_service = OTPService()
    return _otp_service
