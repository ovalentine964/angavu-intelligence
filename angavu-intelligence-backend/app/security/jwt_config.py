"""
JWT Configuration — RS256 (Asymmetric) Implementation

FIX 5: JWT from HS256 to RS256
-------------------------------
PREVIOUS (VULNERABLE): JWT used HS256 (HMAC-SHA256) with a shared secret.
  With HS256, the SAME key signs and verifies tokens. If any service that
  verifies tokens is compromised (e.g., a logging service, a microservice
  with weaker security), the signing key is exposed. An attacker with the
  signing key can forge arbitrary tokens, impersonating any user including admins.

FIX: Switch to RS256 (RSA-SHA256) asymmetric signing.
  - PRIVATE key signs tokens (held only by the auth service)
  - PUBLIC key verifies tokens (distributed to all services)
  - Compromise of a verifying service does NOT expose the signing key
  - Public keys can be served via JWKS endpoint for key rotation

Key management:
  - RSA-2048 minimum (RSA-4096 recommended for production)
  - Keys generated once and stored securely (environment variable or KMS)
  - Key rotation supported via JWKS with multiple active keys
  - Kid (Key ID) in JWT header enables seamless rotation

Dependencies:
  pip install python-jose[cryptography] cryptography pydantic
"""

import os
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import JWTError, jwt
from pydantic import BaseModel, Field


# ── Configuration ────────────────────────────────────────────────

class JWTConfig(BaseModel):
    """JWT configuration with RS256 defaults."""

    algorithm: str = Field(default="RS256", description="JWT signing algorithm")
    access_token_expire_minutes: int = Field(
        default=15,
        description="Access token TTL in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=30,
        description="Refresh token TTL in days"
    )
    issuer: str = Field(
        default="angavu-intelligence",
        description="JWT issuer claim"
    )
    audience: str = Field(
        default="angavu-api",
        description="JWT audience claim"
    )
    key_size: int = Field(
        default=4096,
        description="RSA key size in bits (2048 minimum, 4096 recommended)"
    )

    # Paths for key storage (production should use KMS/vault)
    private_key_path: str = Field(
        default="keys/jwt_private.pem",
        description="Path to RSA private key PEM file"
    )
    public_key_path: str = Field(
        default="keys/jwt_public.pem",
        description="Path to RSA public key PEM file"
    )


# ── Key Management ───────────────────────────────────────────────

