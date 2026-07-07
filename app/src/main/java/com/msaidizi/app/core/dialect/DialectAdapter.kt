package com.msaidizi.app.core.dialect

import com.msaidizi.app.onboarding.Language

/**
 * DialectAdapter — Multilingual, culturally appropriate communication.
 *
 * BCB 108 (Communication): Multilingual code-switching is the norm in Africa.
 * Workers don't speak "pure" languages — they mix languages, use slang,
 * and switch between registers depending on context.
 *
 * A mama mboga in Nairobi might say:
 * "Nimepata customer mmoja, alinunua tomatoes mbili, akanilipa na M-Pesa"
 * — mixing Kiswahili, English, and Sheng seamlessly.
 *
 * Msaidizi must understand ALL of this and respond appropriately.
 *
 * Key principles:
 * 1. Detect the worker's dialect/register from their speech
 * 2. Respond in the same register — don't be more formal than the worker
 * 3. Understand code-switching — mixing languages is normal
 * 4. Be culturally appropriate — different cultures have different norms
 * 5. Voice-first — optimize for spoken language, not written
 *
 * @author Angavu Intelligence — Implementation Swarm 9
 */
interface DialectAdapter {

    /**
     * Detect the dialect/register from text.
     * Returns a dialect identifier (e.g., "sheng", "standard_swahili", "luhya_swahili")
     */
    fun detectDialect(text: String): String

    /**
     * Get the appropriate response register for this dialect.
     * Returns a register identifier for the TTS engine.
     */
    fun getResponseRegister(dialect: String): String

    /**
     * Check if the text contains code-switching (multiple languages).
     */
    fun hasCodeSwitching(text: String): Boolean

    /**
     * Get greeting appropriate for this dialect and time of day.
     */
    fun getGreeting(hourOfDay: Int): String

    /**
     * Get acknowledgment appropriate for this dialect.
     * E.g., "Sawa", "Poa", "Siafiri", "Nimeelewa"
     */
    fun getAcknowledgment(): String

    /**
     * Format currency amount in the dialect's style.
     * E.g., "mia tano" vs "five hundred" vs "500 bob"
     */
    fun formatCurrency(amount: Double): String

    /**
     * Get business terminology in the dialect.
     * E.g., "stock" vs "bidhaa" vs "goods"
     */
    fun getBusinessTerm(term: BusinessTerm): String
}

// ── Business Terms ─────────────────────────────────────────────

enum class BusinessTerm {
    SALE,
    PURCHASE,
    PROFIT,
    LOSS,
    CUSTOMER,
    STOCK,
    PRICE,
    EXPENSE,
    REVENUE,
    CASH,
    MPESA,
    RECORD,
    INVENTORY,
    SUPPLIER,
    MARKET
}
