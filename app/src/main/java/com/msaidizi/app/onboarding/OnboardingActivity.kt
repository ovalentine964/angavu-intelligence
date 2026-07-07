package com.msaidizi.app.onboarding

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import android.view.View
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.google.android.material.progressindicator.LinearProgressIndicator
import com.msaidizi.app.MainActivity
import com.msaidizi.app.R
import com.msaidizi.app.core.dialect.DialectAdapterFactory
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import java.util.Locale

/**
 * OnboardingActivity — Msaidizi meets the worker for the first time.
 *
 * Valentine's vision: "First launch should be different, not OpenClaw framework
 * bootstrap but specification to Msaidizi. Msaidizi gets to know the informal
 * worker well."
 *
 * This is NOT a setup wizard. This is Msaidizi meeting your mum for the first time.
 * It should feel like meeting a helpful friend who happens to be really good with numbers.
 * Voice-first, warm, natural, in her language.
 *
 * Flow:
 * Phase 1: Introduction (30s) — Msaidizi introduces herself, asks for names
 * Phase 2: Getting to Know You (2-3 min) — Business type, location, hours
 * Phase 3: Understanding Your Business (2-3 min) — Supply chain, payments, challenges
 * Phase 4: Setting Up (1-2 min) — Permissions, model download in background
 * Phase 5: First Value (immediate) — First insight based on what we learned
 *
 * Total time: ~7-10 minutes of natural conversation
 * Technical knowledge required: Zero
 *
 * @author Angavu Intelligence — Implementation Swarm 9
 */
class OnboardingActivity : AppCompatActivity() {

    private val viewModel: OnboardingViewModel by viewModels()

    // Voice components
    private var speechRecognizer: SpeechRecognizer? = null
    private var tts: TextToSpeech? = null
    private var isTtsReady = false

    // UI components
    private lateinit var progressIndicator: LinearProgressIndicator
    private lateinit var voiceButton: View
    private lateinit var statusText: View

    // Current conversation state
    private var currentResponseType: ResponseType = ResponseType.FREE_TEXT
    private var selectedLanguage: Language = Language.KISWAHILI

    // ── Permission Handling ────────────────────────────────────

