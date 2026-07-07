package com.msaidizi.app.core.ai

import android.app.Application
import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build
import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL

/**
 * ModelDownloader — Data-aware model downloading for Msaidizi.
 *
 * Valentine's vision: "Should work on data, not only on WiFi — as long as
 * they have enough data, the app downloads all dependencies and setup done
 * automatically."
 *
 * Key design principles:
 * 1. Works on MOBILE DATA — not just WiFi
 * 2. Auto-resume if interrupted (data ran out, phone call, etc.)
 * 3. Prioritize by importance: Whisper (voice) → Qwen (reasoning) → TTS (speech)
 * 4. Never show technical download screens — make it feel like Msaidizi is "getting ready"
 * 5. Show progress naturally: "Ninajifunza lugha yako..." (I'm learning your language...)
 *
 * Download requirements:
 * - Whisper model (~150MB) — speech recognition for her dialect
 * - Qwen 0.5B (~300MB) — on-device reasoning
 * - Piper TTS (~50MB) — voice output in her language
 * - Total: ~500MB
 *
 * Data optimization:
 * - Detect connection type (WiFi vs mobile)
 * - If mobile: check available data budget
 * - Use chunked downloads with resume support
 * - Compress models when possible
 * - Background download during onboarding conversation
 *
 * @author Angavu Intelligence — Implementation Swarm 9
 */
class ModelDownloader(private val application: Application) {

    companion object {
        private const val TAG = "ModelDownloader"
        private const val MODELS_DIR = "models"
        private const val DOWNLOAD_CHUNK_SIZE = 8192
        private const val MAX_RETRY_ATTEMPTS = 5
        private const val RETRY_DELAY_MS = 2000L
    }

    // ── Model Definitions ──────────────────────────────────────

    enum class ModelType(
        val fileName: String,
        val downloadUrl: String,
        val approximateSizeBytes: Long,
        val priority: Int  // Lower = higher priority
    ) {
        WISPER(
            fileName = "whisper-base-multilingual.bin",
            downloadUrl = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin",
            approximateSizeBytes = 150_000_000,  // ~150MB
            priority = 1  // Highest priority — voice input is critical
        ),
        QWEN_0_5B(
            fileName = "qwen-0.5b-q4_0.gguf",
            downloadUrl = "https://huggingface.co/Qwen/Qwen2-0.5B-Instruct-GGUF/resolve/main/qwen2-0_5b-instruct-q4_0.gguf",
            approximateSizeBytes = 300_000_000,  // ~300MB
            priority = 2  // Second priority — reasoning capability
        ),
        PIPER_TTS(
            fileName = "piper-swahili.onnx",
            downloadUrl = "https://huggingface.co/rhasspy/piper-voices/resolve/main/sw/sw-KE/medium/sw-KE-medium.onnx",
            approximateSizeBytes = 50_000_000,  // ~50MB
            priority = 3  // Third priority — voice output
        )
    }

    // ── State ──────────────────────────────────────────────────

    private val modelsDir: File by lazy {
        File(application.filesDir, MODELS_DIR).apply { mkdirs() }
    }

    private val prefs by lazy {
        application.getSharedPreferences("model_downloads", Context.MODE_PRIVATE)
    }

    // ── Public API ─────────────────────────────────────────────

    /**
     * Download a model with progress tracking and auto-resume.
     *
     * @param model The model to download
     * @param onProgress Progress callback (0.0 to 1.0)
     * @param allowMobileData Whether to download on mobile data
     */
    suspend fun downloadModel(
        model: ModelType,
        onProgress: (Float) -> Unit = {},
        allowMobileData: Boolean = true
    ) = withContext(Dispatchers.IO) {
        val modelFile = File(modelsDir, model.fileName)

        // Check if already downloaded
        if (isModelDownloaded(model)) {
            Log.d(TAG, "Model ${model.fileName} already downloaded")
            onProgress(1.0f)
            return@withContext
        }

        // Check connection type and data availability
        val connectionInfo = getConnectionInfo()
        if (!connectionInfo.isWifi && !allowMobileData) {
            Log.d(TAG, "On mobile data and mobile downloads not allowed")
            throw IllegalStateException("Mobile data downloads not allowed")
        }

        // Check available storage
        if (!hasEnoughStorage(model.approximateSizeBytes)) {
            throw IllegalStateException("Not enough storage for ${model.fileName}")
        }

        // Download with retry and resume
        downloadWithRetry(model, modelFile, onProgress)
    }

    /**
     * Check if a model is fully downloaded.
     */
    fun isModelDownloaded(model: ModelType): Boolean {
        val modelFile = File(modelsDir, model.fileName)
        return modelFile.exists() && modelFile.length() >= model.approximateSizeBytes * 0.95
    }

    /**
     * Get the path to a downloaded model.
     */
    fun getModelPath(model: ModelType): String? {
        val modelFile = File(modelsDir, model.fileName)
        return if (modelFile.exists()) modelFile.absolutePath else null
    }

    /**
     * Get total size of all downloaded models.
     */
    fun getTotalDownloadedSize(): Long {
        return modelsDir.listFiles()?.sumOf { it.length() } ?: 0L
    }

