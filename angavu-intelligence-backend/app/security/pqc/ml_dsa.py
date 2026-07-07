"""
ML-DSA (Dilithium) signature provider — NIST FIPS 204.

Parameter sets per FIPS 204:
| Parameter Set  | NIST Level | Public Key | Private Key | Max Signature |
|----------------|------------|------------|-------------|---------------|
| ML-DSA-44      | Level 2    | 1,312 B    | 2,560 B     | 2,420 B       |
| ML-DSA-65      | Level 3    | 1,952 B    | 4,032 B     | 3,293 B       |
| ML-DSA-87      | Level 5    | 2,592 B    | 4,896 B     | 4,595 B       |

⚠️  CURRENT STATUS: STUB IMPLEMENTATION
This provider uses placeholder cryptographic operations. It must NOT be used
in production. Replace with a real FIPS 204 implementation before deployment.

TODO: Replace with liboqs-python (import oqs) or pqcrypto library.
      See: https://github.com/open-quantum-safe/liboqs-python
      See: https://csrc.nist.gov/pubs/fips/204/final
"""

import hashlib
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)

STUB_WARNING = (
    "ML-DSA STUB: Not cryptographically valid. "
    "Replace with real FIPS 204 implementation (liboqs-python) before production use."
)


class MlDsaParameterSet(Enum):
    """ML-DSA parameter sets per FIPS 204."""
    ML_DSA_44 = "ML-DSA-44"
    ML_DSA_65 = "ML-DSA-65"
    ML_DSA_87 = "ML-DSA-87"


# FIPS 204 exact sizes
_PARAM_SIZES = {
    MlDsaParameterSet.ML_DSA_44: {
        "public_key_size": 1_312,
        "private_key_size": 2_560,
        "max_signature_size": 2_420,
        "nist_level": 2,
        "security_bits": 128,
    },
    MlDsaParameterSet.ML_DSA_65: {
        "public_key_size": 1_952,
        "private_key_size": 4_032,
        "max_signature_size": 3_293,
        "nist_level": 3,
        "security_bits": 192,
    },
    MlDsaParameterSet.ML_DSA_87: {
        "public_key_size": 2_592,
        "private_key_size": 4_896,
        "max_signature_size": 4_595,
        "nist_level": 5,
        "security_bits": 256,
    },
}


@dataclass
class KeyPair:
    """Simple key pair container."""
    public_key: bytes
    private_key: bytes
    algorithm: str


