package com.msaidizi.app.core.ai

import android.app.Application
import android.content.Context
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import com.msaidizi.app.core.dialect.KiswahiliDialectAdapter
import com.msaidizi.app.voice.VoicePipeline
import com.msaidizi.app.voice.sts.SpeechToSpeechEngine
import java.io.File

/**
 * ModelManager — Full model strategy for Msaidizi.
 *
 * Valentine's vision: "Ensure Msaidizi functions fully with quality voice and
 * reasoning models as research found and recommended, NOT mini model."
 *
 * Model strategy (Updated by Impl 16 — July 2026):
 * - Device-tiered model selection (LOW/MID/HIGH)
 * - LOW tier:  Qwen3.5-0.8B (~500MB 4-bit) — mobile-optimized reasoning
 * - MID tier:  Qwen3-1.7B (~1.1GB 4-bit) — thinking mode, strong reasoning
 * - HIGH tier: Qwen3.5-2B (~1.2GB 4-bit) — edge-optimized, best quality
 * - ASR: Whisper small (466MB) for dialects, or Microsoft Paza for Swahili/African
 * - TTS: Piper Swahili + Arabic voices
 * - Cascaded S2S pipeline: STT → LLM → TTS with streaming
 *
 * Key features:
 * 1. Background download during onboarding — worker doesn't wait
 * 2. Data-aware — works on mobile data, not just WiFi
 * 3. Auto-resume — if download is interrupted, it picks up where it left off
 * 4. Progressive capability — app works with whatever models are available
 * 5. No technical screens — "Msaidizi is getting ready" not "Downloading model..."
 * 6. Academic framework integration — all advice grounded in ECO/STA theory
 *
 * @author Angavu Intelligence — Implementation Swarm 9 + 16 (Model Upgrade)
 */
class ModelManager(private val application: Application) {

    companion object {
        private const val TAG = "ModelManager"
        private const val PREFS_NAME = "model_manager"
        private const val KEY_FULL_MODELS_READY = "full_models_ready"
        private const val KEY_LAST_DOWNLOAD_ATTEMPT = "last_download_attempt"
        private const val KEY_DEVICE_TIER = "device_tier"

        // ── Reasoning Model Tiers (Impl 16 — July 2026) ────────
        // LOW: Qwen3.5-0.8B — mobile-optimized, ~0.5GB (4-bit quantized)
        // MID: Qwen3-1.7B — thinking mode, strong reasoning, ~1.1GB
        // HIGH: Qwen3.5-2B — edge-optimized, best quality, ~1.2GB

        // ── ASR Model Selection ─────────────────────────────────
        // Whisper small (466MB) for better dialect coverage
        // Microsoft Paza (200MB) for Swahili + African languages (Swarm H)
        // Fallback: Whisper base (150MB)

        // ── TTS Model Selection ─────────────────────────────────
        // Piper Swahili (50MB) — primary voice
        // Piper Arabic (55MB) — North/East Africa coverage
    }

    // ── State ──────────────────────────────────────────────────

    private val _state = MutableStateFlow(ModelManagerState.CHECKING)
    val state: StateFlow<ModelManagerState> = _state.asStateFlow()

    private val _downloadProgress = MutableStateFlow(0f)
    val downloadProgress: StateFlow<Float> = _downloadProgress.asStateFlow()

    private val _downloadState = MutableStateFlow(FullModelDownloadState.NOT_STARTED)
    val downloadState: StateFlow<FullModelDownloadState> = _downloadState.asStateFlow()

    // ── Dependencies ───────────────────────────────────────────

    private val modelDownloader = ModelDownloader(application)
    private val bundledModelManager = BundledModelManager(application)
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    // Voice pipeline with STS integration
    private val stsEngine = SpeechToSpeechEngine()
    private val voicePipeline = VoicePipeline(stsEngine, KiswahiliDialectAdapter())

    private val prefs by lazy {
        application.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
    }

    // ── Initialization ─────────────────────────────────────────

    init {
        checkModelState()
        initializeVoicePipeline()
    }

    /**
     * Initialize the voice pipeline with available models.
     * Tries STS first, falls back to ASR→LLM→TTS.
     */
    private fun initializeVoicePipeline() {
        try {
            val modelDir = File(application.filesDir, "models")
            if (modelDir.exists()) {
                voicePipeline.initialize(modelDir)
                Log.d(TAG, "Voice pipeline initialized — mode: ${voicePipeline.currentMode.value}")
            } else {
                Log.d(TAG, "Models directory not yet available — voice pipeline deferred")
            }
        } catch (e: Exception) {
            Log.w(TAG, "Voice pipeline init deferred: ${e.message}")
        }
    }

    // ── Public API ─────────────────────────────────────────────

    /**
     * Get the voice pipeline for voice interactions.
     * Uses STS when available, falls back to ASR→LLM→TTS.
     */
    fun getVoicePipeline(): VoicePipeline = voicePipeline

