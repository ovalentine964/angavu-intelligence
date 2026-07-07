package com.msaidizi.app.security.crypto.pqc

import android.util.Log
import java.security.MessageDigest
import java.security.SecureRandom

/**
 * ML-DSA (Dilithium) signature provider — NIST FIPS 204.
 *
 * Parameter sets per FIPS 204:
 * | Parameter Set  | NIST Level | Public Key | Private Key | Max Signature |
 * |----------------|------------|------------|-------------|---------------|
 * | ML-DSA-44      | Level 2    | 1,312 B    | 2,560 B     | 2,420 B       |
 * | ML-DSA-65      | Level 3    | 1,952 B    | 4,032 B     | 3,293 B       |
 * | ML-DSA-87      | Level 5    | 2,592 B    | 4,896 B     | 4,595 B       |
 *
 * ⚠️  CURRENT STATUS: STUB IMPLEMENTATION
 * This provider uses placeholder cryptographic operations. It must NOT be used
 * in production. Replace with a real FIPS 204 implementation before deployment.
 *
 * TODO: Replace with Bouncy Castle PQC (org.bouncycastle.pqc.jcajce.provider.MLDSA)
 *       or Android Keystore with PQC support (Android 15+).
 *       See: https://www.bouncycastle.org/java.html
 *       See: https://csrc.nist.gov/pubs/fips/204/final
 */
class MlDsaProvider(
    private val parameterSet: MlDsaParameterSet = MlDsaParameterSet.ML_DSA_65
) : SignatureProvider {

    companion object {
        private const val TAG = "MlDsaProvider"
        private const val STUB_WARNING = "ML-DSA STUB: Not cryptographically valid. " +
            "Replace with real FIPS 204 implementation (Bouncy Castle PQC) before production use."
    }

    /**
     * Flag indicating this is a stub implementation.
     * Callers MUST check this before relying on signature verification results.
     */
    val isStub: Boolean = true

    override val algorithmName: String = parameterSet.name

    override val publicKeySize: Int = parameterSet.publicKeySize
    override val privateKeySize: Int = parameterSet.privateKeySize
    override val maxSignatureSize: Int = parameterSet.maxSignatureSize

    override val isPostQuantum: Boolean = true

    private val secureRandom = SecureRandom()

    init {
        Log.w(TAG, STUB_WARNING)
    }

    /**
     * Generate an ML-DSA key pair.
     *
     * STUB: Generates random bytes. Real ML-DSA key generation derives keys
     * from a seed via FIPS 204 Algorithm 1 (ML-DSA.KeyGen).
     *
     * TODO: Use Bouncy Castle `MLDSAKeyPairGenerator` or equivalent.
     */
    override fun generateKeyPair(): KeyPair {
        Log.w(TAG, "generateKeyPair(): Using STUB random key generation")

        val publicKey = ByteArray(publicKeySize).also { secureRandom.nextBytes(it) }
        val privateKey = ByteArray(privateKeySize).also { secureRandom.nextBytes(it) }

        return KeyPair(
            publicKey = publicKey,
            privateKey = privateKey,
            algorithm = algorithmName
        )
    }

    /**
     * Sign data with an ML-DSA private key.
     *
     * STUB: Uses SHA-512(privateKey || data) as a placeholder.
     * Real ML-DSA uses hedged signing with a random seed derived from
     * H(random || msg || pk) per FIPS 204 Algorithm 2 (ML-DSA.Sign).
     *
     * The output is padded to maxSignatureSize. Real ML-DSA signatures are
     * variable-length (≤ maxSignatureSize).
     *
     * TODO: Use Bouncy Castle `MLDSASigner` or equivalent.
     */
    override fun sign(privateKey: ByteArray, data: ByteArray): ByteArray {
        require(privateKey.size == privateKeySize) {
            "Invalid private key size: ${privateKey.size}, expected $privateKeySize"
        }
        require(data.isNotEmpty()) { "Data to sign must not be empty" }

        Log.w(TAG, "sign(): Using STUB signature generation — NOT cryptographically valid")

        val digest = MessageDigest.getInstance("SHA-512")
        digest.update(privateKey)
        digest.update(data)
        val hash = digest.digest()

        // Pad to maxSignatureSize (real ML-DSA signatures are variable-length ≤ max)
        return ByteArray(maxSignatureSize).also { sig ->
            hash.copyInto(sig)
            // Fill remaining with deterministic derivation (not random) for reproducibility
            val padDigest = MessageDigest.getInstance("SHA-256")
            padDigest.update(hash)
            val pad = padDigest.digest()
            var offset = hash.size
            while (offset < maxSignatureSize) {
                val copyLen = minOf(pad.size, maxSignatureSize - offset)
                pad.copyInto(sig, offset, 0, copyLen)
                offset += copyLen
            }
        }
    }

    /**
     * Verify an ML-DSA signature.
     *
     * ⚠️  STUB: Performs basic structural validation but cannot verify
     * cryptographic correctness. Returns true only if inputs pass
     * structural checks.
     *
     * This is intentionally NOT always-true. The previous stub returned
     * true unconditionally, which is a critical security flaw — it would
     * accept forged signatures. This version at least validates:
     *   1. Public key size matches the parameter set
     *   2. Signature size is within valid range (1..maxSignatureSize)
     *   3. Data is non-empty
     *
     * TODO: Replace with Bouncy Castle `MLDSASigner.verifySignature()` or equivalent.
     * TODO: Add NIST ACVP Known Answer Test (KAT) vectors for validation.
     *
     * @return true only if structural validation passes AND stub mode is active.
     *         In non-stub mode, this must perform real FIPS 204 verification.
     */
    override fun verify(publicKey: ByteArray, data: ByteArray, signature: ByteArray): Boolean {
        // --- Structural validation (always performed, even in stub mode) ---

        if (publicKey.size != publicKeySize) {
            Log.e(TAG, "verify(): REJECTED — invalid public key size: ${publicKey.size}, expected $publicKeySize")
            return false
        }

        if (signature.isEmpty() || signature.size > maxSignatureSize) {
            Log.e(TAG, "verify(): REJECTED — invalid signature size: ${signature.size}, must be 1..$maxSignatureSize")
            return false
        }

        if (data.isEmpty()) {
            Log.e(TAG, "verify(): REJECTED — data must not be empty")
            return false
        }

        // --- STUB: Cannot perform real cryptographic verification ---
        Log.w(TAG, "verify(): STUB — structural validation passed, but cryptographic verification " +
            "is NOT performed. This result is unreliable. Replace with real FIPS 204 implementation.")

        return true
    }

    override fun encrypt(publicKey: ByteArray, data: ByteArray): ByteArray {
        throw UnsupportedOperationException(
            "ML-DSA is a signature algorithm, not an encryption algorithm. " +
            "Use ML-KEM + AES-256-GCM for encryption."
        )
    }

    override fun decrypt(privateKey: ByteArray, data: ByteArray): ByteArray {
        throw UnsupportedOperationException(
            "ML-DSA is a signature algorithm, not an encryption algorithm. " +
            "Use ML-KEM + AES-256-GCM for decryption."
        )
    }
}

