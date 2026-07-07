"""
ML-KEM (Kyber) key encapsulation mechanism — NIST FIPS 203.

Parameter sets per FIPS 203:
| Parameter Set  | NIST Level | Security Bits | Public Key | Ciphertext | Private Key |
|----------------|------------|---------------|------------|------------|-------------|
| ML-KEM-512     | Level 1    | 128           | 800 B      | 768 B      | 1,632 B     |
| ML-KEM-768     | Level 3    | 192           | 1,184 B    | 1,088 B    | 2,400 B     |
| ML-KEM-1024    | Level 5    | 256           | 1,568 B    | 1,568 B    | 3,168 B     |

Private key sizes (FIPS 203, Section 7.1):
  ML-KEM-512:  2×384 + 2×32 + 32 = 1,632 bytes  (d, z seed, pk hash)
  ML-KEM-768:  3×384 + 2×32 + 32 = 2,400 bytes
  ML-KEM-1024: 4×384 + 2×32 + 32 = 3,168 bytes

Shared secret: Always 32 bytes for all parameter sets — correct per FIPS 203.

⚠️  CURRENT STATUS: STUB IMPLEMENTATION
This provider uses placeholder cryptographic operations. It must NOT be used
in production. Replace with a real FIPS 203 implementation before deployment.

Correctness guarantee: The stub uses deterministic derivation
`shared_secret = SHA-256(seed || ciphertext)` for both encapsulate and
decapsulate, ensuring the KEM correctness invariant holds:
  decapsulate(ct, sk) == ss where (ct, ss) = encapsulate(pk)

TODO: Replace with liboqs-python (import oqs) or pqcrypto library.
      See: https://github.com/open-quantum-safe/liboqs-python
      See: https://csrc.nist.gov/pubs/fips/203/final
"""

import hashlib
import logging
import os
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

SHARED_SECRET_SIZE = 32  # FIPS 203: always 32 bytes for all parameter sets

STUB_WARNING = (
    "ML-KEM STUB: Not cryptographically valid. "
    "Replace with real FIPS 203 implementation (liboqs-python) before production use."
)


class MlKemParameterSet(Enum):
    """ML-KEM parameter sets per FIPS 203."""
    ML_KEM_512 = "ML-KEM-512"
    ML_KEM_768 = "ML-KEM-768"
    ML_KEM_1024 = "ML-KEM-1024"


