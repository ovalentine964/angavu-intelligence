package com.msaidizi.app.security.crypto.pqc

import android.util.Log
import java.security.MessageDigest
import java.security.SecureRandom

/**
 * ML-KEM (Kyber) key encapsulation mechanism — NIST FIPS 203.
 *
 * Parameter sets per FIPS 203:
 * | Parameter Set  | NIST Level | Security Bits | Public Key | Ciphertext | Private Key |
 * |----------------|------------|---------------|------------|------------|-------------|
 * | ML-KEM-512     | Level 1    | 128           | 800 B      | 768 B      | 1,632 B     |
 * | ML-KEM-768     | Level 3    | 192           | 1,184 B    | 1,088 B    | 2,400 B     |
 * | ML-KEM-1024    | Level 5    | 256           | 1,568 B    | 1,568 B    | 3,168 B     |
 *
 * Private key sizes (FIPS 203, Section 7.1):
 *   ML-KEM-512:  2×384 + 2×32 + 32 = 1,632 bytes  (d, z seed, pk hash)
 *   ML-KEM-768:  3×384 + 2×32 + 32 = 2,400 bytes
 *   ML-KEM-1024: 4×384 + 2×32 + 32 = 3,168 bytes
 *
 * Shared secret: Always 32 bytes for all parameter sets — correct per FIPS 203.
 *
 * ⚠️  CURRENT STATUS: STUB IMPLEMENTATION
 * This provider uses placeholder cryptographic operations. It must NOT be used
 * in production. Replace with a real FIPS 203 implementation before deployment.
 *
 * Correctness guarantee: The stub uses deterministic derivation
 * `shared_secret = SHA-256(seed || ciphertext)` for both encapsulate and
 * decapsulate, ensuring the KEM correctness invariant holds:
 *   decapsulate(ct, sk) == ss where (ct, ss) = encapsulate(pk)
 *
 * TODO: Replace with Bouncy Castle PQC (org.bouncycastle.pqc.jcajce.provider.MLKEM)
 *       or Android Keystore with PQC support (Android 15+).
 *       See: https://www.bouncycastle.org/java.html
 *       See: https://csrc.nist.gov/pubs/fips/203/final
 */
class MlKemProvider(
    private val parameterSet: MlKemParameterSet = MlKemParameterSet.ML_KEM_768
) : KeyEncapsulationProvider {

    companion object {
        private const val TAG = "MlKemProvider"
        private const val SHARED_SECRET_SIZE = 32 // FIPS 203: always 32 bytes
        private const val STUB_WARNING = "ML-KEM STUB: Not cryptographically valid. " +
            "Replace with real FIPS 203 implementation (Bouncy Castle PQC) before production use."
    }

    /**
     * Flag indicating this is a stub implementation.
     * Callers MUST check this before relying on key exchange security.
     */
    val isStub: Boolean = true

    override val algorithmName: String = parameterSet.name

    override val publicKeySize: Int = parameterSet.publicKeySize
    override val ciphertextSize: Int = parameterSet.ciphertextSize
    override val sharedSecretSize: Int = SHARED_SECRET_SIZE
    override val privateKeySize: Int = parameterSet.privateKeySize

    override val isPostQuantum: Boolean = true

    private val secureRandom = SecureRandom()

    init {
        Log.w(TAG, STUB_WARNING)
    }

    /**
     * Generate an ML-KEM key pair.
     *
     * STUB: Generates random bytes. Real ML-KEM key generation derives keys
     * from a seed via FIPS 203 Algorithm 1 (ML-KEM.KeyGen).
     *
     * In the stub, the "seed" is stored as the first 32 bytes of the private key
     * to enable deterministic decapsulation.
     *
     * TODO: Use Bouncy Castle `MLKEMKeyPairGenerator` or equivalent.
     */
    override fun generateKeyPair(): KeyPair {
        Log.w(TAG, "generateKeyPair(): Using STUB random key generation")

        // Generate a deterministic seed for shared secret derivation
        val seed = ByteArray(32).also { secureRandom.nextBytes(it) }

        val publicKey = ByteArray(publicKeySize).also { secureRandom.nextBytes(it) }

        // Private key = seed || random_padding
        // The seed is used for deterministic decapsulation
        val privateKey = ByteArray(privateKeySize)
        seed.copyInto(privateKey)
        secureRandom.nextBytes(privateKey, 32, privateKeySize)

        return KeyPair(
            publicKey = publicKey,
            privateKey = privateKey,
            algorithm = algorithmName
        )
    }

    /**
     * Encapsulate a shared secret to a public key.
     *
     * STUB: Generates a random seed and derives:
     *   ciphertext = random_bytes(ciphertextSize)
     *   shared_secret = SHA-256(seed || ciphertext)
     *
     * The seed is embedded in the ciphertext so that decapsulation can
     * recover it and derive the same shared secret.
     *
     * TODO: Use Bouncy Castle `MLKEMEncapsulator` or equivalent.
     */
    override fun encapsulate(publicKey: ByteArray): EncapsulationResult {
        require(publicKey.size == publicKeySize) {
            "Invalid public key size: ${publicKey.size}, expected $publicKeySize"
        }

        Log.w(TAG, "encapsulate(): Using STUB encapsulation — NOT cryptographically valid")

        // Generate a random seed (simulates the KEM's internal randomness)
        val seed = ByteArray(32).also { secureRandom.nextBytes(it) }

        // Build ciphertext: seed_prefix || random_padding
        // The seed is embedded so decapsulation can recover it
        val ciphertext = ByteArray(ciphertextSize)
        seed.copyInto(ciphertext) // First 32 bytes = seed
        secureRandom.nextBytes(ciphertext, 32, ciphertextSize) // Rest = random

        // Derive shared secret deterministically: SHA-256(seed || ciphertext)
        val sharedSecret = deriveSharedSecret(seed, ciphertext)

        return EncapsulationResult(
            ciphertext = ciphertext,
            sharedSecret = sharedSecret
        )
    }

    /**
     * Decapsulate a shared secret from a ciphertext using a private key.
     *
     * STUB: Extracts the seed from the ciphertext prefix (first 32 bytes)
     * and derives:
     *   shared_secret = SHA-256(seed || ciphertext)
     *
     * This produces the SAME shared secret as encapsulate(), satisfying
     * the KEM correctness invariant:
     *   decapsulate(ct, sk) == ss where (ct, ss) = encapsulate(pk)
     *
     * The previous stub used SHA-256(privateKey || ciphertext) which produced
     * a DIFFERENT shared secret than encapsulate, breaking the invariant.
     *
     * TODO: Use Bouncy Castle `MLKEMDecapsulator` or equivalent.
     */
    override fun decapsulate(privateKey: ByteArray, ciphertext: ByteArray): ByteArray {
        require(privateKey.size == privateKeySize) {
            "Invalid private key size: ${privateKey.size}, expected $privateKeySize"
        }
        require(ciphertext.size == ciphertextSize) {
            "Invalid ciphertext size: ${ciphertext.size}, expected $ciphertextSize"
        }

        Log.w(TAG, "decapsulate(): Using STUB decapsulation — NOT cryptographically valid")

        // Extract the seed from the ciphertext prefix (first 32 bytes)
        val seed = ciphertext.copyOfRange(0, 32)

        // Derive shared secret deterministically: SHA-256(seed || ciphertext)
        // This MUST match the derivation in encapsulate()
        return deriveSharedSecret(seed, ciphertext)
    }

    /**
     * Deterministic shared secret derivation.
     *
     * Both encapsulate and decapsulate use the same derivation:
     *   shared_secret = SHA-256(seed || ciphertext)[:32]
     *
     * This ensures the KEM correctness invariant holds even in stub mode.
     */
    private fun deriveSharedSecret(seed: ByteArray, ciphertext: ByteArray): ByteArray {
        val digest = MessageDigest.getInstance("SHA-256")
        digest.update(seed)
        digest.update(ciphertext)
        return digest.digest() // 32 bytes, matches SHARED_SECRET_SIZE
    }
}

