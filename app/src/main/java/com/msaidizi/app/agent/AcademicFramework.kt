package com.msaidizi.app.agent

import android.util.Log

/**
 * AcademicFramework — Maps Valentine's Economics & Statistics degree units
 * to Msaidizi's agent functions.
 *
 * Every piece of advice Msaidizi gives is grounded in academic theory.
 * This framework ensures that agent responses reference the correct
 * economic/statistical concepts, making Msaidizi not just smart but
 * academically rigorous.
 *
 * Based on Valentine Owuor's BSc Economics & Statistics curriculum
 * from Masinde Muliro University — 42 degree units across 4 years,
 * systematically mapped to Angavu Intelligence's four product lines:
 * - Soko Pulse — Market Intelligence
 * - Biashara Pulse — Business Intelligence (AI CFO)
 * - Alama Score — Credit/Reputation Scoring
 * - Jamii Insights — Community Intelligence
 *
 * @author Angavu Intelligence — Implementation Swarm 16 (Academic Wiring)
 */
object AcademicFramework {

    private const val TAG = "AcademicFramework"

    // ── Degree Unit Registry ────────────────────────────────────

    /**
     * All degree units with their mapped functions.
     * Each unit contains concepts that drive specific Msaidizi capabilities.
     */
    val degreeUnits: Map<String, DegreeUnit> = mapOf(

        // ════════════════════════════════════════════════════════════
        // YEAR 1 — FOUNDATION
        // ════════════════════════════════════════════════════════════

        "BCB_108" to DegreeUnit(
            code = "BCB 108",
            name = "Business Communication Skills",
            year = 1,
            concepts = listOf(
                AcademicConcept("Shannon-Weaver Communication Model", "Price reports overcome noise/language barriers", listOf("SOKO_PULSE")),
                AcademicConcept("Information Asymmetry (Akerlof, Spence, Stiglitz)", "Every Angavu product reduces information asymmetry", listOf("ALL")),
                AcademicConcept("Multilingual Code-Switching", "14-dialect voice-first interface handles code-switching", listOf("MSAIDIZI")),
                AcademicConcept("Mechanism Design (Myerson, 1981)", "Alama Score incentivizes honest reporting", listOf("ALAMA_SCORE")),
                AcademicConcept("Digital Communication & AI Etiquette", "Agent outputs match human communication expectations", listOf("MSAIDIZI"))
            ),
            agentBindings = listOf(AgentBinding("ALL", "Communication foundation for all agents"))
        ),

        "ECO_100" to DegreeUnit(
            code = "ECO 100",
            name = "Development Concepts and Application",
            year = 1,
            concepts = listOf(
                AcademicConcept("Institutional Economics (Acemoglu & Robinson)", "Formal institutions are extractive; Angavu bridges the gap", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Capability Approach (Sen, Nussbaum)", "Expand capabilities: information, credit access, market participation", listOf("ALL")),
                AcademicConcept("Endogenous Growth (Romer, Lucas)", "Knowledge IS the product — every transaction creates data", listOf("BIASHARA_PULSE")),
                AcademicConcept("Growth Diagnostics (Hausmann, Rodrik, Velasco)", "Information asymmetry = binding constraint", listOf("ALAMA_SCORE"))
            ),
            agentBindings = listOf(AgentBinding("ADVISOR", "Development context for economic advice"))
        ),

        "ECO_101" to DegreeUnit(
            code = "ECO 101",
            name = "Introduction to Microeconomics",
            year = 1,
            concepts = listOf(
                AcademicConcept("Supply & Demand Equilibrium", "Real-time supply-demand mapping in informal markets", listOf("SOKO_PULSE")),
                AcademicConcept("Consumer Theory (Revealed Preference)", "Model informal worker spending patterns", listOf("BIASHARA_PULSE")),
                AcademicConcept("Production Theory (SFA, DEA)", "Measure vendor efficiency — which mama mboga is on the frontier?", listOf("BIASHARA_PULSE")),
                AcademicConcept("Market Structure (Monopsony, Two-Sided Markets)", "Identify middleman monopsony power over farmers", listOf("SOKO_PULSE")),
                AcademicConcept("Market Failures & Externalities", "Alama Score solves adverse selection in informal credit", listOf("ALAMA_SCORE")),
                AcademicConcept("Search and Matching (Diamond-Mortensen-Pissarides)", "Reduce search costs that create price dispersion", listOf("SOKO_PULSE")),
                AcademicConcept("Behavioral Economics (Kahneman, Tversky)", "Nudges: 'Today's tomato price is 15% cheaper than yesterday'", listOf("MSAIDIZI"))
            ),
            agentBindings = listOf(
                AgentBinding("ADVISOR", "Price analysis, supply/demand insights"),
                AgentBinding("ANALYSIS", "Market equilibrium analysis"),
                AgentBinding("BUSINESS", "Production theory for business optimization")
            )
        ),

        "ECO_102" to DegreeUnit(
            code = "ECO 102",
            name = "Introduction to Macroeconomics",
            year = 1,
            concepts = listOf(
                AcademicConcept("GDP Measurement (SNA 2025)", "Measure informal economy's GDP contribution that KNBS misses", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Money & Banking (MV=PY)", "Track money velocity in informal vs formal markets", listOf("SOKO_PULSE")),
                AcademicConcept("Inflation (Demand-pull, Cost-push)", "Real-time informal market inflation — more current than official CPI", listOf("SOKO_PULSE")),
                AcademicConcept("International Trade (Comparative Advantage)", "Cross-border price intelligence for East African trade", listOf("SOKO_PULSE"))
            ),
            agentBindings = listOf(AgentBinding("ANALYSIS", "Macroeconomic analysis for market context"))
        ),

        "ECO_103" to DegreeUnit(
            code = "ECO 103",
            name = "Introduction to Mathematics for Economists",
            year = 1,
            concepts = listOf(
                AcademicConcept("Optimization (Lagrange, Kuhn-Tucker)", "Profit maximization for informal businesses", listOf("BIASHARA_PULSE")),
                AcademicConcept("Financial Mathematics (PV, Annuities)", "True cost of borrowing — expose shylocking rates (120-360%)", listOf("ALAMA_SCORE")),
                AcademicConcept("Game Theory (Nash Equilibrium)", "Lender-borrower as sequential game with moral hazard", listOf("ALAMA_SCORE")),
                AcademicConcept("Linear Algebra (Leontief Input-Output)", "Market interdependence modeling", listOf("SOKO_PULSE"))
            ),
            agentBindings = listOf(AgentBinding("ANALYSIS", "Mathematical foundations for all analytics"))
        ),

        "STA_142" to DegreeUnit(
            code = "STA 142",
            name = "Probability Theory",
            year = 1,
            concepts = listOf(
                AcademicConcept("Bayes' Theorem", "P(default | transaction history, demographics, social network)", listOf("ALAMA_SCORE")),
                AcademicConcept("Conditional Probability (Markov Chains)", "Business state transitions: growing → stable → declining", listOf("BIASHARA_PULSE")),
                AcademicConcept("Distributions (Exponential Families)", "Price distribution modeling for different goods", listOf("SOKO_PULSE")),
                AcademicConcept("Expected Utility (Von Neumann-Morgenstern)", "Model informal worker decision-making under uncertainty", listOf("MSAIDIZI")),
                AcademicConcept("Law of Large Numbers", "With enough users, aggregate statistics become reliable", listOf("JAMII_INSIGHTS"))
            ),
            agentBindings = listOf(
                AgentBinding("ANALYSIS", "Bayesian inference for worker model"),
                AgentBinding("ADVISOR", "Probability-based risk assessment")
            )
        ),

        "MAT_121" to DegreeUnit(
            code = "MAT 121",
            name = "Differential Calculus",
            year = 1,
            concepts = listOf(
                AcademicConcept("Derivatives (Rate of Change)", "Marginal cost, marginal revenue for business metrics", listOf("BIASHARA_PULSE")),
                AcademicConcept("Optimization (First/Second Order)", "Profit maximization: set MR = MC", listOf("BIASHARA_PULSE")),
                AcademicConcept("Elasticity (Point, Arc)", "Real-time price elasticity dashboards", listOf("SOKO_PULSE")),
                AcademicConcept("Taylor Series", "Price forecasting using local polynomial approximation", listOf("SOKO_PULSE"))
            ),
            agentBindings = listOf(AgentBinding("BUSINESS", "Calculus-based business optimization"))
        ),

        // ════════════════════════════════════════════════════════════
        // YEAR 2 — INTERMEDIATE
        // ════════════════════════════════════════════════════════════

        "ECO_201" to DegreeUnit(
            code = "ECO 201",
            name = "Intermediate Microeconomics",
            year = 2,
            concepts = listOf(
                AcademicConcept("Consumer Theory (Demand Estimation)", "Soko Pulse demand estimation from transaction data", listOf("SOKO_PULSE")),
                AcademicConcept("Producer Theory (Efficiency Analysis)", "Biashara Pulse efficiency analysis for informal businesses", listOf("BIASHARA_PULSE")),
                AcademicConcept("Game Theory (Credit Game Design)", "Alama Score credit game design — sequential games with moral hazard", listOf("ALAMA_SCORE")),
                AcademicConcept("Market Structure Analysis", "Jamii Insights market power measurement", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Cost Optimization", "Production theory applied to informal vendor operations", listOf("BIASHARA_PULSE"))
            ),
            agentBindings = listOf(
                AgentBinding("ADVISOR", "Intermediate economic advice with cost optimization"),
                AgentBinding("BUSINESS", "Producer theory for business efficiency"),
                AgentBinding("ANALYSIS", "Demand estimation and market structure")
            )
        ),

        "ECO_206" to DegreeUnit(
            code = "ECO 206",
            name = "Economics of Microfinance",
            year = 2,
            concepts = listOf(
                AcademicConcept("Group Lending Mechanisms", "Social collateral and peer monitoring for informal lending", listOf("ALAMA_SCORE")),
                AcademicConcept("Interest Rate Determination", "Fair rate calculation vs shylocking exploitation", listOf("ALAMA_SCORE")),
                AcademicConcept("Credit Rationing Theory", "Why informal workers are excluded from formal credit", listOf("ALAMA_SCORE")),
                AcademicConcept("Microfinance Theory", "Alama Score IS microfinance theory applied — alternative data solves exclusion", listOf("ALAMA_SCORE"))
            ),
            agentBindings = listOf(
                AgentBinding("ADVISOR", "Credit readiness assessment, microfinance guidance"),
                AgentBinding("ANALYSIS", "Credit scoring model grounded in microfinance theory")
            )
        ),

        "STA_244" to DegreeUnit(
            code = "STA 244",
            name = "Intro to Time Series Analysis & Forecasting",
            year = 2,
            concepts = listOf(
                AcademicConcept("ARIMA Models", "Price forecasting for agricultural and market goods", listOf("SOKO_PULSE")),
                AcademicConcept("Seasonal Decomposition", "Seasonal price adjustment for agricultural markets", listOf("SOKO_PULSE")),
                AcademicConcept("VAR Models", "Inter-market price transmission analysis", listOf("SOKO_PULSE")),
                AcademicConcept("Cointegration", "Long-run price relationships across markets", listOf("SOKO_PULSE"))
            ),
            agentBindings = listOf(
                AgentBinding("ANALYSIS", "Time series forecasting for price predictions"),
                AgentBinding("ADVISOR", "Seasonal advice based on historical patterns")
            )
        ),

        "ECO_202" to DegreeUnit(
            code = "ECO 202",
            name = "Introduction to Economic Statistics",
            year = 2,
            concepts = listOf(
                AcademicConcept("Descriptive Statistics", "Summary statistics from transaction data", listOf("BIASHARA_PULSE")),
                AcademicConcept("Sampling Design", "Representative user sampling for reliable insights", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Data Quality Assessment", "Handling incomplete records in informal economy", listOf("ALL")),
                AcademicConcept("Correlation Analysis", "Price co-movement across markets", listOf("SOKO_PULSE"))
            ),
            agentBindings = listOf(AgentBinding("ANALYSIS", "Statistical foundations for data analysis"))
        ),

        "ECO_203" to DegreeUnit(
            code = "ECO 203",
            name = "Economic Statistics",
            year = 2,
            concepts = listOf(
                AcademicConcept("Price Indices (Laspeyres, Paasche, Fisher)", "Informal market CPI — Kenya's official CPI misses informal workers", listOf("SOKO_PULSE")),
                AcademicConcept("Time Series Decomposition", "Seasonal price adjustment for agricultural markets", listOf("SOKO_PULSE")),
                AcademicConcept("Regression Analysis", "Impact evaluation of market interventions", listOf("ANALYSIS")),
                AcademicConcept("Hypothesis Testing", "Platform credibility — statistical significance of insights", listOf("ANALYSIS"))
            ),
            agentBindings = listOf(AgentBinding("ANALYSIS", "Economic statistics for market intelligence"))
        ),

        // ════════════════════════════════════════════════════════════
        // YEAR 3 — ADVANCED
        // ════════════════════════════════════════════════════════════

        "ECO_321" to DegreeUnit(
            code = "ECO 321",
            name = "Advanced Microeconomics",
            year = 3,
            concepts = listOf(
                AcademicConcept("Information Economics (Akerlof, Spence, Stiglitz)", "Alama Score IS the solution to adverse selection", listOf("ALAMA_SCORE")),
                AcademicConcept("Mechanism Design", "Platform design that elicits truthful data", listOf("ALAMA_SCORE")),
                AcademicConcept("Behavioral Economics (Nudges)", "Nudges for informal workers: timely, contextual, actionable", listOf("MSAIDIZI")),
                AcademicConcept("Welfare Economics", "Measuring impact of interventions on informal workers", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Adverse Selection & Moral Hazard", "Screening and signaling in informal credit markets", listOf("ALAMA_SCORE"))
            ),
            agentBindings = listOf(
                AgentBinding("ADVISOR", "Information economics for credit and market advice"),
                AgentBinding("ANALYSIS", "Adverse selection detection in markets")
            )
        ),

        "STA_341" to DegreeUnit(
            code = "STA 341",
            name = "Theory of Estimation",
            year = 3,
            concepts = listOf(
                AcademicConcept("Maximum Likelihood Estimation (MLE)", "Credit model parameter estimation", listOf("ALAMA_SCORE")),
                AcademicConcept("Bayesian Estimation", "Alama Score posterior updating with transaction data", listOf("ALAMA_SCORE")),
                AcademicConcept("Confidence Intervals", "Reliability bounds for all Msaidizi predictions", listOf("ANALYSIS")),
                AcademicConcept("Bootstrap Methods", "Robust inference without distributional assumptions", listOf("ANALYSIS"))
            ),
            agentBindings = listOf(
                AgentBinding("ANALYSIS", "Estimation theory for statistical rigor"),
                AgentBinding("ADVISOR", "Confidence intervals in advice: 'I'm 85% confident prices will rise'")
            )
        ),

        "ECO_322" to DegreeUnit(
            code = "ECO 322",
            name = "Advanced Macroeconomics",
            year = 3,
            concepts = listOf(
                AcademicConcept("DSGE Models", "Informal economy dynamics modeling", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Monetary Policy Transmission", "How CBK decisions reach informal markets", listOf("SOKO_PULSE")),
                AcademicConcept("Fiscal Policy Impact", "Government spending effects on informal workers", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Growth Accounting", "Informal sector contribution to national growth", listOf("JAMII_INSIGHTS"))
            ),
            agentBindings = listOf(AgentBinding("ANALYSIS", "Advanced macroeconomic analysis"))
        ),

        // ════════════════════════════════════════════════════════════
        // YEAR 4 — MASTERY
        // ════════════════════════════════════════════════════════════

        "ECO_414" to DegreeUnit(
            code = "ECO 414",
            name = "Introduction to Econometrics",
            year = 4,
            concepts = listOf(
                AcademicConcept("OLS, IV, Panel Data Methods", "Causal inference for impact evaluation", listOf("ANALYSIS")),
                AcademicConcept("Demand Estimation", "Price elasticity and demand curves from transaction data", listOf("SOKO_PULSE")),
                AcademicConcept("Price Transmission Analysis", "How price shocks propagate across markets", listOf("SOKO_PULSE")),
                AcademicConcept("Causal Inference (DID, RDD)", "Proving that Angavu products work", listOf("ALL"))
            ),
            agentBindings = listOf(AgentBinding("ANALYSIS", "Econometric methods for rigorous analysis"))
        ),

        "STA_442" to DegreeUnit(
            code = "STA 442",
            name = "Applied Multivariate Analysis",
            year = 4,
            concepts = listOf(
                AcademicConcept("PCA (Dimension Reduction)", "Credit scoring dimension reduction — reduce borrower characteristics", listOf("ALAMA_SCORE")),
                AcademicConcept("Cluster Analysis", "Market segmentation — group similar informal workers", listOf("JAMII_INSIGHTS")),
                AcademicConcept("Factor Analysis", "Latent economic variables underlying market behavior", listOf("SOKO_PULSE")),
                AcademicConcept("Discriminant Analysis", "Borrower classification — good vs risky", listOf("ALAMA_SCORE"))
            ),
            agentBindings = listOf(AgentBinding("ANALYSIS", "Multivariate methods for advanced analytics"))
        )
    )

    // ── Agent → Academic Unit Mappings ──────────────────────────

    /**
     * Maps each agent type to its primary academic units.
     * Agents reference these units when generating advice.
     */
    val agentAcademicMap: Map<AgentType, List<String>> = mapOf(
        AgentType.ADVISOR to listOf(
            "ECO_101",  // Price analysis, supply/demand
            "ECO_201",  // Cost optimization, production theory
            "ECO_206",  // Credit readiness, microfinance
            "ECO_321",  // Information economics, adverse selection
            "STA_142",  // Bayesian inference for risk assessment
            "BCB_108"   // Communication skills
        ),
        AgentType.ANALYSIS to listOf(
            "STA_244",  // Time series forecasting
            "STA_341",  // Estimation, confidence intervals
            "STA_142",  // Probability theory, Bayesian inference
            "ECO_201",  // Demand estimation
            "ECO_321",  // Adverse selection detection
            "ECO_414",  // Econometric methods
            "STA_442",  // Multivariate analysis
            "ECO_202",  // Economic statistics
            "ECO_203"   // Price indices, regression
        ),
        AgentType.BUSINESS to listOf(
            "ECO_201",  // Cost optimization, production theory
            "ECO_101",  // Supply/demand, market structure
            "MAT_121",  // Calculus-based optimization (MR=MC)
            "ECO_103"   // Financial mathematics
        ),
        AgentType.MARKET to listOf(
            "ECO_101",  // Supply/demand, search costs
            "ECO_102",  // Inflation, money velocity
            "STA_244",  // Price forecasting
            "ECO_203",  // Price indices
            "ECO_414"   // Price transmission
        ),
        AgentType.CREDIT to listOf(
            "ECO_206",  // Microfinance theory
            "ECO_321",  // Information economics (adverse selection)
            "STA_142",  // Bayesian inference for credit scoring
            "STA_341",  // MLE for model parameters
            "ECO_103"   // Game theory (lender-borrower)
        ),
        AgentType.COMMUNITY to listOf(
            "ECO_100",  // Development economics
            "BCB_108",  // Communication
            "STA_142",  // Law of Large Numbers (aggregate reliability)
            "ECO_322"   // Welfare economics
        )
    )

    // ── Product → Academic Unit Mappings ────────────────────────

    /**
     * Maps each Angavu product to its academic foundations.
     * Used for generating product descriptions and training data.
     */
    val productAcademicMap: Map<String, List<String>> = mapOf(
        "SOKO_PULSE" to listOf(
            "ECO_101",  // Supply/demand, search costs
            "ECO_102",  // Inflation, money velocity
            "STA_244",  // Time series forecasting
            "ECO_203",  // Price indices
            "ECO_414",  // Price transmission
            "MAT_121"   // Elasticity
        ),
        "BIASHARA_PULSE" to listOf(
            "ECO_101",  // Production theory, efficiency
            "ECO_201",  // Producer theory, cost optimization
            "MAT_121",  // MR=MC optimization
            "ECO_103",  // Financial mathematics
            "STA_142"   // Business state transitions
        ),
        "ALAMA_SCORE" to listOf(
            "ECO_206",  // Microfinance theory
            "ECO_321",  // Information economics
            "STA_142",  // Bayesian inference
            "STA_341",  // MLE estimation
            "ECO_103",  // Game theory
            "BCB_108"   // Mechanism design
        ),
        "JAMII_INSIGHTS" to listOf(
            "ECO_100",  // Development economics
            "ECO_102",  // GDP measurement
            "ECO_322",  // Welfare economics
            "STA_142",  // Law of Large Numbers
            "ECO_201"   // Market structure analysis
        )
    )

    // ── Core Formulae ───────────────────────────────────────────

    /**
     * Key formulae that agents can reference in their reasoning.
     * Each formula is tagged with the degree unit it comes from.
     */
    val coreFormulae: Map<String, AcademicFormula> = mapOf(
        "bayes_theorem" to AcademicFormula(
            name = "Bayes' Theorem",
            formula = "P(A|B) = P(B|A) × P(A) / P(B)",
            description = "Posterior = Likelihood × Prior / Evidence",
            unitCode = "STA 142",
            application = "Alama Score: P(default | data) = P(data | default) × P(default) / P(data)"
        ),
        "price_elasticity" to AcademicFormula(
            name = "Price Elasticity of Demand",
            formula = "ε = (%ΔQ) / (%ΔP)",
            description = "How sensitive is demand to price changes?",
            unitCode = "MAT 121",
            application = "Soko Pulse: When tomato price rises 10%, demand falls 15% → ε = -1.5 (elastic)"
        ),
        "profit_maximization" to AcademicFormula(
            name = "Profit Maximization",
            formula = "π = TR - TC, optimal where MR = MC",
            description = "Maximize profit by setting marginal revenue equal to marginal cost",
            unitCode = "ECO 201",
            application = "Biashara Pulse: For mama mboga, find the output level where MR = MC"
        ),
        "search_cost_model" to AcademicFormula(
            name = "Search Cost → Price Dispersion",
            formula = "Search costs ↑ → Price dispersion ↑ → Inefficiency ↑",
            description = "Higher search costs mean wider price variation across markets",
            unitCode = "ECO 101",
            application = "Soko Pulse reduces search costs → reduces price dispersion → improves market efficiency"
        ),
        "credit_scoring" to AcademicFormula(
            name = "Bayesian Credit Score",
            formula = "Score = Σ wᵢ × P(default | featureᵢ)",
            description = "Weighted sum of default probabilities given each feature",
            unitCode = "STA 142",
            application = "Alama Score: Combine transaction frequency, repayment history, social network into credit score"
        ),
        "marginal_cost" to AcademicFormula(
            name = "Marginal Cost",
            formula = "MC = dTC/dQ",
            description = "Cost of producing one additional unit",
            unitCode = "MAT 121",
            application = "Biashara Pulse: What's the cost of one more batch of goods for the vendor?"
        ),
        "confidence_interval" to AcademicFormula(
            name = "Confidence Interval",
            formula = "x̄ ± z × (σ/√n)",
            description = "Range where the true value likely falls",
            unitCode = "STA 341",
            application = "Analysis Agent: 'Maize price will be KES 45-55 per kg (95% CI)'"
        )
    )

    // ── API Methods ─────────────────────────────────────────────

    /**
     * Get academic context for an agent type.
     * Returns the degree units and concepts the agent should reference.
     */
    fun getAcademicContext(agentType: AgentType): AcademicContext {
        val unitCodes = agentAcademicMap[agentType] ?: emptyList()
        val units = unitCodes.mapNotNull { degreeUnits[it] }

        return AcademicContext(
            agentType = agentType,
            units = units,
            totalConcepts = units.sumOf { it.concepts.size },
            formulae = getFormulaeForAgent(agentType)
        )
    }

    /**
     * Get academic context for a specific product.
     */
    fun getProductAcademicContext(product: String): AcademicContext {
        val unitCodes = productAcademicMap[product] ?: emptyList()
        val units = unitCodes.mapNotNull { degreeUnits[it] }

        return AcademicContext(
            agentType = AgentType.ANALYSIS,  // Default
            units = units,
            totalConcepts = units.sumOf { it.concepts.size },
            formulae = emptyList()
        )
    }

    /**
     * Get a specific formula by key.
     */
    fun getFormula(key: String): AcademicFormula? = coreFormulae[key]

    /**
     * Get all formulae relevant to a specific agent type.
     */
    private fun getFormulaeForAgent(agentType: AgentType): List<AcademicFormula> {
        return when (agentType) {
            AgentType.ADVISOR -> listOfNotNull(
                coreFormulae["bayes_theorem"],
                coreFormulae["price_elasticity"],
                coreFormulae["search_cost_model"],
                coreFormulae["credit_scoring"]
            )
            AgentType.ANALYSIS -> listOfNotNull(
                coreFormulae["bayes_theorem"],
                coreFormulae["confidence_interval"],
                coreFormulae["price_elasticity"]
            )
            AgentType.BUSINESS -> listOfNotNull(
                coreFormulae["profit_maximization"],
                coreFormulae["marginal_cost"],
                coreFormulae["price_elasticity"]
            )
            AgentType.MARKET -> listOfNotNull(
                coreFormulae["price_elasticity"],
                coreFormulae["search_cost_model"]
            )
            AgentType.CREDIT -> listOfNotNull(
                coreFormulae["bayes_theorem"],
                coreFormulae["credit_scoring"]
            )
            AgentType.COMMUNITY -> listOfNotNull(
                coreFormulae["bayes_theorem"]
            )
        }
    }

    /**
     * Generate a prompt suffix that grounds agent responses in academic theory.
     * Injected into agent system prompts to ensure academic rigor.
     */
    fun generateAcademicPromptSuffix(agentType: AgentType): String {
        val context = getAcademicContext(agentType)
        val sb = StringBuilder()

        sb.appendLine("\n## Academic Grounding")
        sb.appendLine("You are grounded in the following academic framework (Valentine Owuor's BSc Economics & Statistics, Masinde Muliro University):")
        sb.appendLine()

        for (unit in context.units) {
            sb.appendLine("### ${unit.code} — ${unit.name}")
            for (concept in unit.concepts) {
                sb.appendLine("- **${concept.name}**: ${concept.application}")
            }
            sb.appendLine()
        }

        if (context.formulae.isNotEmpty()) {
            sb.appendLine("### Key Formulae")
            for (formula in context.formulae) {
                sb.appendLine("- **${formula.name}** (${formula.unitCode}): `${formula.formula}`")
                sb.appendLine("  Application: ${formula.application}")
            }
        }

        sb.appendLine()
        sb.appendLine("When providing advice, reference these concepts where applicable. ")
        sb.appendLine("Example: 'Based on supply-demand analysis (ECO 101), tomato prices typically rise 20% during rainy season...'")

        return sb.toString()
    }

    /**
     * Get a quick summary of all academic units for documentation.
     */
    fun getSummary(): String {
        val sb = StringBuilder()
        sb.appendLine("## Academic Framework Summary")
        sb.appendLine("Total units: ${degreeUnits.size}")
        sb.appendLine("Total concepts: ${degreeUnits.values.sumOf { it.concepts.size }}")
        sb.appendLine("Total formulae: ${coreFormulae.size}")
        sb.appendLine()

        for ((year, units) in degreeUnits.values.groupBy { it.year }.toSortedMap()) {
            sb.appendLine("### Year $year")
            for (unit in units) {
                sb.appendLine("- ${unit.code}: ${unit.name} (${unit.concepts.size} concepts)")
            }
            sb.appendLine()
        }

        return sb.toString()
    }
}

// ── Data Classes ───────────────────────────────────────────────

/**
 * Represents a complete degree unit with its academic concepts.
 */
data class DegreeUnit(
    val code: String,
    val name: String,
    val year: Int,
    val concepts: List<AcademicConcept>,
    val agentBindings: List<AgentBinding> = emptyList()
)

/**
 * A single academic concept mapped to Msaidizi products.
 */
data class AcademicConcept(
    val name: String,
    val application: String,
    val products: List<String>  // Which Angavu products use this concept
)

/**
 * Binds an academic unit to a specific agent.
 */
data class AgentBinding(
    val agentId: String,        // Agent type or "ALL"
    val reason: String          // Why this unit is relevant to this agent
)

/**
 * A mathematical formula with its academic source and practical application.
 */
data class AcademicFormula(
    val name: String,
    val formula: String,
    val description: String,
    val unitCode: String,       // Which degree unit this comes from
    val application: String     // How Msaidizi uses this formula
)

/**
 * Academic context provided to an agent for grounded responses.
 */
data class AcademicContext(
    val agentType: AgentType,
    val units: List<DegreeUnit>,
    val totalConcepts: Int,
    val formulae: List<AcademicFormula>
)

/**
 * Agent types in the Msaidizi system.
 */
enum class AgentType {
    ADVISOR,    // Economic advice to workers
    ANALYSIS,   // Statistical analysis and forecasting
    BUSINESS,   // Business optimization (AI CFO)
    MARKET,     // Market intelligence (Soko Pulse)
    CREDIT,     // Credit scoring (Alama Score)
    COMMUNITY   // Community intelligence (Jamii Insights)
}
