package com.msaidizi.app.agent

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.util.Log

/**
 * ModelRouter — Intelligent model routing with zero paid API dependency.
 *
 * Valentine's directive: ZERO paid APIs, full ownership.
 *
 * Fallback chain (July 2026):
 *   1. On-device (Qwen3.5) — default, works offline
 *   2. Angavu Cloud (open-source model) — for complex tasks when online
 *
 * REMOVED from previous chain (paid APIs eliminated):
 *   - GPT-5.4 nano (OpenAI) — REMOVED: paid API
 *   - Claude Haiku (Anthropic) — REMOVED: paid API
 *   - DeepSeek V4 Flash — REMOVED: paid API
 *
 * Design principles:
 *   - On-device is the DEFAULT for all routine tasks
 *   - Angavu Cloud is used ONLY for tasks requiring larger models
 *   - Offline mode always falls back to on-device — no blocking
 *   - All models are open-source or owned by Angavu
 *   - Model routing is transparent to the agent layer
 *
 * Model routing by task complexity (Swarm G recommendation):
 *   - Tier 1 (simple): Balance checks, stock counts → On-device Qwen3.5
 *   - Tier 2 (standard): Price queries, trade matching → On-device Qwen3.5
 *   - Tier 3 (complex): Credit assessment, planning → Angavu Cloud model
 *
 * @author Angavu Intelligence — Implementation Swarm 17
 */