/**
 * ML-KEM parameter sets per FIPS 203.
 *
 * Private key sizes are actual FIPS 203 values:
 * - ML-KEM-512:  1,632 bytes  (2×384 + 2×32 + 32)
 * - ML-KEM-768:  2,400 bytes  (3×384 + 2×32 + 32)
 * - ML-KEM-1024: 3,168 bytes  (4×384 + 2×32 + 32)
 *
 * Previous approximation used `publicKeySize * 2` which is incorrect.
 */
enum class MlKemParameterSet(
    val publicKeySize: Int,
    val ciphertextSize: Int,
    val privateKeySize: Int,
    val nistLevel: Int,
    val securityBits: Int
) {
    ML_KEM_512(
        publicKeySize = 800,
        ciphertextSize = 768,
        privateKeySize = 1_632,  // FIPS 203: 2×384 + 2×32 + 32
        nistLevel = 1,
        securityBits = 128
    ),
    ML_KEM_768(
        publicKeySize = 1_184,
        ciphertextSize = 1_088,
        privateKeySize = 2_400,  // FIPS 203: 3×384 + 2×32 + 32
        nistLevel = 3,
        securityBits = 192
    ),
    ML_KEM_1024(
        publicKeySize = 1_568,
        ciphertextSize = 1_568,
        privateKeySize = 3_168,  // FIPS 203: 4×384 + 2×32 + 32
        nistLevel = 5,
        securityBits = 256
    )
}

/**
 * Interface for key encapsulation mechanisms (ML-KEM, etc.)
 *
 * Separated from CryptoProvider because KEMs don't do direct encrypt/decrypt.
 */
interface KeyEncapsulationProvider {
    val algorithmName: String
    val publicKeySize: Int
    val ciphertextSize: Int
    val sharedSecretSize: Int
    val privateKeySize: Int
    val isPostQuantum: Boolean

    fun generateKeyPair(): KeyPair
    fun encapsulate(publicKey: ByteArray): EncapsulationResult
    fun decapsulate(privateKey: ByteArray, ciphertext: ByteArray): ByteArray
}

/**
 * Result of key encapsulation.
 */
data class EncapsulationResult(
    val ciphertext: ByteArray,
    val sharedSecret: ByteArray
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is EncapsulationResult) return false
        return ciphertext.contentEquals(other.ciphertext) &&
            sharedSecret.contentEquals(other.sharedSecret)
    }

    override fun hashCode(): Int {
        var result = ciphertext.contentHashCode()
        result = 31 * result + sharedSecret.contentHashCode()
        return result
    }
}