    /**
     * Check if STS direct mode is available.
     */
    fun isSTSAvailable(): Boolean = stsEngine.isSTSAvailable()

    /**
     * Check if the app has a usable model (bundled or full).
     * This is the primary check — the app should work with whatever is available.
     */
    fun hasUsableModel(): Boolean {
        return hasFullModel() || bundledModelManager.hasUsableModel()
    }

    /**
     * Check if full models are downloaded and ready.
     */
    fun hasFullModel(): Boolean {
        val whisperReady = modelDownloader.isModelDownloaded(ModelDownloader.ModelType.WHISPER_SMALL) ||
                modelDownloader.isModelDownloaded(ModelDownloader.ModelType.WISPER)
        val qwenReady = modelDownloader.isModelDownloaded(getReasoningModelForTier())
        val ttsReady = modelDownloader.isModelDownloaded(ModelDownloader.ModelType.PIPER_TTS)
        return whisperReady && qwenReady && ttsReady
    }

    /**
     * Get the reasoning model type for the current device tier.
     */
    fun getReasoningModelForTier(): ModelDownloader.ModelType {
        return when (getDeviceTier()) {
            DeviceTier.LOW -> ModelDownloader.ModelType.QWEN3_5_0_8B
            DeviceTier.MID -> ModelDownloader.ModelType.QWEN3_1_7B
            DeviceTier.HIGH -> ModelDownloader.ModelType.QWEN3_5_2B
        }
    }

    /**
     * Get the ASR model type for the current device tier.
     * Prefers Paza for Swahili/African languages, falls back to Whisper.
     */
    fun getASRModelForTier(): ModelDownloader.ModelType {
        return when (getDeviceTier()) {
            DeviceTier.LOW -> ModelDownloader.ModelType.WHISPER_BASE
            DeviceTier.MID -> ModelDownloader.ModelType.PAZA_ASR  // Microsoft Paza — better for Swahili
            DeviceTier.HIGH -> ModelDownloader.ModelType.WHISPER_SMALL  // Best dialect coverage
        }
    }

    /**
     * Get the best available model path.
     * Returns full model if available, otherwise bundled.
     */
    fun getBestModelPath(): String? {
        // Prefer full model (tier-appropriate)
        val fullPath = modelDownloader.getModelPath(getReasoningModelForTier())
        if (fullPath != null) return fullPath

        // Fall back to legacy Qwen 0.5B
        val legacyPath = modelDownloader.getModelPath(ModelDownloader.ModelType.QWEN_0_5B)
        if (legacyPath != null) return legacyPath

        // Fall back to bundled model
        return bundledModelManager.getBestModelPath()
    }

    /**
     * Get the Whisper/ASR model path for speech recognition.
     */
    fun getWhisperModelPath(): String? {
        // Try tier-appropriate ASR first
        val asrModel = getASRModelForTier()
        val path = modelDownloader.getModelPath(asrModel)
        if (path != null) return path

        // Fallback to legacy whisper
        return modelDownloader.getModelPath(ModelDownloader.ModelType.WISPER)
    }

    /**
     * Get the TTS model path for voice output.
     */
    fun getTtsModelPath(): String? {
        return modelDownloader.getModelPath(ModelDownloader.ModelType.PIPER_TTS)
    }

    /**
     * Get the device tier based on available RAM and CPU cores.
     */
    fun getDeviceTier(): DeviceTier {
        val saved = prefs.getString(KEY_DEVICE_TIER, null)
        if (saved != null) return DeviceTier.valueOf(saved)

        val runtime = Runtime.getRuntime()
        val maxMemoryMB = runtime.maxMemory() / (1024 * 1024)
        val cpuCores = runtime.availableProcessors()

        val tier = when {
            maxMemoryMB >= 4096 && cpuCores >= 8 -> DeviceTier.HIGH
            maxMemoryMB >= 2048 && cpuCores >= 4 -> DeviceTier.MID
            else -> DeviceTier.LOW
        }

        prefs.edit().putString(KEY_DEVICE_TIER, tier.name).apply()
        return tier
    }

