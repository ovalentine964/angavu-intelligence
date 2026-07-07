package com.msaidizi.app.agent

import android.content.Context
import android.util.Log
import com.msaidizi.app.core.security.KeyManager
import java.util.regex.Pattern
/**
 * Orchestrator — Agent response pipeline with output sanitization
 * and academic framework integration.
 *
 * FIX 4: Agent Output Sanitization
 * ---------------------------------
 * PREVIOUS (VULNERABLE): Agent responses were displayed directly to the
 * user without sanitization. A compromised or jailbroken LLM could inject:
 *   - XSS payloads (if rendered in WebView)
 *   - Prompt injection (to manipulate downstream agents)
 *   - Phishing links (fake M-Pesa URLs)
 *   - PII leakage (phone numbers, national IDs from training data)
 *   - SQL/NoSQL injection (if responses reach database queries)
 *
 * FIX: All agent output passes through [sanitizeAgentOutput] before
 * display. This strips dangerous content while preserving legitimate
 * Swahili/multilingual text including code-switched content.
 *
 * IMPL 16: Academic Framework Integration
 * ----------------------------------------
 * Every agent response is grounded in Valentine's Economics & Statistics
 * academic framework. The orchestrator injects academic context into agent
 * prompts via [AcademicFramework.generateAcademicPromptSuffix].
 *
 * Defense-in-depth layers:
 *   1. HTML/script tag stripping (WebView XSS prevention)
 *   2. URL sanitization (phishing link detection)
 *   3. PII masking (phone numbers, national IDs, bank accounts)
 *   4. Prompt injection detection (prevent agent manipulation)
 *   5. Content length limiting (prevent UI overflow attacks)
 *   6. Control character removal (prevent terminal/shell injection)
 *   7. Academic grounding (ensure responses are theoretically sound)
 */
class Orchestrator(private val context: Context) {

    companion object {
        private const val TAG = "Orchestrator"
        private const val MAX_RESPONSE_LENGTH = 5000  // chars
        private const val MAX_URL_COUNT = 3           // max URLs in a single response

        // ── Dangerous pattern regexes ─────────────────────────

        // HTML/XML tags that could carry XSS payloads
        private val HTML_TAG_PATTERN = Pattern.compile(
            "</?(?:script|iframe|object|embed|form|input|meta|link|style|base|applet|marquee|svg|math)[^>]*>",
            Pattern.CASE_INSENSITIVE
        )

        // Generic HTML tags — strip all of them
        private val ALL_HTML_TAGS = Pattern.compile("<[^>]+>")

        // JavaScript event handlers in attributes
        private val JS_EVENT_HANDLER = Pattern.compile(
            "\\bon\\w+\\s*=\\s*['\"]",
            Pattern.CASE_INSENSITIVE
        )

        // javascript: and data: URIs
        private val DANGEROUS_URI = Pattern.compile(
            "(?:javascript|data|vbscript|file|ftp):\\s*",
            Pattern.CASE_INSENSITIVE
        )

        // Kenyan phone numbers: +254 7XX XXX XXX, 07XX XXX XXX, etc.
        private val PHONE_PATTERN = Pattern.compile(
            "(?:\\+?254|0)[\\s.-]?[17]\\d{1}[\\s.-]?\\d{3}[\\s.-]?\\d{3,4}"
        )

        // National ID number: 8+ digits starting with specific patterns
        private val NATIONAL_ID_PATTERN = Pattern.compile(
            "\\b\\d{7,10}\\b(?=.{0,20}(?:ID|id|Namba|namba|kitambulisho))"
        )

        // Account/card numbers (M-Pesa, bank)
        private val ACCOUNT_NUMBER_PATTERN = Pattern.compile(
            "\\b(?:\\d{4}[\\s-]?){3,4}\\d{1,4}\\b"
        )

        // Prompt injection patterns (attempts to manipulate the LLM)
        private val PROMPT_INJECTION_PATTERNS = listOf(
            Pattern.compile("(?i)ignore\\s+(?:all\\s+)?(?:previous|prior|above)\\s+instructions"),
            Pattern.compile("(?i)you\\s+are\\s+now\\s+(?:a|an|the)"),
            Pattern.compile("(?i)system\\s*prompt\\s*:",
                Pattern.CASE_INSENSITIVE or Pattern.LITERAL),
            Pattern.compile("(?i)\\[/?INST\\]"),  // Llama-style injection
            Pattern.compile("(?i)<\\|im_start\\|>"),  // ChatML injection
            Pattern.compile("(?i)pretend\\s+(?:you|that)"),
            Pattern.compile("(?i)act\\s+as\\s+(?:a|an)"),
            Pattern.compile("(?i)\\bDAN\\b.*\\bjailbreak\\b"),
            Pattern.compile("(?i)\\bdo\\s+anything\\s+now\\b"),
        )

        // Suspicious URLs (known phishing patterns for East Africa)
        private val SUSPICIOUS_URL_PATTERNS = listOf(
            Pattern.compile("(?i)m-pesa.*\\.(?!safaricom\\.co\\.ke)"),  // Fake M-Pesa domains
            Pattern.compile("(?i)mpesa.*\\.(?!safaricom\\.co\\.ke)"),
            Pattern.compile("(?i)safaricom.*\\.(?!co\\.ke)"),
        )

        // Control characters (except newline, tab, carriage return)
        private val CONTROL_CHARS = Pattern.compile("[\\x00-\\x08\\x0B\\x0C\\x0E-\\x1F\\x7F]")

        // Zero-width characters (used for invisible prompt injection)
        private val ZERO_WIDTH_CHARS = Pattern.compile("[\\u200B\\u200C\\u200D\\uFEFF\\u2060\\u180E]")
    }

