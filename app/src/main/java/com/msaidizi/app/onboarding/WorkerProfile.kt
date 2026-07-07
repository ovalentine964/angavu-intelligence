package com.msaidizi.app.onboarding

import com.google.gson.Gson
import com.google.gson.annotations.SerializedName

/**
 * WorkerProfile — The formal representation of an informal worker.
 *
 * This is NOT a form. It's what Msaidizi learns through conversation.
 * Every field has a Bayesian prior (ECO 101 / STA 142) that gets updated
 * as Msaidizi interacts with the worker over time.
 *
 * Academic grounding:
 * - STA 142 (Probability): Bayesian updating — priors from onboarding, posteriors from interaction
 * - ECO 101 (Microeconomics): Consumer theory — budget constraints, preferences, substitution
 * - ECO 201 (Intermediate Micro): Producer theory — production function, cost structure
 * - ECO 206 (Microfinance): Credit constraints, savings patterns
 * - ECO 204 (African Development): Gender dimensions, rural-urban dynamics
 * - BCB 108 (Communication): Multilingual, culturally appropriate, voice-first
 *
 * @author Angavu Intelligence — Implementation Swarm 9
 */
data class WorkerProfile(
    // ── Identity ──────────────────────────────────────────────
    @SerializedName("worker_id") val workerId: String = "",
    @SerializedName("worker_name") val workerName: String = "",
    @SerializedName("agent_name") val agentName: String = "",  // What the worker calls Msaidizi
    @SerializedName("language") val language: Language = Language.KISWAHILI,
    @SerializedName("dialect") val dialect: String = "",       // e.g., "sheng", "standard_swahili", "luhya_swahili"
    @SerializedName("personality_style") val personalityStyle: PersonalityStyle = PersonalityStyle.WARM,

    // ── Phase 2: Getting to Know You ──────────────────────────
    // ECO 201: Producer theory — what is the worker's production function?
    @SerializedName("business_type") val businessType: BusinessType = BusinessType.UNKNOWN,
    @SerializedName("business_subtype") val businessSubtype: String = "",  // e.g., "tomatoes", "mandazi", "boda boda"
    @SerializedName("work_location") val workLocation: WorkLocation = WorkLocation.UNKNOWN,
    @SerializedName("market_name") val marketName: String = "",           // e.g., "Gikomba", "Kariakor"
    @SerializedName("work_schedule") val workSchedule: WorkSchedule = WorkSchedule(),
    @SerializedName("works_alone") val worksAlone: Boolean = true,
    @SerializedName("team_size") val teamSize: Int = 1,

    // ── Phase 3: Understanding Your Business ──────────────────
    // ECO 201: Cost structure, supply chain
    // ECO 206: Credit constraints, payment methods
    @SerializedName("supply_chain") val supplyChain: SupplyChain = SupplyChain(),
    @SerializedName("customer_acquisition") val customerAcquisition: CustomerAcquisition = CustomerAcquisition(),
    @SerializedName("payment_methods") val paymentMethods: PaymentMethods = PaymentMethods(),
    @SerializedName("record_keeping") val recordKeeping: RecordKeeping = RecordKeeping(),
    @SerializedName("biggest_challenge") val biggestChallenge: String = "",
    @SerializedName("challenge_category") val challengeCategory: ChallengeCategory = ChallengeCategory.UNKNOWN,

    // ── Phase 4: Setup Preferences ────────────────────────────
    @SerializedName("voice_permission_granted") val voicePermissionGranted: Boolean = false,
    @SerializedName("notification_preferences") val notificationPreferences: NotificationPreferences = NotificationPreferences(),
    @SerializedName("daily_briefing_time") val dailyBriefingTime: String = "07:00",

    // ── Bayesian Priors (STA 142) ─────────────────────────────
    // These are Msaidizi's initial beliefs about the worker, updated with every interaction
    @SerializedName("bayesian_priors") val bayesianPriors: BayesianPriors = BayesianPriors(),

    // ── Metadata ──────────────────────────────────────────────
    @SerializedName("onboarding_completed") val onboardingCompleted: Boolean = false,
    @SerializedName("onboarding_timestamp") val onboardingTimestamp: Long = 0L,
    @SerializedName("interaction_count") val interactionCount: Int = 0,
    @SerializedName("profile_version") val profileVersion: Int = 1
) {
    /**
     * Serialize to JSON for persistent storage.
     * Stored on-device only — never leaves the phone (IMPL_5 security).
     */
    fun toJson(): String = Gson().toJson(this)

    companion object {
        fun fromJson(json: String): WorkerProfile = Gson().fromJson(json, WorkerProfile::class.java)

        /**
         * Generate a unique worker ID.
         * Uses device-local UUID — no PII in the ID itself.
         */
        fun generateId(): String = java.util.UUID.randomUUID().toString().take(12)
    }
}