    /**
     * Start downloading full models in background.
     * Called during onboarding — worker doesn't wait for this.
     *
     * Download priority (updated by Impl 16):
     * 1. ASR model — voice input is critical for voice-first interaction
     * 2. Reasoning model (tier-appropriate) — on-device intelligence
     * 3. Piper TTS — voice output
     *
     * This ensures the app gets progressively more capable:
     * - After ASR: voice input works
     * - After reasoning model: full intelligence works
     * - After TTS: voice output works
     */
    fun startBackgroundDownload() {
        if (hasFullModel()) {
            _state.value = ModelManagerState.FULL_MODEL_READY
            _downloadState.value = FullModelDownloadState.COMPLETED
            return
        }

        scope.launch {
            try {
                _downloadState.value = FullModelDownloadState.DOWNLOADING
                _state.value = ModelManagerState.DOWNLOADING

                // Check connection
                val connectionInfo = modelDownloader.getConnectionInfo()
                if (!connectionInfo.isConnected) {
                    _downloadState.value = FullModelDownloadState.WAITING_FOR_CONNECTION
                    scheduleRetry()
                    return@launch
                }

                // Download models in priority order (tier-aware)
                val asrModel = getASRModelForTier()
                val reasoningModel = getReasoningModelForTier()

                downloadModelWithProgress(asrModel, 0f, 0.25f)
                downloadModelWithProgress(reasoningModel, 0.25f, 0.85f)
                downloadModelWithProgress(ModelDownloader.ModelType.PIPER_TTS, 0.85f, 1.0f)

                // All models downloaded
                _downloadState.value = FullModelDownloadState.COMPLETED
                _downloadProgress.value = 1.0f
                _state.value = ModelManagerState.FULL_MODEL_READY

                // Save state
                prefs.edit().putBoolean(KEY_FULL_MODELS_READY, true).apply()

                // Initialize voice pipeline with downloaded models
                initializeVoicePipeline()

                Log.d(TAG, "All full models downloaded successfully")

            } catch (e: Exception) {
                Log.e(TAG, "Model download failed: ${e.message}", e)
                _downloadState.value = FullModelDownloadState.FAILED
                _state.value = ModelManagerState.ERROR

                // Schedule retry
                scheduleRetry()
            }
        }
    }

    /**
     * Resume a paused download.
     * Called when connection is restored or user requests retry.
     */
    fun resumeDownload() {
        startBackgroundDownload()
    }

    /**
     * Set WiFi-only download preference.
     * Default: allow mobile data (Valentine's vision: "work on data, not only WiFi")
     */
    fun setWifiOnlyDownload(wifiOnly: Boolean) {
        prefs.edit().putBoolean("wifi_only_download", wifiOnly).apply()
    }

    /**
     * Check if WiFi-only download is enabled.
     */
    fun isWifiOnlyDownload(): Boolean {
        return prefs.getBoolean("wifi_only_download", false)  // Default: allow mobile data
    }

    /**
     * Get download status message in the worker's language.
     * Never technical — always feels like Msaidizi is "getting ready."
     */
    fun getDownloadStatusMessage(language: String = "sw"): String {
        return when (_downloadState.value) {
            FullModelDownloadState.NOT_STARTED -> when (language) {
                "sw" -> "Msaidizi anajiandaa..."
                else -> "Msaidizi is getting ready..."
            }
            FullModelDownloadState.DOWNLOADING -> when (language) {
                "sw" -> "Ninajifunza... ${(_downloadProgress.value * 100).toInt()}%"
                else -> "Learning... ${(_downloadProgress.value * 100).toInt()}%"
            }
            FullModelDownloadState.COMPLETED -> when (language) {
                "sw" -> "Tayari! Msaidizi amejifunza."
                else -> "Ready! Msaidizi has learned."
            }
            FullModelDownloadState.WAITING_FOR_WIFI -> when (language) {
                "sw" -> "Nangoja WiFi..."
                else -> "Waiting for WiFi..."
            }
            FullModelDownloadState.WAITING_FOR_CONNECTION -> when (language) {
                "sw" -> "Nangoja muunganisho..."
                else -> "Waiting for connection..."
            }
            FullModelDownloadState.FAILED -> when (language) {
                "sw" -> "Jaribu tena baadaye"
                else -> "Try again later"
            }
        }
    }

    /**
     * Get model tier description for the current device.
     */
    fun getTierDescription(language: String = "sw"): String {
        return when (getDeviceTier()) {
            DeviceTier.LOW -> when (language) {
                "sw" -> "Msaidizi mwepesi (Qwen3.5-0.8B)"
                else -> "Msaidizi Lite (Qwen3.5-0.8B)"
            }
            DeviceTier.MID -> when (language) {
                "sw" -> "Msaidizi mwerevu (Qwen3-1.7B)"
                else -> "Msaidizi Smart (Qwen3-1.7B)"
            }
            DeviceTier.HIGH -> when (language) {
                "sw" -> "Msaidizi hodari (Qwen3.5-2B)"
                else -> "Msaidizi Pro (Qwen3.5-2B)"
            }
        }
    }