    /**
     * Sanitize agent output before displaying to the user.
     *
     * This is the PRIMARY defense against malicious agent responses.
     * It runs on EVERY agent response, including:
     * - On-device model output (Qwen 0.5B)
     * - Cloud fallback responses (DeepSeek, GPT)
     * - Federated model outputs
     * - Third-party agent responses (via A2A protocol)
     *
     * @param rawOutput The unsanitized agent response
     * @param contextInfo Optional context about the agent that produced this output
     * @return Sanitized response safe for display
     */
    fun sanitizeAgentOutput(rawOutput: String, contextInfo: String = ""): String {
        if (rawOutput.isBlank()) return ""

        var sanitized = rawOutput

        // Layer 1: Remove control characters (prevents terminal injection)
        sanitized = CONTROL_CHARS.matcher(sanitized).replaceAll("")

        // Layer 2: Remove zero-width characters (invisible prompt injection)
        sanitized = ZERO_WIDTH_CHARS.matcher(sanitized).replaceAll("")

        // Layer 3: Strip dangerous HTML tags (XSS prevention)
        sanitized = HTML_TAG_PATTERN.matcher(sanitized).replaceAll("[removed]")

        // Layer 4: Strip ALL remaining HTML tags
        sanitized = ALL_HTML_TAGS.matcher(sanitized).replaceAll("")

        // Layer 5: Remove JavaScript event handlers
        sanitized = JS_EVENT_HANDLER.matcher(sanitized).replaceAll("on[removed]=")

        // Layer 6: Neutralize dangerous URIs
        sanitized = DANGEROUS_URI.matcher(sanitized).replaceAll("[removed]:")

        // Layer 7: Mask PII (phone numbers, IDs, account numbers)
        sanitized = maskPII(sanitized)

        // Layer 8: Detect and flag prompt injection attempts
        val injectionDetected = detectPromptInjection(sanitized)
        if (injectionDetected) {
            Log.w(TAG, "Prompt injection detected in agent output from: $contextInfo")
            // Strip the injection pattern but keep the rest
            sanitized = stripPromptInjection(sanitized)
        }

        // Layer 9: Validate and limit URLs
        sanitized = sanitizeUrls(sanitized)

        // Layer 10: Normalize whitespace (prevents layout attacks)
        sanitized = sanitized.replace(Regex("\\s{4,}"), "   ")
        sanitized = sanitized.trim()

        // Layer 11: Enforce length limit
        if (sanitized.length > MAX_RESPONSE_LENGTH) {
            sanitized = sanitized.substring(0, MAX_RESPONSE_LENGTH) + "...[truncated]"
        }

        // Layer 12: Unescape HTML entities that survived
        sanitized = sanitized
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", "\"")
            .replace("&#39;", "'")