// ── Enums ──────────────────────────────────────────────────────

enum class Language(val code: String, val displayName: String, val flag: String) {
    KISWAHILI("sw", "Kiswahili", "🇰🇪"),
    ENGLISH("en", "English", "🇬🇧"),
    AMHARIC("am", "አማርኛ", "🇪🇹"),
    HAUSA("ha", "Hausa", "🇳🇬"),
    IGBO("ig", "Igbo", "🇳🇬"),
    YORUBA("yo", "Yoruba", "🇳🇬"),
    ZULU("zu", "isiZulu", "🇿🇦"),
    XHOSA("xh", "isiXhosa", "🇿🇦"),
    KINYARWANDA("rw", "Kinyarwanda", "🇷🇼"),
    LINGALA("ln", "Lingala", "🇨🇩"),
    SHONA("sn", "ChiShona", "🇿🇼"),
    LUGANDA("lg", "Luganda", "🇺🇬"),
    SOMALI("so", "Soomaali", "🇸🇴"),
    PORTUGUESE("pt", "Português", "🇲🇿")
}

enum class BusinessType(val displayName: String, val priorDailyRevenue: Double) {
    // ECO 201: Production function estimates by business type
    // These are Bayesian priors — updated with actual data from the worker
    RETAIL("Biashara ya Rejareja", 800.0),      // KES — micro retail
    FOOD("Mama Mboga / Food Vendor", 600.0),      // KES — food sales
    TRANSPORT("Boda Boda / Transport", 1200.0),    // KES — transport services
    SERVICES("Huduma / Services", 1000.0),         // KES — hairdressing, phone repair, etc.
    MANUFACTURING("Ufundi / Manufacturing", 1500.0), // KES — small-scale production
    AGRICULTURE("Kilimo / Agriculture", 500.0),    // KES — farming, produce
    UNKNOWN("Biashara", 700.0)                     // Default prior
}

enum class WorkLocation(val displayName: String) {
    MARKET("Soko / Market"),
    ROADSIDE("Barabarani / Roadside"),
    HOME("Nyumbani / Home"),
    MOBILE("Ninazunguka / Mobile"),
    SHOP("Duka / Shop"),
    ONLINE("Mtandaoni / Online"),
    UNKNOWN("Sijui")
}

enum class ChallengeCategory {
    CAPITAL,           // "Sina mtaji" — no capital
    INVENTORY,         // "Bidhaa zinaisha haraka" — stock runs out
    CUSTOMERS,         // "Wateja ni wachache" — few customers
    COMPETITION,       // "Washindani wengi" — many competitors
    RECORDS,           // "Sijui faida yangu" — don't know profit
    THEFT_LOSS,        // "Bidhaa zinapotea" — goods go missing
    PRICING,           // "Sijui bei sahihi" — don't know right price
    TRANSPORT,         // "Usafiri ni gharama" — transport costs
    UNKNOWN
}

enum class PersonalityStyle {
    WARM,      // Default — warm, friendly, like a trusted friend
    FORMAL,    // For workers who prefer professional language
    PLAYFUL,   // For workers who are casual and use humor
    SHENG      // For workers who speak Sheng — Msaidizi adapts
}

// ── Data Classes for Structured Onboarding Responses ──────────