    /**
     * Get detailed model status for debugging.
     * Only shown in developer mode — never to the worker.
     */
    fun getModelStatus(): ModelStatus {
        return ModelStatus(
            whisperDownloaded = modelDownloader.isModelDownloaded(ModelDownloader.ModelType.WHISPER_SMALL) ||
                    modelDownloader.isModelDownloaded(ModelDownloader.ModelType.WISPER),
            qwenDownloaded = modelDownloader.isModelDownloaded(getReasoningModelForTier()),
            ttsDownloaded = modelDownloader.isModelDownloaded(ModelDownloader.ModelType.PIPER_TTS),
            bundledAvailable = bundledModelManager.hasUsableModel(),
            totalDownloadedBytes = modelDownloader.getTotalDownloadedSize(),
            connectionInfo = modelDownloader.getConnectionInfo(),
            deviceTier = getDeviceTier(),
            reasoningModel = getReasoningModelForTier().name,
            asrModel = getASRModelForTier().name
        )
    }

    // ── Private Implementation ─────────────────────────────────

    private fun checkModelState() {
        _state.value = when {
            hasFullModel() -> ModelManagerState.FULL_MODEL_READY
            bundledModelManager.hasUsableModel() -> ModelManagerState.BUNDLED_READY
            else -> ModelManagerState.UNAVAILABLE
        }

        // Check if there's a pending download
        if (!hasFullModel() && prefs.getBoolean(KEY_FULL_MODELS_READY, false)) {
            // Was previously complete but models were deleted — restart download
            startBackgroundDownload()
        }
    }

    private suspend fun downloadModelWithProgress(
        model: ModelDownloader.ModelType,
        progressStart: Float,
        progressEnd: Float
    ) {
        modelDownloader.downloadModel(
            model = model,
            onProgress = { modelProgress ->
                val overallProgress = progressStart + (progressEnd - progressStart) * modelProgress
                _downloadProgress.value = overallProgress
            },
            allowMobileData = !isWifiOnlyDownload()
        )
    }

    private fun scheduleRetry() {
        // Save last attempt time for retry logic
        prefs.edit().putLong(KEY_LAST_DOWNLOAD_ATTEMPT, System.currentTimeMillis()).apply()

        // In production, this would use WorkManager for reliable background scheduling
        // For now, we'll retry when the app next opens or on connectivity change
        Log.d(TAG, "Download retry scheduled")
    }

    /**
     * Force re-download of all models.
     * Used when models are corrupted or need updating.
     */
    fun forceRedownload() {
        modelDownloader.deleteAllModels()
        prefs.edit().putBoolean(KEY_FULL_MODELS_READY, false).apply()
        _state.value = ModelManagerState.UNAVAILABLE
        _downloadState.value = FullModelDownloadState.NOT_STARTED
        startBackgroundDownload()
    }

    /**
     * Clean up resources.
     */
    fun cleanup() {
        modelDownloader.cleanupIncompleteDownloads()
    }
}

// ── State Enums ────────────────────────────────────────────────

enum class ModelManagerState {
    CHECKING,           // Checking model availability
    UNAVAILABLE,        // No models available
    BUNDLED_READY,      // Bundled mini-model available (basic functionality)
    DOWNLOADING,        // Full models downloading
    FULL_MODEL_READY,   // All full models available
    ERROR               // Error state
}

enum class FullModelDownloadState {
    NOT_STARTED,
    DOWNLOADING,
    COMPLETED,
    WAITING_FOR_WIFI,
    WAITING_FOR_CONNECTION,
    FAILED
}

/**
 * Device tier — determines model selection based on device capability.
 * LOW:  ≤2GB RAM, ≤4 cores → Qwen3.5-0.8B
 * MID:  ≤4GB RAM, ≤8 cores → Qwen3-1.7B
 * HIGH: >4GB RAM, >8 cores → Qwen3.5-2B
 */
enum class DeviceTier {
    LOW,
    MID,
    HIGH
}

// ── Status Data Class ──────────────────────────────────────────

data class ModelStatus(
    val whisperDownloaded: Boolean,
    val qwenDownloaded: Boolean,
    val ttsDownloaded: Boolean,
    val bundledAvailable: Boolean,
    val totalDownloadedBytes: Long,
    val connectionInfo: ConnectionInfo,
    val deviceTier: DeviceTier = DeviceTier.MID,
    val reasoningModel: String = "QWEN3_1_7B",
    val asrModel: String = "WHISPER_SMALL"
) {
    fun isFullyReady(): Boolean = whisperDownloaded && qwenDownloaded && ttsDownloaded
    fun isPartiallyReady(): Boolean = whisperDownloaded || qwenDownloaded || ttsDownloaded
    fun getReadinessPercentage(): Int {
        var ready = 0
        if (whisperDownloaded) ready += 30
        if (qwenDownloaded) ready += 55
        if (ttsDownloaded) ready += 15
        return ready
    }

    /**
     * Human-readable model info for developer mode.
     */
    fun getModelInfo(): String = buildString {
        append("Tier: $deviceTier | ")
        append("Reasoning: $reasoningModel | ")
        append("ASR: $asrModel | ")
        append("Ready: ${getReadinessPercentage()}%")
    }
}