class ModelRouter(
    private val context: Context,
    private val config: ModelRouterConfig = ModelRouterConfig()
) {

    companion object {
        private const val TAG = "ModelRouter"
    }

    // ── Configuration ────────────────────────────────────────

    data class ModelRouterConfig(
        /** On-device model identifier (Qwen3.5 quantized for Android) */
        val onDeviceModelId: String = "qwen3.5-ondevice",

        /** Angavu Cloud model endpoint (open-source model) */
        val cloudEndpoint: String = "https://api.angavu.ai/v1/inference",

        /** Angavu Cloud model identifier (open-source model, TBD) */
        val cloudModelId: String = "angavu-open-v1",

        /** Maximum latency before falling back to on-device (ms) */
        val cloudTimeoutMs: Long = 5000L,

        /** Whether to prefer on-device even when cloud is available */
        val preferOnDevice: Boolean = true,

        /** Task tiers that are always on-device regardless of connectivity */
        val alwaysOnDeviceTiers: Set<TaskTier> = setOf(
            TaskTier.TIER_1_SIMPLE,
            TaskTier.TIER_2_STANDARD
        ),

        /** Task tiers that use cloud when available */
        val cloudEligibleTiers: Set<TaskTier> = setOf(
            TaskTier.TIER_3_COMPLEX
        )
    )

    // ── Task Tiers ───────────────────────────────────────────

    /**
     * Task complexity tiers — from Swarm G research.
     * Determines which model handles the task.
     */
    enum class TaskTier {
        /** Balance checks, stock counts, simple lookups → On-device */
        TIER_1_SIMPLE,

        /** Price queries, trade matching, routine operations → On-device */
        TIER_2_STANDARD,

        /** Credit assessment, planning, complex analysis → Cloud (when available) */
        TIER_3_COMPLEX
    }

    // ── Model Target ─────────────────────────────────────────

    /**
     * Where to run inference.
     */
    sealed class ModelTarget {
        /** Run on-device using Qwen3.5 (offline-capable) */
        data class OnDevice(
            val modelId: String = "qwen3.5-ondevice"
        ) : ModelTarget()

        /** Run on Angavu Cloud (open-source model) */
        data class AngavuCloud(
            val endpoint: String,
            val modelId: String
        ) : ModelTarget()
    }

    // ── Routing ──────────────────────────────────────────────

    /**
     * Route a task to the appropriate model.
     *
     * Decision logic:
     * 1. Always on-device for Tier 1 & 2 (offline-capable, fast)
     * 2. Tier 3: on-device if preferOnDevice=true or offline
     * 3. Tier 3: Angavu Cloud if online and preferOnDevice=false
     * 4. Always fall back to on-device if cloud fails
     *
     * @param taskTier The complexity tier of the task
     * @return ModelTarget indicating where to run inference
     */
    fun route(taskTier: TaskTier): ModelTarget {
        // Tier 1 & 2: Always on-device
        if (taskTier in config.alwaysOnDeviceTiers) {
            Log.d(TAG, "Routing $taskTier → on-device (always)")
            return ModelTarget.OnDevice(config.onDeviceModelId)
        }

        // Tier 3: Check if cloud is available and preferred
        if (taskTier in config.cloudEligibleTiers) {
            if (config.preferOnDevice) {
                Log.d(TAG, "Routing $taskTier → on-device (preferOnDevice=true)")
                return ModelTarget.OnDevice(config.onDeviceModelId)
            }

            if (!isOnline()) {
                Log.d(TAG, "Routing $taskTier → on-device (offline)")
                return ModelTarget.OnDevice(config.onDeviceModelId)
            }

            Log.d(TAG, "Routing $taskTier → Angavu Cloud")
            return ModelTarget.AngavuCloud(
                endpoint = config.cloudEndpoint,
                modelId = config.cloudModelId
            )
        }

        // Default: on-device
        Log.d(TAG, "Routing $taskTier → on-device (default)")
        return ModelTarget.OnDevice(config.onDeviceModelId)
    }

    /**
     * Route with automatic fallback.
     *
     * Tries the primary target first. If it fails (timeout, error),
     * falls back to on-device. This ensures workers always get a
     * response, even when the network is unreliable.
     *
     * @param taskTier The complexity tier of the task
     * @param prompt The input prompt
     * @return Inference result from whichever model succeeds
     */
    suspend fun routeWithFallback(
        taskTier: TaskTier,
        prompt: String
    ): InferenceResult {
        val primary = route(taskTier)

        return try {
            executeInference(primary, prompt)
        } catch (e: Exception) {
            Log.w(TAG, "Primary model failed, falling back to on-device", e)

            // Always fall back to on-device — never block
            val fallback = ModelTarget.OnDevice(config.onDeviceModelId)
            try {
                executeInference(fallback, prompt)
            } catch (fallbackError: Exception) {
                Log.e(TAG, "On-device fallback also failed", fallbackError)
                InferenceResult(
                    text = "Samahani, nimehitaji muda. Jaribu tena baada ya muda mfupi.",
                    // "Sorry, I needed some time. Try again shortly."
                    modelUsed = "none",
                    success = false,
                    error = fallbackError.message
                )
            }
        }
    }

    // ── Inference Execution ──────────────────────────────────

    /**
     * Execute inference on the specified model target.
     */
    private suspend fun executeInference(
        target: ModelTarget,
        prompt: String
    ): InferenceResult {
        return when (target) {
            is ModelTarget.OnDevice -> executeOnDevice(target, prompt)
            is ModelTarget.AngavuCloud -> executeCloud(target, prompt)
        }
    }

    /**
     * Run inference on the on-device model (Qwen3.5).
     *
     * This uses the local Qwen3.5 model running via llama.cpp
     * or the Android NNAPI delegate. Always available, even offline.
     */
    private suspend fun executeOnDevice(
        target: ModelTarget.OnDevice,
        prompt: String
    ): InferenceResult {
        // In production, this calls the local model via llama.cpp JNI
        // For now, delegate to the existing ModelManager
        return try {
            val result = ModelManager.getInstance(context).generate(
                modelId = target.modelId,
                prompt = prompt
            )
            InferenceResult(
                text = result,
                modelUsed = target.modelId,
                success = true
            )
        } catch (e: Exception) {
            Log.e(TAG, "On-device inference failed", e)
            throw e
        }
    }

    /**
     * Run inference on Angavu Cloud (open-source model).
     *
     * Only used for Tier 3 tasks when online. All data stays
     * within Angavu infrastructure — no third-party APIs.
     */
    private suspend fun executeCloud(
        target: ModelTarget.AngavuCloud,
        prompt: String
    ): InferenceResult {
        // In production, this calls Angavu's cloud API
        // The cloud runs an open-source model (e.g., Qwen2.5-72B, Llama 3.1)
        return try {
            val response = AngavuCloudClient(context).inference(
                endpoint = target.endpoint,
                modelId = target.modelId,
                prompt = prompt,
                timeoutMs = config.cloudTimeoutMs
            )
            InferenceResult(
                text = response.text,
                modelUsed = "${target.modelId}@cloud",
                success = true,
                latencyMs = response.latencyMs
            )
        } catch (e: Exception) {
            Log.w(TAG, "Cloud inference failed", e)
            throw e
        }
    }

    // ── Network Detection ────────────────────────────────────

    /**
     * Check if the device has internet connectivity.
     */
    private fun isOnline(): Boolean {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager
            ?: return false

        val network = cm.activeNetwork ?: return false
        val capabilities = cm.getNetworkCapabilities(network) ?: return false

        return capabilities.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }

    // ── Data Classes ─────────────────────────────────────────

    data class InferenceResult(
        val text: String,
        val modelUsed: String,
        val success: Boolean,
        val latencyMs: Long? = null,
        val error: String? = null
    )

    // ── Placeholder Clients ──────────────────────────────────

    /**
     * Placeholder for the on-device model manager.
     * Will be replaced with actual llama.cpp JNI integration.
     */
    class ModelManager private constructor(private val context: Context) {
        companion object {
            @Volatile private var instance: ModelManager? = null
            fun getInstance(context: Context): ModelManager =
                instance ?: synchronized(this) {
                    instance ?: ModelManager(context.applicationContext).also { instance = it }
                }
        }

        suspend fun generate(modelId: String, prompt: String): String {
            // TODO: Integrate with llama.cpp JNI for Qwen3.5
            throw NotImplementedError("On-device model not yet integrated")
        }
    }

    /**
     * Placeholder for Angavu Cloud client.
     * All traffic stays within Angavu infrastructure.
     */
    class AngavuCloudClient(private val context: Context) {
        data class CloudResponse(val text: String, val latencyMs: Long)

        suspend fun inference(
            endpoint: String,
            modelId: String,
            prompt: String,
            timeoutMs: Long
        ): CloudResponse {
            // TODO: Implement HTTP client to Angavu Cloud
            // Must use PQC (ML-KEM) for transport encryption
            throw NotImplementedError("Angavu Cloud client not yet integrated")
        }
    }
}