    /**
     * Get connection info for data-aware downloading.
     */
    fun getConnectionInfo(): ConnectionInfo {
        val cm = application.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            val network = cm.activeNetwork ?: return ConnectionInfo(false, false, 0L)
            val capabilities = cm.getNetworkCapabilities(network) ?: return ConnectionInfo(false, false, 0L)

            val isWifi = capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)
            val isCellular = capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)
            val linkProperties = cm.getLinkProperties(network)

            ConnectionInfo(
                isConnected = true,
                isWifi = isWifi,
                isMobileData = isCellular,
                estimatedBandwidth = capabilities.linkDownstreamBandwidthKbps.toLong()
            )
        } else {
            @Suppress("DEPRECATION")
            val networkInfo = cm.activeNetworkInfo
            ConnectionInfo(
                isConnected = networkInfo?.isConnected == true,
                isWifi = networkInfo?.type == ConnectivityManager.TYPE_WIFI,
                isMobileData = networkInfo?.type == ConnectivityManager.TYPE_MOBILE
            )
        }
    }

    /**
     * Estimate remaining data budget (if available).
     * Returns bytes available, or -1 if unknown.
     */
    fun estimateAvailableData(): Long {
        // This is a rough estimate — actual data tracking requires
        // carrier APIs which aren't universally available
        return -1L  // Unknown — we'll download anyway if allowed
    }

    // ── Private Implementation ─────────────────────────────────

    private suspend fun downloadWithRetry(
        model: ModelType,
        targetFile: File,
        onProgress: (Float) -> Unit
    ) {
        var attempts = 0
        var lastException: Exception? = null

        while (attempts < MAX_RETRY_ATTEMPTS) {
            try {
                downloadChunked(model, targetFile, onProgress)
                Log.d(TAG, "Successfully downloaded ${model.fileName}")
                return
            } catch (e: Exception) {
                lastException = e
                attempts++
                Log.w(TAG, "Download attempt $attempts failed for ${model.fileName}: ${e.message}")

                if (attempts < MAX_RETRY_ATTEMPTS) {
                    delay(RETRY_DELAY_MS * attempts)  // Exponential backoff
                }
            }
        }

        throw lastException ?: Exception("Download failed after $MAX_RETRY_ATTEMPTS attempts")
    }

    private suspend fun downloadChunked(
        model: ModelType,
        targetFile: File,
        onProgress: (Float) -> Unit
    ) = withContext(Dispatchers.IO) {
        val tempFile = File(modelsDir, "${model.fileName}.tmp")
        val resumeOffset = if (tempFile.exists()) tempFile.length() else 0L

        val url = URL(model.downloadUrl)
        val connection = url.openConnection() as HttpURLConnection

        try {
            // Set headers for resume support
            connection.setRequestProperty("User-Agent", "Msaidizi/1.0")
            if (resumeOffset > 0) {
                connection.setRequestProperty("Range", "bytes=$resumeOffset-")
                Log.d(TAG, "Resuming download from offset $resumeOffset")
            }

            connection.connectTimeout = 30000
            connection.readTimeout = 60000
            connection.connect()

            if (connection.responseCode !in 200..299 && connection.responseCode != 206) {
                throw Exception("HTTP ${connection.responseCode}: ${connection.responseMessage}")
            }

            val contentLength = connection.contentLength.toLong()
            val totalSize = resumeOffset + contentLength

            connection.inputStream.use { input ->
                FileOutputStream(tempFile, resumeOffset > 0).use { output ->
                    val buffer = ByteArray(DOWNLOAD_CHUNK_SIZE)
                    var bytesRead: Int
                    var totalRead = resumeOffset

                    while (input.read(buffer).also { bytesRead = it } != -1) {
                        output.write(buffer, 0, bytesRead)
                        totalRead += bytesRead

                        val progress = totalRead.toFloat() / totalSize
                        onProgress(progress.coerceIn(0f, 1f))

                        // Check if connection was lost
                        if (Thread.currentThread().isInterrupted) {
                            throw InterruptedException("Download interrupted")
                        }
                    }
                }
            }

            // Rename temp file to final file
            tempFile.renameTo(targetFile)
            Log.d(TAG, "Download complete: ${model.fileName} (${targetFile.length()} bytes)")

        } finally {
            connection.disconnect()
        }
    }

    private fun hasEnoughStorage(requiredBytes: Long): Boolean {
        val available = modelsDir.freeSpace
        return available > requiredBytes * 1.1  // 10% buffer
    }

    /**
     * Clean up incomplete downloads.
     */
    fun cleanupIncompleteDownloads() {
        modelsDir.listFiles()?.forEach { file ->
            if (file.name.endsWith(".tmp")) {
                file.delete()
                Log.d(TAG, "Cleaned up incomplete download: ${file.name}")
            }
        }
    }

    /**
     * Delete all downloaded models.
     */
    fun deleteAllModels() {
        modelsDir.listFiles()?.forEach { it.delete() }
        Log.d(TAG, "Deleted all models")
    }
}

// ── Connection Info ────────────────────────────────────────────

data class ConnectionInfo(
    val isConnected: Boolean,
    val isWifi: Boolean,
    val isMobileData: Boolean = false,
    val estimatedBandwidth: Long = 0L  // kbps
)