data class WorkSchedule(
    @SerializedName("morning") val morning: Boolean = false,    // 6am - 12pm
    @SerializedName("afternoon") val afternoon: Boolean = false, // 12pm - 5pm
    @SerializedName("evening") val evening: Boolean = false,     // 5pm - 9pm
    @SerializedName("night") val night: Boolean = false,         // 9pm - 6am
    @SerializedName("days_per_week") val daysPerWeek: Int = 6    // Default: 6 days (Mon-Sat)
) {
    fun summary(): String {
        val periods = mutableListOf<String>()
        if (morning) periods.add("asubuhi")
        if (afternoon) periods.add("mchana")
        if (evening) periods.add("jioni")
        if (night) periods.add("usiku")
        return "${periods.joinToString(", ")} — siku $daysPerWeek kwa wiki"
    }
}

data class SupplyChain(
    @SerializedName("source_type") val sourceType: SupplySourceType = SupplySourceType.UNKNOWN,
    @SerializedName("source_location") val sourceLocation: String = "",
    @SerializedName("frequency") val frequency: String = "",        // "daily", "weekly", "biweekly"
    @SerializedName("transport_cost_kes") val transportCostKes: Double = 0.0
)

enum class SupplySourceType(val displayName: String) {
    WHOLESALE("Ghala / Wholesale market"),
    FARMER("Mkulima / Direct from farmer"),
    MIDDLEMAN("Dalali / Middleman"),
    MANUFACTURER("Mtengenezaji / Manufacturer"),
    IMPORT("Nje / Import"),
    UNKNOWN("Sijui")
}

data class CustomerAcquisition(
    @SerializedName("walk_in") val walkIn: Boolean = true,
    @SerializedName("referrals") val referrals: Boolean = false,
    @SerializedName("social_media") val socialMedia: Boolean = false,
    @SerializedName("regular_customers") val regularCustomers: Boolean = true,
    @SerializedName("estimated_regulars") val estimatedRegulars: Int = 0
)

data class PaymentMethods(
    @SerializedName("mpesa") val mpesa: Boolean = false,
    @SerializedName("cash") val cash: Boolean = true,
    @SerializedName("both") val both: Boolean = false,
    @SerializedName("mpesa_till") val mpesaTill: Boolean = false,
    @SerializedName("mpesa_paybill") val mpesaPaybill: Boolean = false
) {
    fun summary(): String = when {
        both -> "M-Pesa na pesa taslimu"
        mpesa -> "M-Pesa pekee"
        cash -> "Pesa taslimu pekee"
        else -> "Sijui"
    }
}

data class RecordKeeping(
    @SerializedName("method") val method: RecordMethod = RecordMethod.NONE,
    @SerializedName("regularity") val regularity: String = "",   // "daily", "sometimes", "never"
    @SerializedName("tracks_expenses") val tracksExpenses: Boolean = false,
    @SerializedName("tracks_sales") val tracksSales: Boolean = false,
    @SerializedName("knows_profit") val knowsProfit: Boolean = false
)

enum class RecordMethod(val displayName: String) {
    NOTEBOOK("Daftari / Notebook"),
    PHONE("Simu / Phone app"),
    MEMORY("Kichwani / Memory"),
    SOMEONE_ELSE("Mtu mwingine / Someone else helps"),
    NONE("Hakuna / None")
}

data class NotificationPreferences(
    @SerializedName("daily_briefing") val dailyBriefing: Boolean = true,
    @SerializedName("sales_reminders") val salesReminders: Boolean = true,
    @SerializedName("restock_alerts") val restockAlerts: Boolean = true,
    @SerializedName("market_price_alerts") val marketPriceAlerts: Boolean = true,
    @SerializedName("quiet_hours_start") val quietHoursStart: String = "21:00",
    @SerializedName("quiet_hours_end") val quietHoursEnd: String = "06:00"
)

// ── Bayesian Priors (STA 142) ──────────────────────────────────