/**
 * ML-DSA parameter sets per FIPS 204.
 */
enum class MlDsaParameterSet(
    val publicKeySize: Int,
    val privateKeySize: Int,
    val maxSignatureSize: Int,
    val nistLevel: Int,
    val securityBits: Int
) {
    ML_DSA_44(
        publicKeySize = 1_312,
        privateKeySize = 2_560,
        maxSignatureSize = 2_420,
        nistLevel = 2,
        securityBits = 128
    ),
    ML_DSA_65(
        publicKeySize = 1_952,
        privateKeySize = 4_032,
        maxSignatureSize = 3_293,
        nistLevel = 3,
        securityBits = 192
    ),
    ML_DSA_87(
        publicKeySize = 2_592,
        privateKeySize = 4_896,
        maxSignatureSize = 4_595,
        nistLevel = 5,
        securityBits = 256
    )
}

/**
 * Interface for signature providers (ML-DSA, ECDSA, etc.)
 */
interface SignatureProvider {
    val algorithmName: String
    val publicKeySize: Int
    val privateKeySize: Int
    val maxSignatureSize: Int
    val isPostQuantum: Boolean

    fun generateKeyPair(): KeyPair
    fun sign(privateKey: ByteArray, data: ByteArray): ByteArray
    fun verify(publicKey: ByteArray, data: ByteArray, signature: ByteArray): Boolean
    fun encrypt(publicKey: ByteArray, data: ByteArray): ByteArray
    fun decrypt(privateKey: ByteArray, data: ByteArray): ByteArray
}

/**
 * Simple key pair container.
 */
data class KeyPair(
    val publicKey: ByteArray,
    val privateKey: ByteArray,
    val algorithm: String
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is KeyPair) return false
        return algorithm == other.algorithm &&
            publicKey.contentEquals(other.publicKey) &&
            privateKey.contentEquals(other.privateKey)
    }

    override fun hashCode(): Int {
        var result = algorithm.hashCode()
        result = 31 * result + publicKey.contentHashCode()
        result = 31 * result + privateKey.contentHashCode()
        return result
    }
}