# FIPS 203 exact sizes — private key sizes are actual FIPS 203 values, NOT publicKeySize * 2
_PARAM_SIZES = {
    MlKemParameterSet.ML_KEM_512: {
        "public_key_size": 800,
        "ciphertext_size": 768,
        "private_key_size": 1_632,  # FIPS 203: 2×384 + 2×32 + 32
        "nist_level": 1,
        "security_bits": 128,
    },
    MlKemParameterSet.ML_KEM_768: {
        "public_key_size": 1_184,
        "ciphertext_size": 1_088,
        "private_key_size": 2_400,  # FIPS 203: 3×384 + 2×32 + 32
        "nist_level": 3,
        "security_bits": 192,
    },
    MlKemParameterSet.ML_KEM_1024: {
        "public_key_size": 1_568,
        "ciphertext_size": 1_568,
        "private_key_size": 3_168,  # FIPS 203: 4×384 + 2×32 + 32
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


@dataclass
class EncapsulationResult:
    """Result of key encapsulation."""
    ciphertext: bytes
    shared_secret: bytes


class MlKemProvider:
    """
    ML-KEM (Kyber) key encapsulation mechanism.

    ⚠️  STUB: All cryptographic operations are placeholders.
    Callers MUST check `is_stub` before relying on key exchange security.

    Correctness: Uses deterministic derivation SHA-256(seed || ciphertext)
    for both encapsulate and decapsulate, ensuring the KEM correctness
    invariant holds even in stub mode.

    TODO: Replace internals with liboqs:
        import oqs
        kem = oqs.KeyEncapsulation("ML-KEM-768")
        public_key = kem.generate_keypair()
        ciphertext, shared_secret = kem.encapsulate(public_key)
        shared_secret_dec = kem.decapsulate(ciphertext)
    """

    def __init__(self, parameter_set: MlKemParameterSet = MlKemParameterSet.ML_KEM_768):
        self._param_set = parameter_set
        sizes = _PARAM_SIZES[parameter_set]
        self._public_key_size = sizes["public_key_size"]
        self._ciphertext_size = sizes["ciphertext_size"]
        self._private_key_size = sizes["private_key_size"]
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
    def ciphertext_size(self) -> int:
        return self._ciphertext_size

    @property
    def shared_secret_size(self) -> int:
        return SHARED_SECRET_SIZE

    @property
    def private_key_size(self) -> int:
        return self._private_key_size

    @property
    def is_post_quantum(self) -> bool:
        return True

    def generate_keypair(self) -> KeyPair:
        """
        Generate an ML-KEM key pair.

        STUB: Generates random bytes. Real ML-KEM key generation derives keys
        from a seed via FIPS 203 Algorithm 1 (ML-KEM.KeyGen).

        In the stub, the "seed" is stored as the first 32 bytes of the private key
        to enable deterministic decapsulation.

        TODO: Use liboqs `oqs.KeyEncapsulation("ML-KEM-768").generate_keypair()`
        """
        logger.warning("generate_keypair(): Using STUB random key generation")

        # Generate a deterministic seed for shared secret derivation
        seed = os.urandom(32)

        public_key = os.urandom(self._public_key_size)

        # Private key = seed || random_padding
        # The seed is used for deterministic decapsulation
        private_key = seed + os.urandom(self._private_key_size - 32)

        return KeyPair(
            public_key=public_key,
            private_key=private_key,
            algorithm=self.algorithm_name,
        )

    def encapsulate(self, public_key: bytes) -> EncapsulationResult:
        """
        Encapsulate a shared secret to a public key.

        STUB: Generates a random seed and derives:
          ciphertext = seed || random_bytes(ciphertextSize - 32)
          shared_secret = SHA-256(seed || ciphertext)

        The seed is embedded in the ciphertext so that decapsulation can
        recover it and derive the same shared secret.

        TODO: Use liboqs `kem.encapsulate(public_key)`
        """
        if len(public_key) != self._public_key_size:
            raise ValueError(
                f"Invalid public key size: {len(public_key)}, expected {self._public_key_size}"
            )

        logger.warning("encapsulate(): Using STUB encapsulation — NOT cryptographically valid")

        # Generate a random seed (simulates the KEM's internal randomness)
        seed = os.urandom(32)

        # Build ciphertext: seed_prefix || random_padding
        # The seed is embedded so decapsulation can recover it
        ciphertext = seed + os.urandom(self._ciphertext_size - 32)

        # Derive shared secret deterministically: SHA-256(seed || ciphertext)
        shared_secret = self._derive_shared_secret(seed, ciphertext)

        return EncapsulationResult(
            ciphertext=ciphertext,
            shared_secret=shared_secret,
        )

    def decapsulate(self, private_key: bytes, ciphertext: bytes) -> bytes:
        """
        Decapsulate a shared secret from a ciphertext using a private key.

        STUB: Extracts the seed from the ciphertext prefix (first 32 bytes)
        and derives:
          shared_secret = SHA-256(seed || ciphertext)

        This produces the SAME shared secret as encapsulate(), satisfying
        the KEM correctness invariant:
          decapsulate(ct, sk) == ss where (ct, ss) = encapsulate(pk)

        The previous stub used hashlib.sha256(private_key + ciphertext).digest()[:32]
        which produced a DIFFERENT shared secret than encapsulate, breaking the invariant.

        TODO: Use liboqs `kem.decapsulate(ciphertext)`
        """
        if len(private_key) != self._private_key_size:
            raise ValueError(
                f"Invalid private key size: {len(private_key)}, expected {self._private_key_size}"
            )
        if len(ciphertext) != self._ciphertext_size:
            raise ValueError(
                f"Invalid ciphertext size: {len(ciphertext)}, expected {self._ciphertext_size}"
            )

        logger.warning("decapsulate(): Using STUB decapsulation — NOT cryptographically valid")

        # Extract the seed from the ciphertext prefix (first 32 bytes)
        seed = ciphertext[:32]

        # Derive shared secret deterministically: SHA-256(seed || ciphertext)
        # This MUST match the derivation in encapsulate()
        return self._derive_shared_secret(seed, ciphertext)

    def _derive_shared_secret(self, seed: bytes, ciphertext: bytes) -> bytes:
        """
        Deterministic shared secret derivation.

        Both encapsulate and decapsulate use the same derivation:
          shared_secret = SHA-256(seed || ciphertext)[:32]

        This ensures the KEM correctness invariant holds even in stub mode.
        """
        h = hashlib.sha256()
        h.update(seed)
        h.update(ciphertext)
        return h.digest()[:SHARED_SECRET_SIZE]