/**
 * Bayesian priors for the worker's economic behavior.
 *
 * STA 142 (Probability): These represent Msaidizi's initial beliefs
 * about the worker before observing any real data. Every interaction
 * updates these priors using Bayes' theorem:
 *
 *   P(θ|data) ∝ P(data|θ) × P(θ)
 *
 * Where:
 * - P(θ) = prior (what we believe before seeing data)
 * - P(data|θ) = likelihood (how well the data fits our model)
 * - P(θ|data) = posterior (updated belief after seeing data)
 *
 * ECO 101: Consumer theory — budget constraints, preferences
 * ECO 201: Producer theory — production function, returns to scale
 * ECO 206: Microfinance — credit constraints, savings patterns
 */
data class BayesianPriors(
    // ── Revenue Priors (ECO 201: Production function) ──────────
    @SerializedName("estimated_daily_revenue") val estimatedDailyRevenue: Double = 0.0,
    @SerializedName("revenue_confidence") val revenueConfidence: Double = 0.3,  // Low initial confidence
    @SerializedName("revenue_variance") val revenueVariance: Double = 500.0,     // High initial uncertainty

    // ── Cost Priors (ECO 201: Cost structure) ──────────────────
    @SerializedName("estimated_daily_cost") val estimatedDailyCost: Double = 0.0,
    @SerializedName("cost_confidence") val costConfidence: Double = 0.3,
    @SerializedName("cost_variance") val costVariance: Double = 300.0,

    // ── Profit Margin Priors ───────────────────────────────────
    @SerializedName("estimated_margin") val estimatedMargin: Double = 0.25,  // 25% default for informal retail
    @SerializedName("margin_confidence") val marginConfidence: Double = 0.2,

    // ── Savings Priors (ECO 206: Microfinance) ─────────────────
    @SerializedName("estimated_savings_rate") val estimatedSavingsRate: Double = 0.05,  // 5% default
    @SerializedName("savings_confidence") val savingsConfidence: Double = 0.2,
    @SerializedName("likely_has_mpesa") val likelyHasMpesa: Boolean = true,  // 96% of Kenyans have M-Pesa

    // ── Credit Priors (ECO 206: Credit constraints) ────────────
    @SerializedName("credit_constraint_level") val creditConstraintLevel: Double = 0.7,  // Most informal workers are credit-constrained
    @SerializedName("likely_has_formal_credit") val likelyHasFormalCredit: Boolean = false,
    @SerializedName("likely_uses_informal_lending") val likelyUsesInformalLending: Boolean = true,

    // ── Consumer Behavior Priors (ECO 101: Consumer theory) ────
    @SerializedName("price_sensitivity") val priceSensitivity: Double = 0.8,  // High — budget-constrained
    @SerializedName("brand_loyalty") val brandLoyalty: Double = 0.3,          // Low — price-driven
    @SerializedName("substitution_elasticity") val substitutionElasticity: Double = 1.2,  // Elastic — easy to switch

    // ── Risk Priors (STA 142 + ECO 101) ───────────────────────
    @SerializedName("risk_aversion") val riskAversion: Double = 0.6,  // Moderately risk-averse
    @SerializedName("income_volatility") val incomeVolatility: Double = 0.4,  // High volatility in informal sector

    // ── Growth Priors (ECO 204: African Development) ───────────
    @SerializedName("growth_potential") val growthPotential: Double = 0.5,
    @SerializedName("formalization_readiness") val formalizationReadiness: Double = 0.2  // Most start informal
) {
    /**
     * Update a prior using Bayes' theorem.
     *
     * @param observation The observed value
     * @param observationConfidence How reliable is this observation (0.0 - 1.0)
     * @param priorMean Current prior mean
     * @param priorVariance Current prior variance
     * @return Updated (posterior) mean
     */
    fun bayesianUpdate(
        observation: Double,
        observationConfidence: Double,
        priorMean: Double,
        priorVariance: Double
    ): Double {
        // Simple conjugate normal update
        val observationVariance = 1.0 / (observationConfidence.coerceIn(0.01, 0.99) * 10)
        val posteriorVariance = 1.0 / (1.0 / priorVariance + 1.0 / observationVariance)
        val posteriorMean = posteriorVariance * (priorMean / priorVariance + observation / observationVariance)
        return posteriorMean
    }
}