        return sanitized
    }

    /**
     * Mask PII in agent output.
     *
     * Replaces:
     * - Phone numbers → +254 7XX XXX XXX
     * - National ID references → [ID MASKED]
     * - Account numbers → [ACCOUNT MASKED]
     *
     * Preserves legitimate numeric content (prices, quantities, dates).
     */
    private fun maskPII(text: String): String {
        var masked = text

        // Mask phone numbers
        masked = PHONE_PATTERN.matcher(masked).replaceAll("[PHONE MASKED]")

        // Mask national ID references (only when near ID-related keywords)
        masked = NATIONAL_ID_PATTERN.matcher(masked).replaceAll("[ID MASKED]")

        // Mask account numbers (16-digit sequences with optional separators)
        masked = ACCOUNT_NUMBER_PATTERN.matcher(masked).replaceAll("[ACCOUNT MASKED]")

        return masked
    }

    /**
     * Detect prompt injection attempts.
     *
     * Returns true if the output contains patterns that suggest the
     * agent was manipulated to inject instructions.
     */
    private fun detectPromptInjection(text: String): Boolean {
        return PROMPT_INJECTION_PATTERNS.any { pattern ->
            pattern.matcher(text).find()
        }
    }

    /**
     * Strip prompt injection patterns from the output.
     *
     * Rather than rejecting the entire response (which would be a DoS vector),
     * we remove the suspicious patterns and keep the rest.
     */
    private fun stripPromptInjection(text: String): String {
        var cleaned = text
        for (pattern in PROMPT_INJECTION_PATTERNS) {
            cleaned = pattern.matcher(cleaned).replaceAll("[injection removed]")
        }
        return cleaned
    }

    /**
     * Validate and sanitize URLs in the output.
     *
     * - Removes suspicious phishing URLs (fake M-Pesa domains)
     * - Limits the number of URLs to prevent spam
     * - Ensures all URLs use HTTPS
     */
    private fun sanitizeUrls(text: String): String {
        var sanitized = text

        // Check for suspicious URLs
        for (pattern in SUSPICIOUS_URL_PATTERNS) {
            if (pattern.matcher(sanitized).find()) {
                Log.w(TAG, "Suspicious URL detected in agent output")
                sanitized = pattern.matcher(sanitized).replaceAll("[suspicious link removed]")
            }
        }

        // Count remaining URLs and cap them
        val urlPattern = Pattern.compile("https?://\\S+")
        val matcher = urlPattern.matcher(sanitized)
        var urlCount = 0
        val urls = mutableListOf<String>()
        while (matcher.find()) {
            urls.add(matcher.group())
            urlCount++
        }

        if (urlCount > MAX_URL_COUNT) {
            // Remove excess URLs (keep first MAX_URL_COUNT)
            for (i in MAX_URL_COUNT until urls.size) {
                sanitized = sanitized.replace(urls[i], "[link removed]")
            }
        }

        // Force HTTP → HTTPS for any remaining URLs
        sanitized = sanitized.replace(Regex("http://(?!localhost)"), "https://")

        return sanitized
    }

    /**
     * Process a complete agent response through the sanitization pipeline.
     *
     * This is the main entry point called by the UI layer.
     *
     * @param agentResponse Raw response from the agent
     * @param agentId Identifier of the agent that produced the response
     * @return Sanitized, display-ready response
     */
    fun processAgentResponse(agentResponse: AgentResponse): AgentResponse {
        val sanitizedText = sanitizeAgentOutput(
            rawOutput = agentResponse.text,
            contextInfo = "agent=${agentResponse.agentId}"
        )

        return agentResponse.copy(
            text = sanitizedText,
            isSanitized = true,
            originalLength = agentResponse.text.length
        )
    }

    /**
     * Get the academic prompt suffix for a given agent type.
     * Injected into the agent's system prompt to ground responses in theory.
     *
     * @param agentType The agent requesting academic context
     * @return Academic prompt suffix to append to system prompt
     */
    fun getAcademicPromptSuffix(agentType: AgentType): String {
        return AcademicFramework.generateAcademicPromptSuffix(agentType)
    }

    /**
     * Get the full system prompt for an agent, including academic grounding.
     *
     * @param agentType The agent type
     * @param basePrompt The agent's base system prompt
     * @return Enhanced prompt with academic framework
     */
    fun buildAgentPrompt(agentType: AgentType, basePrompt: String): String {
        val academicSuffix = getAcademicPromptSuffix(agentType)
        return "$basePrompt\n$academicSuffix"
    }
}

/**
 * Represents a response from an agent.
 */
data class AgentResponse(
    val agentId: String,
    val text: String,
    val confidence: Float = 0f,
    val isSanitized: Boolean = false,
    val originalLength: Int = 0,
    val timestamp: Long = System.currentTimeMillis()
)