    private val audioPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            initializeSpeechRecognizer()
        } else {
            // Gentle nudge — not an error
            Toast.makeText(this, "Sauti inahitajika kwa Msaidizi kukusaidia vizuri zaidi", Toast.LENGTH_LONG).show()
        }
    }

    // ── Lifecycle ──────────────────────────────────────────────

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_onboarding)

        // Initialize UI
        setupUI()

        // Initialize TTS
        initializeTTS()

        // Request audio permission
        requestAudioPermission()

        // Observe ViewModel state
        observeViewModel()

        // Start the conversation
        // (ViewModel starts automatically in init block)
    }

    override fun onDestroy() {
        speechRecognizer?.destroy()
        tts?.shutdown()
        super.onDestroy()
    }

    // ── UI Setup ───────────────────────────────────────────────

    private fun setupUI() {
        progressIndicator = findViewById(R.id.progress_onboarding)
        voiceButton = findViewById(R.id.btn_voice_input)
        statusText = findViewById(R.id.text_status)

        // Voice button — tap to speak
        voiceButton.setOnClickListener {
            if (viewModel.isListening.value == true) {
                stopListening()
            } else {
                startListening()
            }
        }

        // Progress indicator
        progressIndicator.max = 100
        progressIndicator.progress = 0
    }

    // ── ViewModel Observation ──────────────────────────────────

    private fun observeViewModel() {
        // Observe Msaidizi's messages
        viewModel.msaidiziMessage.observe(this) { message ->
            if (message != null) {
                displayMessage(message)
                speakMessage(message.text)
                currentResponseType = message.responseType

                // Update progress based on phase
                updateProgress(message.phase)
            }
        }

        // Observe current phase
        viewModel.currentPhase.observe(this) { phase ->
            updatePhaseUI(phase)
        }

        // Observe listening state
        viewModel.isListening.observe(this) { isListening ->
            updateListeningUI(isListening)
        }

        // Observe model download progress
        lifecycleScope.launch {
            viewModel.modelDownloadProgress.collectLatest { progress ->
                updateDownloadProgress(progress)
            }
        }

        // Observe model download state
        lifecycleScope.launch {
            viewModel.modelDownloadState.collectLatest { state ->
                updateDownloadStateUI(state)
            }
        }

        // Observe onboarding completion
        viewModel.onboardingComplete.observe(this) { isComplete ->
            if (isComplete) {
                onOnboardingComplete()
            }
        }

        // Observe first insight
        viewModel.firstInsight.observe(this) { insight ->
            if (insight != null) {
                displayInsight(insight)
            }
        }
    }

    // ── Message Display ────────────────────────────────────────

    private fun displayMessage(message: ConversationMessage) {
        // In a real implementation, this would update a RecyclerView
        // with chat bubbles. For now, we update the main text view.
        val messageView = findViewById<android.widget.TextView>(R.id.text_msaidizi_message)
        messageView?.text = message.text

        // Show translation if available
        val translationView = findViewById<android.widget.TextView>(R.id.text_translation)
        if (message.translation.isNotEmpty()) {
            translationView?.text = message.translation
            translationView?.visibility = View.VISIBLE
        } else {
            translationView?.visibility = View.GONE
        }

        // Show response type indicator
        if (message.expectsResponse) {
            showResponseOptions(message.responseType)
        }
    }

    private fun displayInsight(insight: String) {
        // Highlight the first insight with special styling
        val insightView = findViewById<android.widget.TextView>(R.id.text_insight)
        insightView?.text = insight
        insightView?.visibility = View.VISIBLE
    }

    // ── Voice Input ────────────────────────────────────────────

    private fun initializeSpeechRecognizer() {
        if (!SpeechRecognizer.isRecognitionAvailable(this)) {
            Toast.makeText(this, "Usikilizaji wa sauti haupatikani", Toast.LENGTH_SHORT).show()
            return
        }

        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this).apply {
            setRecognitionListener(object : RecognitionListener {
                override fun onReadyForSpeech(params: Bundle?) {
                    statusText.post { (statusText as? android.widget.TextView)?.text = "Sikiliza..." }
                }

                override fun onBeginningOfSpeech() {}
                override fun onRmsChanged(rmsdB: Float) {}
                override fun onBufferReceived(buffer: ByteArray?) {}
                override fun onEndOfSpeech() {
                    statusText.post { (statusText as? android.widget.TextView)?.text = "Naelewa..." }
                }

                override fun onError(error: Int) {
                    statusText.post { (statusText as? android.widget.TextView)?.text = "Jaribu tena..." }
                }

                override fun onResults(results: Bundle?) {
                    val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                    if (!matches.isNullOrEmpty()) {
                        val recognizedText = matches[0]
                        processWorkerResponse(recognizedText)
                    }
                }

                override fun onPartialResults(partialResults: Bundle?) {}
                override fun onEvent(eventType: Int, params: Bundle?) {}
            })
        }
    }

    private fun startListening() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED) {
            requestAudioPermission()
            return
        }

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, getLocaleForLanguage(selectedLanguage))
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
        }

        speechRecognizer?.startListening(intent)
    }

    private fun stopListening() {
        speechRecognizer?.stopListening()
    }

    private fun processWorkerResponse(text: String) {
        // Detect dialect from the response
        val dialect = viewModel.detectDialect(text)
        val dialectAdapter = DialectAdapterFactory.create(selectedLanguage)

        // Process based on current response type
        when (currentResponseType) {
            ResponseType.AGENT_NAMING -> {
                // Extract the name from the response
                val name = extractName(text)
                viewModel.onAgentNamed(name)
            }
            ResponseType.WORKER_NAME -> {
                val name = extractName(text)
                viewModel.onWorkerNamed(name)
            }
            ResponseType.BUSINESS_TYPE -> {
                val type = classifyBusinessType(text)
                viewModel.onBusinessTypeSelected(type, text)
            }
            ResponseType.WORK_LOCATION -> {
                val location = classifyWorkLocation(text)
                viewModel.onWorkLocationSelected(location, extractMarketName(text))
            }
            ResponseType.WORK_SCHEDULE -> {
                val schedule = parseWorkSchedule(text)
                viewModel.onWorkScheduleSet(schedule)
            }
            ResponseType.TEAM_SIZE -> {
                val worksAlone = !text.contains("mtu") && !text.contains("watu") && !text.contains("people")
                val teamSize = if (worksAlone) 1 else extractTeamSize(text)
                viewModel.onTeamSizeAnswered(worksAlone, teamSize)
            }
            ResponseType.SUPPLY_CHAIN -> {
                val supplyChain = parseSupplyChain(text)
                viewModel.onSupplyChainAnswered(supplyChain)
            }
            ResponseType.CUSTOMER_ACQUISITION -> {
                val acquisition = parseCustomerAcquisition(text)
                viewModel.onCustomerAcquisitionAnswered(acquisition)
            }
            ResponseType.PAYMENT_METHODS -> {
                val methods = parsePaymentMethods(text)
                viewModel.onPaymentMethodsAnswered(methods)
            }
            ResponseType.RECORD_KEEPING -> {
                val recordKeeping = parseRecordKeeping(text)
                viewModel.onRecordKeepingAnswered(recordKeeping)
            }
            ResponseType.BIGGEST_CHALLENGE -> {
                val category = classifyChallenge(text)
                viewModel.onBiggestChallengeAnswered(text, category)
            }
            ResponseType.VOICE_PERMISSION -> {
                // Check if the response is affirmative
                if (isAffirmative(text)) {
                    viewModel.onVoicePermissionGranted()
                }
            }
            ResponseType.NOTIFICATION_TIME -> {
                val time = parseNotificationTime(text)
                viewModel.onNotificationTimeSet(time)
            }
            ResponseType.FREE_TEXT -> {
                // General conversation — pass to ViewModel for processing
            }
        }
    }

    // ── Text-to-Speech ─────────────────────────────────────────

    private fun initializeTTS() {
        tts = TextToSpeech(this) { status ->
            if (status == TextToSpeech.SUCCESS) {
                isTtsReady = true
                updateTTSLanguage(selectedLanguage)
            }
        }
    }

    private fun speakMessage(text: String) {
        if (!isTtsReady) return

        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "msaidizi_message")
    }

    private fun updateTTSLanguage(language: Language) {
        val locale = when (language) {
            Language.KISWAHILI -> Locale("sw", "KE")
            Language.ENGLISH -> Locale.US
            Language.AMHARIC -> Locale("am", "ET")
            Language.HAUSA -> Locale("ha", "NG")
            Language.YORUBA -> Locale("yo", "NG")
            Language.IGBO -> Locale("ig", "NG")
            Language.ZULU -> Locale("zu", "ZA")
            Language.XHOSA -> Locale("xh", "ZA")
            Language.KINYARWANDA -> Locale("rw", "RW")
            Language.LINGALA -> Locale("ln", "CD")
            Language.SHONA -> Locale("sn", "ZW")
            Language.LUGANDA -> Locale("lg", "UG")
            Language.SOMALI -> Locale("so", "SO")
            Language.PORTUGUESE -> Locale("pt", "MZ")
        }
        tts?.language = locale
    }

    // ── Response Processing Helpers ────────────────────────────

    private fun extractName(text: String): String {
        // Simple name extraction — take the first meaningful word
        // In production, this would use NLP
        return text.trim().split("\\s+".toRegex()).firstOrNull() ?: text
    }

    private fun classifyBusinessType(text: String): BusinessType {
        val lower = text.lowercase()
        return when {
            lower.contains("rejareja") || lower.contains("retail") || lower.contains("duka") -> BusinessType.RETAIL
            lower.contains("mama mboga") || lower.contains("chakula") || lower.contains("food") || lower.contains("nyanya") -> BusinessType.FOOD
            lower.contains("boda") || lower.contains("transport") || lower.contains("tuk tuk") -> BusinessType.TRANSPORT
            lower.contains("saluni") || lower.contains("salon") || lower.contains("huduma") || lower.contains("service") -> BusinessType.SERVICES
            lower.contains("ufundi") || lower.contains("manufacturing") || lower.contains("maker") -> BusinessType.MANUFACTURING
            lower.contains("kilimo") || lower.contains("agriculture") || lower.contains("farming") -> BusinessType.AGRICULTURE
            else -> BusinessType.UNKNOWN
        }
    }

    private fun classifyWorkLocation(text: String): WorkLocation {
        val lower = text.lowercase()
        return when {
            lower.contains("soko") || lower.contains("market") -> WorkLocation.MARKET
            lower.contains("barabara") || lower.contains("roadside") || lower.contains("njia") -> WorkLocation.ROADSIDE
            lower.contains("nyumba") || lower.contains("home") || lower.contains("ndani") -> WorkLocation.HOME
            lower.contains("zunguka") || lower.contains("mobile") || lower.contains("nitembeze") -> WorkLocation.MOBILE
            lower.contains("duka") || lower.contains("shop") -> WorkLocation.SHOP
            else -> WorkLocation.UNKNOWN
        }
    }

    private fun extractMarketName(text: String): String {
        // Try to extract market name from text
        // e.g., "Soko la Gikomba" -> "Gikomba"
        val marketPatterns = listOf("soko la", "soko", "market", "katika")
        for (pattern in marketPatterns) {
            val index = text.lowercase().indexOf(pattern)
            if (index >= 0) {
                val after = text.substring(index + pattern.length).trim()
                if (after.isNotEmpty()) {
                    return after.split("\\s+".toRegex()).firstOrNull() ?: after
                }
            }
        }
        return ""
    }

    private fun parseWorkSchedule(text: String): WorkSchedule {
        val lower = text.lowercase()
        return WorkSchedule(
            morning = lower.contains("asubuhi") || lower.contains("morning"),
            afternoon = lower.contains("mchana") || lower.contains("afternoon"),
            evening = lower.contains("jioni") || lower.contains("evening"),
            night = lower.contains("usiku") || lower.contains("night"),
            daysPerWeek = extractDaysPerWeek(text)
        )
    }

    private fun extractDaysPerWeek(text: String): Int {
        val lower = text.lowercase()
        return when {
            lower.contains("kila siku") || lower.contains("every day") || lower.contains("7") -> 7
            lower.contains("6") || lower.contains("jumamosi") || lower.contains("saturday") -> 6
            lower.contains("5") || lower.contains("wiki") || lower.contains("week") -> 5
            else -> 6  // Default: 6 days
        }
    }

    private fun extractTeamSize(text: String): Int {
        // Try to extract number from text
        val numbers = "\\d+".toRegex().findAll(text).map { it.value.toInt() }.toList()
        return numbers.firstOrNull() ?: 2  // Default: 2 if they mentioned others
    }

    private fun parseSupplyChain(text: String): SupplyChain {
        val lower = text.lowercase()
        val sourceType = when {
            lower.contains("ghala") || lower.contains("wholesale") -> SupplySourceType.WHOLESALE
            lower.contains("mkulima") || lower.contains("farmer") -> SupplySourceType.FARMER
            lower.contains("dalali") || lower.contains("middleman") -> SupplySourceType.MIDDLEMAN
            lower.contains("mtengenezaji") || lower.contains("manufacturer") -> SupplySourceType.MANUFACTURER
            else -> SupplySourceType.UNKNOWN
        }
        return SupplyChain(sourceType = sourceType)
    }

    private fun parseCustomerAcquisition(text: String): CustomerAcquisition {
        val lower = text.lowercase()
        return CustomerAcquisition(
            walkIn = lower.contains("wanakuja") || lower.contains("walk") || lower.contains("mwenyewe"),
            referrals = lower.contains("rafiki") || lower.contains("referral") || lower.contains("recommend"),
            socialMedia = lower.contains("mitandao") || lower.contains("social") || lower.contains("facebook") || lower.contains("whatsapp")
        )
    }

    private fun parsePaymentMethods(text: String): PaymentMethods {
        val lower = text.lowercase()
        val hasMpesa = lower.contains("mpesa") || lower.contains("m-pesa") || lower.contains("pesa ya simu")
        val hasCash = lower.contains("taslimu") || lower.contains("cash") || lower.contains("pesa")
        return PaymentMethods(
            mpesa = hasMpesa,
            cash = hasCash,
            both = hasMpesa && hasCash
        )
    }

    private fun parseRecordKeeping(text: String): RecordKeeping {
        val lower = text.lowercase()
        val method = when {
            lower.contains("daftari") || lower.contains("notebook") || lower.contains("andika") -> RecordMethod.NOTEBOOK
            lower.contains("simu") || lower.contains("phone") || lower.contains("app") -> RecordMethod.PHONE
            lower.contains("kichwani") || lower.contains("memory") || lower.contains("nakumbuka") -> RecordMethod.MEMORY
            lower.contains("mtu mwingine") || lower.contains("someone") -> RecordMethod.SOMEONE_ELSE
            else -> RecordMethod.NONE
        }
        return RecordKeeping(
            method = method,
            tracksSales = method != RecordMethod.NONE,
            tracksExpenses = method == RecordMethod.NOTEBOOK || method == RecordMethod.PHONE,
            knowsProfit = lower.contains("faida") || lower.contains("profit")
        )
    }

    private fun classifyChallenge(text: String): ChallengeCategory {
        val lower = text.lowercase()
        return when {
            lower.contains("mtaji") || lower.contains("capital") || lower.contains("pesa") -> ChallengeCategory.CAPITAL
            lower.contains("stock") || lower.contains("bidhaa") || lower.contains("inventory") -> ChallengeCategory.INVENTORY
            lower.contains("wateja") || lower.contains("customer") || lower.contains("mteja") -> ChallengeCategory.CUSTOMERS
            lower.contains("shindani") || lower.contains("competitor") || lower.contains("competition") -> ChallengeCategory.COMPETITION
            lower.contains("rekodi") || lower.contains("record") || lower.contains("sijui faida") -> ChallengeCategory.RECORDS
            lower.contains("wizi") || lower.contains("theft") || lower.contains("potea") -> ChallengeCategory.THEFT_LOSS
            lower.contains("bei") || lower.contains("price") || lower.contains("pricing") -> ChallengeCategory.PRICING
            lower.contains("usafiri") || lower.contains("transport") -> ChallengeCategory.TRANSPORT
            else -> ChallengeCategory.UNKNOWN
        }
    }

    private fun isAffirmative(text: String): Boolean {
        val lower = text.lowercase()
        return lower.contains("ndiyo") || lower.contains("sawa") || lower.contains("yes") ||
                lower.contains("poa") || lower.contains("safi") || lower.contains("siafiri") ||
                lower.contains("sawa") || lower.contains("naomba") || lower.contains("ataka")
    }

    private fun parseNotificationTime(text: String): String {
        val lower = text.lowercase()
        return when {
            lower.contains("saa moja") || lower.contains("7") || lower.contains("saba") -> "07:00"
            lower.contains("saa mbili") || lower.contains("8") || lower.contains("nane") -> "08:00"
            lower.contains("saa tatu") || lower.contains("9") || lower.contains("tisa") -> "09:00"
            lower.contains("saa sita") || lower.contains("6") || lower.contains("sita") -> "06:00"
            else -> "07:00"  // Default: 7am
        }
    }

    // ── UI Updates ─────────────────────────────────────────────

    private fun updateProgress(phase: OnboardingPhase) {
        val progress = when (phase) {
            OnboardingPhase.INTRODUCTION -> 10
            OnboardingPhase.GETTING_TO_KNOW -> 30
            OnboardingPhase.UNDERSTANDING_BUSINESS -> 60
            OnboardingPhase.SETTING_UP -> 80
            OnboardingPhase.FIRST_VALUE -> 95
        }
        progressIndicator.progress = progress
    }

    private fun updatePhaseUI(phase: OnboardingPhase) {
        val phaseText = when (phase) {
            OnboardingPhase.INTRODUCTION -> "Tunajuliana..."
            OnboardingPhase.GETTING_TO_KNOW -> "Najifunza kuhusu biashara yako..."
            OnboardingPhase.UNDERSTANDING_BUSINESS -> "Naelewa biashara yako zaidi..."
            OnboardingPhase.SETTING_UP -> "Najiandaa kukusaidia..."
            OnboardingPhase.FIRST_VALUE -> "Tayari!"
        }
        (statusText as? android.widget.TextView)?.text = phaseText
    }

    private fun updateListeningUI(isListening: Boolean) {
        voiceButton.isSelected = isListening
        val buttonLabel = if (isListening) "Sikiliza..." else "Sema na Msaidizi"
        (voiceButton as? android.widget.TextView)?.text = buttonLabel
    }

    private fun updateDownloadProgress(progress: Float) {
        // Update download progress bar
        val downloadProgress = findViewById<LinearProgressIndicator>(R.id.progress_model_download)
        downloadProgress?.progress = (progress * 100).toInt()
    }

    private fun updateDownloadStateUI(state: ModelDownloadState) {
        val downloadStatus = findViewById<android.widget.TextView>(R.id.text_download_status)
        when (state) {
            ModelDownloadState.NOT_STARTED -> {
                downloadStatus?.text = ""
                downloadStatus?.visibility = View.GONE
            }
            ModelDownloadState.DOWNLOADING_WHISPER -> {
                downloadStatus?.text = "Ninajifunza lugha yako..."
                downloadStatus?.visibility = View.VISIBLE
            }
            ModelDownloadState.DOWNLOADING_QWEN -> {
                downloadStatus?.text = "Ninajifunza kufikiri..."
                downloadStatus?.visibility = View.VISIBLE
            }
            ModelDownloadState.DOWNLOADING_TTS -> {
                downloadStatus?.text = "Ninajifunza kuzungumza..."
                downloadStatus?.visibility = View.VISIBLE
            }
            ModelDownloadState.DOWNLOADING -> {
                downloadStatus?.text = "Najiandaa..."
                downloadStatus?.visibility = View.VISIBLE
            }
            ModelDownloadState.COMPLETED -> {
                downloadStatus?.text = "Tayari!"
                downloadStatus?.visibility = View.VISIBLE
            }
            ModelDownloadState.FAILED -> {
                downloadStatus?.text = "Jaribu tena baadaye"
                downloadStatus?.visibility = View.VISIBLE
            }
        }
    }

    private fun showResponseOptions(responseType: ResponseType) {
        // Show appropriate response options based on type
        // This could be chips, buttons, or free text input
        when (responseType) {
            ResponseType.AGENT_NAMING -> {
                // Show naming dialog
                val dialog = AgentNamingDialog.newInstance(selectedLanguage) { name ->
                    viewModel.onAgentNamed(name)
                }
                dialog.show(supportFragmentManager, "agent_naming")
            }
            ResponseType.BUSINESS_TYPE -> {
                // Show business type chips
                showBusinessTypeChips()
            }
            ResponseType.VOICE_PERMISSION -> {
                // Show permission confirmation
                showPermissionConfirmation()
            }
            else -> {
                // Free text — just show voice button
            }
        }
    }

    private fun showBusinessTypeChips() {
        // In a real implementation, this would show a ChipGroup
        // with business type options
    }

    private fun showPermissionConfirmation() {
        // Show a friendly confirmation dialog for voice permission
    }

    // ── Navigation ─────────────────────────────────────────────

    private fun onOnboardingComplete() {
        // Transition to main activity
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        startActivity(intent)
        finish()
    }

    // ── Utility ────────────────────────────────────────────────

    private fun getLocaleForLanguage(language: Language): String {
        return when (language) {
            Language.KISWAHILI -> "sw-KE"
            Language.ENGLISH -> "en-US"
            Language.AMHARIC -> "am-ET"
            Language.HAUSA -> "ha-NG"
            Language.YORUBA -> "yo-NG"
            Language.IGBO -> "ig-NG"
            Language.ZULU -> "zu-ZA"
            Language.XHOSA -> "xh-ZA"
            Language.KINYARWANDA -> "rw-RW"
            Language.LINGALA -> "ln-CD"
            Language.SHONA -> "sn-ZW"
            Language.LUGANDA -> "lg-UG"
            Language.SOMALI -> "so-SO"
            Language.PORTUGUESE -> "pt-MZ"
        }
    }

    private fun requestAudioPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED) {
            audioPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
        } else {
            initializeSpeechRecognizer()
        }
    }
}