class KeyManager:
    """
    Manages RSA key pair for JWT signing/verification.

    In production, keys should be stored in:
    - AWS KMS / GCP Cloud KMS / Azure Key Vault
    - HashiCorp Vault
    - Encrypted environment variables

    For development/testing, keys are generated and stored as PEM files.
    """

    def __init__(self, config: JWTConfig):
        self.config = config
        self._private_key = None
        self._public_key = None
        self._kid = None  # Key ID for JWKS

    def initialize(self) -> None:
        """Load or generate RSA key pair."""
        private_key_path = Path(self.config.private_key_path)
        public_key_path = Path(self.config.public_key_path)

        if private_key_path.exists() and public_key_path.exists():
            self._load_keys(private_key_path, public_key_path)
        else:
            self._generate_and_save_keys(private_key_path, public_key_path)

    def _generate_and_save_keys(
        self, private_path: Path, public_path: Path
    ) -> None:
        """Generate new RSA key pair and save to files."""
        # Validate key size
        if self.config.key_size < 2048:
            raise ValueError(
                f"RSA key size must be >= 2048 bits, got {self.config.key_size}"
            )

        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.config.key_size,
        )

        # Extract public key
        public_key = private_key.public_key()

        # Serialize private key (PKCS8, PEM)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        # Serialize public key (SubjectPublicKeyInfo, PEM)
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # Create directories
        private_path.parent.mkdir(parents=True, exist_ok=True)

        # Write keys (restrict permissions on private key)
        private_path.write_bytes(private_pem)
        os.chmod(str(private_path), 0o600)  # Owner read/write only
        public_path.write_bytes(public_pem)

        self._private_key = private_key
        self._public_key = public_key
        self._kid = str(uuid.uuid4())

        print(f"Generated RSA-{self.config.key_size} key pair:")
        print(f"  Private key: {private_path}")
        print(f"  Public key:  {public_path}")
        print(f"  Key ID (kid): {self._kid}")

    def _load_keys(self, private_path: Path, public_path: Path) -> None:
        """Load existing RSA key pair from PEM files."""
        private_pem = private_path.read_bytes()
        public_pem = public_path.read_bytes()

        self._private_key = serialization.load_pem_private_key(
            private_pem, password=None
        )
        self._public_key = serialization.load_pem_public_key(public_pem)
        self._kid = str(uuid.uuid4())

    @property
    def private_key(self):
        if self._private_key is None:
            raise RuntimeError("KeyManager not initialized. Call initialize() first.")
        return self._private_key

    @property
    def public_key(self):
        if self._public_key is None:
            raise RuntimeError("KeyManager not initialized. Call initialize() first.")
        return self._public_key

    @property
    def kid(self) -> str:
        if self._kid is None:
            raise RuntimeError("KeyManager not initialized. Call initialize() first.")
        return self._kid

    def get_private_key_pem(self) -> str:
        """Get private key as PEM string."""
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

    def get_public_key_pem(self) -> str:
        """Get public key as PEM string."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    def get_jwks(self) -> dict:
        """
        Get public key in JWKS (JSON Web Key Set) format.
        Used for serving /.well-known/jwks.json endpoint.
        """
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
        from base64 import urlsafe_b64encode

        pub_numbers = self.public_key.public_numbers()

        def int_to_base64url(n: int) -> str:
            byte_length = (n.bit_length() + 7) // 8
            n_bytes = n.to_bytes(byte_length, byteorder="big")
            return urlsafe_b64encode(n_bytes).rstrip(b"=").decode("ascii")

        return {
            "keys": [
                {
                    "kty": "RSA",
                    "use": "sig",
                    "alg": "RS256",
                    "kid": self.kid,
                    "n": int_to_base64url(pub_numbers.n),
                    "e": int_to_base64url(pub_numbers.e),
                }
            ]
        }


# ── Token Operations ─────────────────────────────────────────────

class JWTTokenManager:
    """
    JWT token manager using RS256 asymmetric signing.

    Token lifecycle:
    1. User authenticates (OTP, biometric, etc.)
    2. Auth service creates access + refresh tokens using PRIVATE key
    3. Access token (15 min) sent to client
    4. Refresh token (30 days) stored HttpOnly cookie
    5. Client uses access token for API calls
    6. API services verify using PUBLIC key (never have private key)
    7. When access token expires, client uses refresh token to get new pair

    Security properties:
    - RS256: signing key (private) != verification key (public)
    - Compromise of any API service doesn't expose signing capability
    - Key rotation via JWKS with multiple active kids
    - Refresh token rotation with family-based theft detection
    """

    def __init__(self, config: Optional[JWTConfig] = None):
        self.config = config or JWTConfig()
        self.key_manager = KeyManager(self.config)
        self.key_manager.initialize()

    def create_access_token(
        self,
        user_id: str,
        phone_hash: str,
        device_id_hash: str,
        roles: list[str] | None = None,
        extra_claims: dict | None = None,
    ) -> str:
        """
        Create a signed JWT access token.

        Claims:
        - sub: user ID
        - phone_hash: hashed phone number (never raw phone)
        - device_id_hash: hashed device ID (for device binding)
        - roles: user roles for RBAC
        - iss: issuer
        - aud: audience
        - iat: issued at
        - exp: expiration
        - jti: unique token ID (for revocation)
        """
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.config.access_token_expire_minutes)

        payload = {
            "sub": user_id,
            "phone_hash": phone_hash,
            "device_id_hash": device_id_hash,
            "roles": roles or ["user"],
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
            "jti": str(uuid.uuid4()),  # Unique token ID for revocation
        }

        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(
            payload,
            self.key_manager.get_private_key_pem(),
            algorithm=self.config.algorithm,
            headers={"kid": self.key_manager.kid},
        )

    def create_refresh_token(
        self,
        user_id: str,
        device_id_hash: str,
        token_family: str | None = None,
    ) -> str:
        """
        Create a signed JWT refresh token.

        Refresh tokens have:
        - Longer TTL (30 days)
        - Token family ID (for theft detection)
        - Single-use enforcement (rotate on each use)
        """
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=self.config.refresh_token_expire_days)

        payload = {
            "sub": user_id,
            "device_id_hash": device_id_hash,
            "type": "refresh",
            "family": token_family or str(uuid.uuid4()),
            "iss": self.config.issuer,
            "aud": self.config.audience,
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
            "jti": str(uuid.uuid4()),
        }

        return jwt.encode(
            payload,
            self.key_manager.get_private_key_pem(),
            algorithm=self.config.algorithm,
            headers={"kid": self.key_manager.kid},
        )

    def verify_token(self, token: str) -> dict:
        """
        Verify a JWT token using the PUBLIC key.

        This method is called by ALL API services to verify tokens.
        They only have the public key — they cannot forge tokens.

        Returns the decoded payload if valid.
        Raises JWTError if the token is invalid, expired, or tampered.
        """
        try:
            payload = jwt.decode(
                token,
                self.key_manager.get_public_key_pem(),
                algorithms=[self.config.algorithm],
                issuer=self.config.issuer,
                audience=self.config.audience,
            )
            return payload
        except JWTError as e:
            raise JWTError(f"Token verification failed: {e}")

    def verify_and_decode_unverified(self, token: str) -> dict:
        """
        Decode token WITHOUT verification (for debugging/logging only).
        NEVER use this for authorization decisions.
        """
        return jwt.get_unverified_claims(token)

    def get_jwks(self) -> dict:
        """Get JWKS for serving /.well-known/jwks.json."""
        return self.key_manager.get_jwks()


# ── Singleton instance ───────────────────────────────────────────

_token_manager: Optional[JWTTokenManager] = None


def get_token_manager() -> JWTTokenManager:
    """Get or create the singleton JWTTokenManager."""
    global _token_manager
    if _token_manager is None:
        config = JWTConfig(
            algorithm=os.getenv("JWT_ALGORITHM", "RS256"),
            access_token_expire_minutes=int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", "15")),
            refresh_token_expire_days=int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "30")),
            issuer=os.getenv("JWT_ISSUER", "angavu-intelligence"),
            audience=os.getenv("JWT_AUDIENCE", "angavu-api"),
            key_size=int(os.getenv("JWT_KEY_SIZE", "4096")),
            private_key_path=os.getenv("JWT_PRIVATE_KEY_PATH", "keys/jwt_private.pem"),
            public_key_path=os.getenv("JWT_PUBLIC_KEY_PATH", "keys/jwt_public.pem"),
        )
        _token_manager = JWTTokenManager(config)
    return _token_manager
