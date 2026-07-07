package com.msaidizi.app.agent

import android.content.Context
import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import com.msaidizi.app.core.dialect.DialectAdapter
import java.util.concurrent.ConcurrentHashMap
import java.util.regex.Pattern

/**
 * IntentRouter — Config-driven intent classification.
 *
 * FIX 4.3: Replaced 800+ lines of hardcoded regex with a JSON config file
 * (assets/intent_patterns.json). Intent patterns can now be updated
 * without code changes — just edit the JSON and reload.
 *
 * Architecture:
 * 1. Load patterns from JSON config at init
 * 2. Compile regex patterns once (cached)
 * 3. Score each intent by pattern matches + keyword matches + sheng boost
 * 4. Return highest-scoring intent above confidence threshold
 *
 * @author Angavu Intelligence — Architecture Fix Team 4
 */
class IntentRouter(
    private val context: Context,
    private val dialectAdapter: DialectAdapter? = null
) {

    // ── Config model ──────────────────────────────────────────

    data class IntentConfig(
        @SerializedName("_meta") val meta: ConfigMeta = ConfigMeta(),
        @SerializedName("settings") val settings: ConfigSettings = ConfigSettings(),
        @SerializedName("intents") val intents: Map<String, IntentDefinition> = emptyMap()
    )

    data class ConfigMeta(
        @SerializedName("version") val version: String = "1.0.0",
        @SerializedName("description") val description: String = ""
    )

    data class ConfigSettings(
        @SerializedName("case_sensitive") val caseSensitive: Boolean = false,
        @SerializedName("sheng_weight_boost") val shengWeightBoost: Double = 1.3,
        @SerializedName("min_confidence_threshold") val minConfidenceThreshold: Double = 0.4,
        @SerializedName("fallback_intent") val fallbackIntent: String = "UNKNOWN"
    )

    data class IntentDefinition(
        @SerializedName("description") val description: String = "",
        @SerializedName("priority") val priority: Int = 5,
        @SerializedName("patterns") val patterns: List<String> = emptyList(),
        @SerializedName("sheng_patterns") val shengPatterns: List<String> = emptyList(),
        @SerializedName("keywords") val keywords: List<String> = emptyList(),
        @SerializedName("response_hints") val responseHints: List<String> = emptyList()
    )

    // ── Classification result ─────────────────────────────────

    data class IntentClassification(
        val intent: String,
        val confidence: Double,
        val matchedPattern: String? = null,
        val isSheng: Boolean = false,
        val responseHints: List<String> = emptyList()
    )

    // ── State ─────────────────────────────────────────────────

    private var config: IntentConfig = IntentConfig()
    private val compiledPatterns = ConcurrentHashMap<String, List<CompiledPattern>>()
    private val compiledShengPatterns = ConcurrentHashMap<String, List<CompiledPattern>>()

    data class CompiledPattern(
        val pattern: Pattern,
        val source: String // "standard" or "sheng"
    )

    init {
        loadConfig()
    }

    // ── Config loading ────────────────────────────────────────

    /**
     * Load and compile patterns from the JSON config file.
     * Call this to reload after updating the config at runtime.
     */
    fun loadConfig() {
        try {
            val json = context.assets.open("intent_patterns.json")
                .bufferedReader()
                .use { it.readText() }
            config = Gson().fromJson(json, IntentConfig::class.java)
            compileAllPatterns()
        } catch (e: Exception) {
            android.util.Log.e("IntentRouter", "Failed to load intent_patterns.json", e)
            // Fall back to empty config — everything will be UNKNOWN
            config = IntentConfig()
        }
    }

    /**
     * Reload config from a custom JSON string (e.g., downloaded update).
     */
    fun loadConfigFromJson(json: String) {
        try {
            config = Gson().fromJson(json, IntentConfig::class.java)
            compileAllPatterns()
        } catch (e: Exception) {
            android.util.Log.e("IntentRouter", "Failed to parse intent config JSON", e)
        }
    }

    private fun compileAllPatterns() {
        compiledPatterns.clear()
        compiledShengPatterns.clear()

        val flags = if (config.settings.caseSensitive) 0 else Pattern.CASE_INSENSITIVE

        for ((intentName, intentDef) in config.intents) {
            val standard = intentDef.patterns.mapNotNull { patternStr ->
                try {
                    CompiledPattern(Pattern.compile(patternStr, flags), "standard")
                } catch (e: Exception) {
                    android.util.Log.w("IntentRouter", "Invalid pattern for $intentName: $patternStr")
                    null
                }
            }
            compiledPatterns[intentName] = standard

            val sheng = intentDef.shengPatterns.mapNotNull { patternStr ->
                try {
                    CompiledPattern(Pattern.compile(patternStr, flags), "sheng")
                } catch (e: Exception) {
                    android.util.Log.w("IntentRouter", "Invalid sheng pattern for $intentName: $patternStr")
                    null
                }
            }
            compiledShengPatterns[intentName] = sheng
        }
    }

    // ── Classification ────────────────────────────────────────

    /**
     * Classify the user's input text into an intent.
     *
     * Scoring algorithm:
     * 1. Pattern match → base score 1.0
     * 2. Sheng pattern match → base score × sheng_weight_boost
     * 3. Keyword match → base score 0.5 per keyword (max 3)
     * 4. Intent priority bonus → priority / 20.0
     * 5. Final score = max(pattern_score, keyword_score) + priority_bonus
     */
    fun classify(text: String): IntentClassification {
        val normalizedText = text.trim().lowercase()
        if (normalizedText.isBlank()) {
            return IntentClassification(
                intent = config.settings.fallbackIntent,
                confidence = 0.0
            )
        }

        val isSheng = dialectAdapter?.hasCodeSwitching(normalizedText) == true ||
            containsShengMarkers(normalizedText)

        val scores = mutableMapOf<String, Double>()
        val matchedPatterns = mutableMapOf<String, String>()

        for ((intentName, intentDef) in config.intents) {
            if (intentName == "UNKNOWN") continue

            var bestScore = 0.0
            var bestPattern: String? = null

            // 1. Check standard patterns
            val standardMatches = compiledPatterns[intentName] ?: emptyList()
            for (cp in standardMatches) {
                if (cp.pattern.matcher(normalizedText).find()) {
                    val score = 1.0
                    if (score > bestScore) {
                        bestScore = score
                        bestPattern = cp.pattern.pattern()
                    }
                }
            }

            // 2. Check sheng patterns (with boost)
            if (isSheng) {
                val shengMatches = compiledShengPatterns[intentName] ?: emptyList()
                for (cp in shengMatches) {
                    if (cp.pattern.matcher(normalizedText).find()) {
                        val score = 1.0 * config.settings.shengWeightBoost
                        if (score > bestScore) {
                            bestScore = score
                            bestPattern = cp.pattern.pattern()
                        }
                    }
                }
            }

            // 3. Keyword matching (weaker signal)
            val keywordHits = intentDef.keywords.count { keyword ->
                normalizedText.contains(keyword.lowercase())
            }
            val keywordScore = (keywordHits.coerceAtMost(3) * 0.5).coerceAtMost(1.5)

            // 4. Priority bonus
            val priorityBonus = intentDef.priority / 20.0

            // 5. Final score
            val finalScore = maxOf(bestScore, keywordScore * 0.7) + priorityBonus

            if (finalScore > 0) {
                scores[intentName] = finalScore
                if (bestPattern != null) {
                    matchedPatterns[intentName] = bestPattern
                }
            }
        }

        // Find the best intent
        val bestEntry = scores.maxByOrNull { it.value }
        if (bestEntry == null || bestEntry.value < config.settings.minConfidenceThreshold) {
            return IntentClassification(
                intent = config.settings.fallbackIntent,
                confidence = bestEntry?.value ?: 0.0,
                isSheng = isSheng,
                responseHints = config.intents[config.settings.fallbackIntent]?.responseHints ?: emptyList()
            )
        }

        val intentDef = config.intents[bestEntry.key]
        return IntentClassification(
            intent = bestEntry.key,
            confidence = bestEntry.value.coerceAtMost(1.0),
            matchedPattern = matchedPatterns[bestEntry.key],
            isSheng = isSheng,
            responseHints = intentDef?.responseHints ?: emptyList()
        )
    }

    // ── Sheng detection ───────────────────────────────────────

    private val shengMarkers = setOf(
        "sasa", "niaje", "mambo", "vipi", "poa", "fiti", "safi",
        "brathe", "boss", "ndege", "kanyang", "ka-straight",
        "kuja", "sepa", "pusha", "move", "droo", "ndege"
    )

    private fun containsShengMarkers(text: String): Boolean {
        val words = text.split("\\s+".toRegex())
        return words.any { it in shengMarkers }
    }

    // ── Utility ───────────────────────────────────────────────

    /**
     * Get all registered intent names.
     */
    fun getRegisteredIntents(): Set<String> = config.intents.keys

    /**
     * Get the config version.
     */
    fun getConfigVersion(): String = config.meta.version

    /**
     * Check if a specific intent is registered.
     */
    fun hasIntent(intentName: String): Boolean = config.intents.containsKey(intentName)
}