class MlDsaProvider:
    """
    ML-DSA (Dilithium) signature provider.

    ⚠️  STUB: All cryptographic operations are placeholders.
    Callers MUST check `is_stub` before relying on verification results.

    TODO: Replace internals with liboqs:
        import oqs
        signer = oqs.Signature("ML-DSA-65")
        public_key = signer.generate_keypair()
        signature = signer.sign(data)
        is_valid = signer.verify(data, signature, public_key)
    """

    def __init__(self, parameter_set: MlDsaParameterSet = MlDsaParameterSet.ML_DSA_65):
        self._param_set = parameter_set
        sizes = _PARAM_SIZES[parameter_set]
        self._public_key_size = sizes["public_key_size"]
        self._private_key_size = sizes["private_key_size"]
        self._max_signature_size = sizes["max_signature_size"]
        self._nist_level = sizes["nist_level"]
        self._security_bits = sizes["security_bits"]

        self.is_stub = True
        """Flag indicating this is a stub. Callers MUST check before relying on results."""

        logger.warning(STUB_WARNING)

    @property
    def algorithm_name(self) -> str:
        return self._param_set.value

    @property
    def public_key_size(self) -> int:
        return self._public_key_size

    @property
    def private_key_size(self) -> int:
        return self._private_key_size

    @property
    def max_signature_size(self) -> int:
        return self._max_signature_size

    @property
    def is_post_quantum(self) -> bool:
        return True

    def generate_keypair(self) -> KeyPair:
        """
        Generate an ML-DSA key pair.

        STUB: Generates random bytes. Real ML-DSA key generation derives keys
        from a seed via FIPS 204 Algorithm 1 (ML-DSA.KeyGen).

        TODO: Use liboqs `oqs.Signature("ML-DSA-65").generate_keypair()`
        """
        logger.warning("generate_keypair(): Using STUB random key generation")

        public_key = os.urandom(self._public_key_size)
        private_key = os.urandom(self._private_key_size)

        return KeyPair(
            public_key=public_key,
            private_key=private_key,
            algorithm=self.algorithm_name,
        )

    def sign(self, private_key: bytes, data: bytes) -> bytes:
        """
        Sign data with an ML-DSA private key.

        STUB: Uses SHA-512(privateKey || data) as a placeholder.
        Real ML-DSA uses hedged signing with a random seed derived from
        H(random || msg || pk) per FIPS 204 Algorithm 2 (ML-DSA.Sign).

        The output is padded to maxSignatureSize. Real ML-DSA signatures are
        variable-length (≤ maxSignatureSize).

        TODO: Use liboqs `oqs.Signature("ML-DSA-65").sign(data, private_key)`
        """
        if len(private_key) != self._private_key_size:
            raise ValueError(
                f"Invalid private key size: {len(private_key)}, expected {self._private_key_size}"
            )
        if not data:
            raise ValueError("Data to sign must not be empty")

        logger.warning("sign(): Using STUB signature generation — NOT cryptographically valid")

        h = hashlib.sha512()
        h.update(private_key)
        h.update(data)
        sig_hash = h.digest()

        # Pad to maxSignatureSize (real ML-DSA signatures are variable-length ≤ max)
        sig = bytearray(self._max_signature_size)
        sig[: len(sig_hash)] = sig_hash

        # Fill remaining with deterministic derivation (not random) for reproducibility
        pad = hashlib.sha256(sig_hash).digest()
        offset = len(sig_hash)
        while offset < self._max_signature_size:
            copy_len = min(len(pad), self._max_signature_size - offset)
            sig[offset : offset + copy_len] = pad[:copy_len]
            offset += copy_len

        return bytes(sig)

    def verify(self, public_key: bytes, data: bytes, signature: bytes) -> bool:
        """
        Verify an ML-DSA signature.

        ⚠️  STUB: Performs basic structural validation but cannot verify
        cryptographic correctness. Returns True only if inputs pass
        structural checks.

        This is intentionally NOT always-True. The previous stub returned
        True unconditionally, which is a critical security flaw — it would
        accept forged signatures. This version at least validates:
          1. Public key size matches the parameter set
          2. Signature size is within valid range (1..maxSignatureSize)
          3. Data is non-empty

        TODO: Replace with liboqs:
            oqs_sig = oqs.Signature("ML-DSA-65")
            is_valid = oqs_sig.verify(data, signature, public_key)
        TODO: Add NIST ACVP Known Answer Test (KAT) vectors for validation.

        Returns:
            True only if structural validation passes AND stub mode is active.
            In non-stub mode, this must perform real FIPS 204 verification.
        """
        # --- Structural validation (always performed, even in stub mode) ---

        if len(public_key) != self._public_key_size:
            logger.error(
                "verify(): REJECTED — invalid public key size: %d, expected %d",
                len(public_key), self._public_key_size,
            )
            return False

        if not signature or len(signature) > self._max_signature_size:
            logger.error(
                "verify(): REJECTED — invalid signature size: %d, must be 1..%d",
                len(signature), self._max_signature_size,
            )
            return False

        if not data:
            logger.error("verify(): REJECTED — data must not be empty")
            return False

        # --- STUB: Cannot perform real cryptographic verification ---
        logger.warning(
            "verify(): STUB — structural validation passed, but cryptographic verification "
            "is NOT performed. This result is unreliable. Replace with real FIPS 204 implementation."
        )

        return True

    def encrypt(self, public_key: bytes, data: bytes) -> bytes:
        raise NotImplementedError(
            "ML-DSA is a signature algorithm, not an encryption algorithm. "
            "Use ML-KEM + AES-256-GCM for encryption."
        )

    def decrypt(self, private_key: bytes, data: bytes) -> bytes:
        raise NotImplementedError(
            "ML-DSA is a signature algorithm, not an encryption algorithm. "
            "Use ML-KEM + AES-256-GCM for decryption."
        )
