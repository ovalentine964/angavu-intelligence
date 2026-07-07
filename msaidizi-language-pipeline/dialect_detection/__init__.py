"""
Dialect Detection Module for Msaidizi
=====================================

Detects which of 14+ dialects/languages a user is speaking using a
multi-signal approach:

1. **Lexical analysis** — Sheng slang, regional vocabulary, borrowed words
2. **Phonological features** — Tonal patterns, vowel harmony, consonant clusters
3. **Morphological markers** — Bantu noun class prefixes, verb extensions
4. **Syntactic patterns** — Word order, code-switching boundaries
5. **N-gram language models** — Statistical dialect classification
6. **Context from user history** — Previous dialect choices, location, demographics

The detector uses a lightweight classifier that runs on-device, combined
with a rule-based system for high-confidence lexical markers.

Architecture:
  Text/Audio → Feature Extraction → Ensemble Classifier → Dialect Label + Confidence

For code-switched input (e.g., Swahili-English-Sheng), the detector
returns the PRIMARY dialect plus detected secondary languages with boundaries.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class LanguageFamily(Enum):
    """Language families for cross-lingual transfer."""
    BANTU_EAST = "bantu_east"
    BANTU_SHENG = "bantu_sheng"
    NILOTIC = "nilotic"
    CUSHITIC = "cushitic"
    AFROASIATIC_SEMITIC = "afroasiatic_semitic"
    AFROASIATIC_CHADIC = "afroasiatic_chadic"
    NIGER_CONGO_YORUBOID = "niger_congo_yoruboid"
    NIGER_CONGO_IGBO = "niger_congo_igbo"
    ENGLISH = "english"
    UNKNOWN = "unknown"


@dataclass
class DialectResult:
    """Result of dialect detection."""
    primary_dialect: str
    primary_confidence: float
    secondary_dialects: List[Tuple[str, float]]  # (dialect, confidence)
    language_family: LanguageFamily
    code_switch_segments: List[CodeSwitchSegment] = field(default_factory=list)
    is_code_switched: bool = False
    features_used: List[str] = field(default_factory=list)
    raw_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class CodeSwitchSegment:
    """A segment of text identified as belonging to a specific language."""
    text: str
    start_offset: int
    end_offset: int
    language: str
    confidence: float


# ─────────────────────────────────────────────────────────────────────
# Lexical markers — the fastest, most reliable signal for African dialects
# ─────────────────────────────────────────────────────────────────────

# Sheng is a rapidly evolving slang continuum. These are stable markers.
SHENG_MARKERS = {
    # Core Sheng vocabulary (Nairobi)
    "niaje", "sasa", "poa", "fiti", "ndeio", "mbogi", "mzinga",
    "ndelevu", "chipo", "mzingo", "ndege", "guoko", "nduthi",
    "kasongo", "kanairo", "mathree", "nganya", "kanyangi",
    "mresh", "ushago", "mazishi", "kuomoka", "ndula", "mjango",
    "wamlambez", "wamyamaza", "kibao", "mzinga", "ndelevu",
    "maandamano", "kuhepa", "kuboo", "kudinya", "kuchoma",
    # Sheng verb forms
    "naskia", "najua", "nafeel", "nathink", "naget", "narada",
    # Code-mixed Sheng-English
    "ata si", "kwani ni", "bado niko", "sijui aje",
}

# Coastal Swahili markers — distinct from standard/nairobi
COASTAL_SWAHILI_MARKERS = {
    "wapya", "habari za", "mambo vipi", "poa sana",
    "shwari", "salama", "uhali gani", "hujambo",
    "sijambo", "nzuri", "fika", "karibu", "asante sana",
    "la hila", "maulana", "bwana", "mzee", "dada",
    # Arabic-influenced vocabulary
    "inshallah", "mashallah", "wallahi", "habibi",
    "haram", "halal", "duka", "soko", "bandari",
    # Coastal distinctives
    "pwani", "bahari", "dhow", "jahazi", "mtego",
}

# Inland/upcountry Swahili
INLAND_SWAHILI_MARKERS = {
    "sawa", "vizuri", "nzuri sana", "twende",
    "haraka", "pole pole", "chap chap",
    "maji", "njaa", "kazi", "shamba", "boma",
}

# Kikuyu-influenced Swahili — Bantu morphological mixing
KIKUYU_SWAHILI_MARKERS = {
    "ni", "ndio", "wĩ", "atuĩte", "tũkũũka",
    "mwĩhĩ", "mũtũmĩa", "kĩhĩ", "gĩkũyũ",
    "ngai", "njĩra", "mũciĩ", "rũgendo",
    # Kikuyu-influenced Swahili constructions
    "ni kweli", "ata sisi", "tuko hapa", "twende nyumbani",
}

# Dholuo-influenced Swahili
DHOLOU_SWAHILI_MARKERS = {
    "nyako", "otenga", "mikayi", "jaowi", "dhi",
    "koro", "nade", "yawa", "apwoyo", "chuth",
    "nyar", "achieng", "odongo", "omondi", "ongeri",
    # Luo-influenced Swahili
    "in gi", "to gi", "maber", "ber",
}

# Yoruba markers
YORUBA_MARKERS = {
    "bawo", "se daadaa", "e ku", "o dara", "e se",
    "mo n lo", "o ti", "ki ni", "nibo", "bawo ni",
    "ẹ", "ọ", "ṣ", "ọ̀", "à", "ń",
    "abi", "sha", "jare", "shey", "wahala",
}

# Hausa markers
HAUSA_MARKERS = {
    "sannu", "yaya", "lafiya", "na gode", "in sha allah",
    "kai", "tafiya", "gida", "abinci", "ruwa",
    "ba", "da", "ne", "ce", "wannan",
}

# Amharic markers (Ge'ez script detection is primary signal)
AMHARIC_MARKERS = {
    # Amharic uses Ge'ez script — Unicode range U+1200-U+137F
    # Romanized markers for when users type in Latin script
    "selam", "tena yistilign", "ameseginalehu",
    "dehna", "eh", "aw", "shi",
}

# Zulu markers
ZULU_MARKERS = {
    "sawubona", "unjani", "ngiyabonga", "yebo",
    "ngikhona", "hamba", "khuluma", "dlala",
    "umuntu", "isizulu", "ubuntu",
    # Zulu click consonants (represented in Latin)
    "q", "x", "c",  # These are click consonants in Zulu
}

# Xhosa markers
XHOSA_MARKERS = {
    "molo", "unjani", "enkosi", "ewe",
    "ndiyaphila", "hamba", "thetha", "dlala",
    "ubuntu", "isixhosa",
}

# Igbo markers
IGBO_MARKERS = {
    "ndewo", "kedu", "daalu", "o di mma",
    "biko", "nke", "ya", "anyi", "unu",
    "igbo", "oha", "ala",
}

# Maasai markers
MAASAI_MARKERS = {
    "sopa", "yeyo", "tiniki", "keju",
    "enkai", "oleng", "enkitok", "ilmurran",
    "enkang", "olchani",
}

# Somali markers
SOMALI_MARKERS = {
    "is ka warran", "nabad", "mahadsanid",
    "waan", "waa", "wuxuu", "gabadh",
    "soomaali", "muqdisho", "hargeisa",
}

# Luhya markers
LUHYA_MARKERS = {
    "mulembe", "oli khayi", "nende",
    "mukhulungwa", "omukulu", "omukhana",
    "luyia", "oluluyia",
}

# Kalenjin markers
KALENJIN_MARKERS = {
    "mising", "chamgei", "kamnywal",
    "kipsigis", "nandi", "tugen",
    "kalee", "amen",
}


# ─────────────────────────────────────────────────────────────────────
# Dialect Classifier — multi-signal ensemble
# ─────────────────────────────────────────────────────────────────────

@dataclass
class DialectClassifier:
    """
    Multi-signal dialect classifier for 14+ African dialects.

    Signals:
    1. Lexical marker matching (fastest, most reliable for Sheng/regional)
    2. Script detection (Ge'ez for Amharic, click consonants for Zulu/Xhosa)
    3. N-gram statistical model (learned from training data)
    4. Morphological analysis (Bantu noun classes, verb extensions)
    5. Context from user history

    The ensemble weights are:
    - Lexical: 0.35 (instant, reliable for distinct dialects)
    - Script/phonological: 0.25 (strong signal for distinct scripts)
    - N-gram LM: 0.25 (statistical backbone)
    - Morphological: 0.10 (supplementary for Bantu languages)
    - Context: 0.05 (user history bias, weak prior)
    """

    # Lexical marker dictionaries
    marker_sets: Dict[str, set] = field(default_factory=lambda: {
        "sheng_nairobi": SHENG_MARKERS,
        "swahili_coast": COASTAL_SWAHILI_MARKERS,
        "swahili_inland": INLAND_SWAHILI_MARKERS,
        "kikuyu_swahili": KIKUYU_SWAHILI_MARKERS,
        "dholuo_swahili": DHOLOU_SWAHILI_MARKERS,
        "yoruba_core": YORUBA_MARKERS,
        "hausa_core": HAUSA_MARKERS,
        "amharic_core": AMHARIC_MARKERS,
        "zulu_core": ZULU_MARKERS,
        "xhosa_core": XHOSA_MARKERS,
        "igbo_core": IGBO_MARKERS,
        "maasai_swahili": MAASAI_MARKERS,
        "somali_swahili": SOMALI_MARKERS,
        "luhya_swahili": LUHYA_MARKERS,
        "kalenjin_swahili": KALENJIN_MARKERS,
    })

    # Ensemble weights
    weights: Dict[str, float] = field(default_factory=lambda: {
        "lexical": 0.35,
        "script": 0.25,
        "ngram": 0.25,
        "morphological": 0.10,
        "context": 0.05,
    })

    # User dialect history for context-aware detection
    user_dialect_history: List[str] = field(default_factory=list)

    def detect(self, text: str, audio_features: Optional[Dict] = None) -> DialectResult:
        """
        Detect the dialect of the given text.

        Args:
            text: Input text (from ASR or typed input)
            audio_features: Optional acoustic features from speech

        Returns:
            DialectResult with primary dialect, confidence, and code-switch info
        """
        text_lower = text.lower().strip()

        # Signal 1: Lexical marker matching
        lexical_scores = self._score_lexical(text_lower)

        # Signal 2: Script detection
        script_scores = self._score_script(text)

        # Signal 3: N-gram scoring (simplified — would use trained model)
        ngram_scores = self._score_ngram(text_lower)

        # Signal 4: Morphological analysis
        morph_scores = self._score_morphological(text_lower)

        # Signal 5: Context from user history
        context_scores = self._score_context()

        # Ensemble combination
        final_scores: Dict[str, float] = {}
        all_dialects = set()
        for scores in [lexical_scores, script_scores, ngram_scores,
                        morph_scores, context_scores]:
            all_dialects.update(scores.keys())

        for dialect in all_dialects:
            score = (
                self.weights["lexical"] * lexical_scores.get(dialect, 0.0) +
                self.weights["script"] * script_scores.get(dialect, 0.0) +
                self.weights["ngram"] * ngram_scores.get(dialect, 0.0) +
                self.weights["morphological"] * morph_scores.get(dialect, 0.0) +
                self.weights["context"] * context_scores.get(dialect, 0.0)
            )
            final_scores[dialect] = score

        if not final_scores:
            return DialectResult(
                primary_dialect="swahili_core",
                primary_confidence=0.3,
                secondary_dialects=[],
                language_family=LanguageFamily.BANTU_EAST,
                raw_scores={},
            )

        # Sort by score descending
        sorted_dialects = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

        primary = sorted_dialects[0]
        secondary = [(d, s) for d, s in sorted_dialects[1:4] if s > 0.1]

        # Determine language family
        family = self._get_language_family(primary[0])

        # Check for code-switching
        is_code_switched, segments = self._detect_code_switching(text, final_scores)

        # Update user history
        self.user_dialect_history.append(primary[0])
        if len(self.user_dialect_history) > 20:
            self.user_dialect_history = self.user_dialect_history[-20:]

        return DialectResult(
            primary_dialect=primary[0],
            primary_confidence=min(primary[1], 1.0),
            secondary_dialects=secondary,
            language_family=family,
            code_switch_segments=segments,
            is_code_switched=is_code_switched,
            features_used=["lexical", "script", "ngram", "morphological", "context"],
            raw_scores=final_scores,
        )

    def _score_lexical(self, text: str) -> Dict[str, float]:
        """Score dialects based on lexical marker presence."""
        scores: Dict[str, float] = {}
        words = set(re.findall(r'\b\w+\b', text))

        for dialect, markers in self.marker_sets.items():
            # Count matching markers
            matches = words.intersection(markers)
            # Also check multi-word markers
            for marker in markers:
                if " " in marker and marker in text:
                    matches.add(marker)

            if matches:
                # Score = (matches / total markers in set) * boost
                # Boost short texts less aggressively
                coverage = len(matches) / max(len(markers) * 0.1, 1)
                text_length_factor = min(len(words) / 5, 1.0)
                scores[dialect] = min(coverage * text_length_factor, 1.0)

        # Special handling: if heavy English presence, boost Sheng (code-switching)
        english_words = {"the", "is", "and", "but", "can", "you", "help", "me",
                         "how", "what", "where", "when", "much", "very", "ok",
                         "yes", "no", "please", "sorry", "hello", "good", "nice"}
        english_count = len(words.intersection(english_words))
        if english_count > 2 and "swahili_core" in scores:
            # Code-switched input — likely Sheng or coastal
            scores["sheng_nairobi"] = scores.get("sheng_nairobi", 0.0) + 0.2
            scores["swahili_coast"] = scores.get("swahili_coast", 0.0) + 0.1

        return scores

    def _score_script(self, text: str) -> Dict[str, float]:
        """Score dialects based on script detection."""
        scores: Dict[str, float] = {}

        # Ge'ez script (Amharic) — U+1200-U+137F, U+1380-U+139F, U+2D80-U+2DDF
        ge_ez_chars = sum(1 for c in text
                          if ('\u1200' <= c <= '\u137f') or
                          ('\u1380' <= c <= '\u139f') or
                          ('\u2d80' <= c <= '\u2ddf'))
        if ge_ez_chars > 0:
            ratio = ge_ez_chars / max(len(text), 1)
            scores["amharic_core"] = min(ratio * 2, 1.0)

        # Arabic script (could be Somali, Swahili coast, Hausa in Ajami)
        arabic_chars = sum(1 for c in text
                           if '\u0600' <= c <= '\u06ff')
        if arabic_chars > 0:
            ratio = arabic_chars / max(len(text), 1)
            scores["somali_swahili"] = min(ratio * 1.5, 0.8)
            scores["swahili_coast"] = min(ratio * 1.0, 0.5)
            scores["hausa_core"] = min(ratio * 0.8, 0.4)

        # Click consonant detection for Zulu/Xhosa
        # In romanized text, clicks are represented by q, x, c in specific contexts
        click_patterns = re.findall(r'\b\w*[qx](?=[aeiou])\w*\b', text.lower())
        if click_patterns and len(click_patterns) >= 2:
            # Distinguish Zulu vs Xhosa by vocabulary
            xhosa_vocab = len(set(text.lower().split()).intersection(XHOSA_MARKERS))
            zulu_vocab = len(set(text.lower().split()).intersection(ZULU_MARKERS))
            if xhosa_vocab > zulu_vocab:
                scores["xhosa_core"] = 0.6
                scores["zulu_core"] = 0.3
            else:
                scores["zulu_core"] = 0.6
                scores["xhosa_core"] = 0.3

        return scores

    def _score_ngram(self, text: str) -> Dict[str, float]:
        """
        Score dialects using character n-gram models.

        In production, this would use a pre-trained n-gram language model.
        Here we use a simplified heuristic based on character patterns.
        """
        scores: Dict[str, float] = {}
        words = text.split()
        if not words:
            return scores

        # Bantu noun class prefix detection
        # Swahili: m-/wa-, ki-/vi-, n-/n-, u-, etc.
        bantu_prefixes = {
            "m": 0.1, "wa": 0.15, "ki": 0.15, "vi": 0.15,
            "n": 0.08, "u": 0.05, "ma": 0.1, "chi": 0.12,
            "vi": 0.12, "zi": 0.08, "mi": 0.1,
        }
        bantu_score = 0.0
        for word in words:
            for prefix, weight in bantu_prefixes.items():
                if word.startswith(prefix) and len(word) > len(prefix) + 2:
                    bantu_score += weight
                    break

        if bantu_score > 0.2:
            # High Bantu morphology — likely East African
            scores["swahili_core"] = min(bantu_score / len(words), 0.8)
            scores["swahili_coast"] = min(bantu_score / len(words) * 0.7, 0.6)

        # Swahili verb endings: -a (default), -i (stative), -e (subjunctive)
        swahili_verb_pattern = re.findall(r'\b\w+(?:na|li|ta|me|ki|ka|a|i|e|eni|ika)\b', text)
        if swahili_verb_pattern:
            swahili_score = len(swahili_verb_pattern) / max(len(words), 1)
            scores["swahili_core"] = max(scores.get("swahili_core", 0.0), swahili_score)

        # Tonal language indicators (Yoruba, Igbo)
        # Hard to detect in text without diacritics, but vowel patterns help
        yoruba_vowel_pattern = re.findall(r'[aeiou]{3,}', text.lower())
        if yoruba_vowel_pattern:
            scores["yoruba_core"] = scores.get("yoruba_core", 0.0) + 0.1

        return scores

    def _score_morphological(self, text: str) -> Dict[str, float]:
        """Score based on morphological analysis."""
        scores: Dict[str, float] = {}
        words = text.lower().split()

        # Swahili verb conjugation patterns
        swahili_tenses = ["na", "li", "ta", "me", "ki", "ka", "hu"]
        for word in words:
            for tense in swahili_tenses:
                if word.startswith(tense) and len(word) > 4:
                    scores["swahili_core"] = scores.get("swahili_core", 0.0) + 0.05

        # Negative markers
        neg_markers = {"si", "sio", "hapana", "la", "hata"}
        neg_matches = set(words).intersection(neg_markers)
        if neg_matches:
            scores["swahili_core"] = scores.get("swahili_core", 0.0) + 0.05 * len(neg_matches)

        return scores

    def _score_context(self) -> Dict[str, float]:
        """Score based on user's dialect history."""
        if not self.user_dialect_history:
            return {}

        # Count recent dialect choices
        from collections import Counter
        recent = self.user_dialect_history[-10:]
        counts = Counter(recent)
        total = len(recent)

        scores = {}
        for dialect, count in counts.items():
            # Prior probability from history (weak signal)
            scores[dialect] = (count / total) * 0.5  # Scale down

        return scores

    def _detect_code_switching(
        self, text: str, dialect_scores: Dict[str, float]
    ) -> Tuple[bool, List[CodeSwitchSegment]]:
        """
        Detect code-switching in text.

        Returns (is_code_switched, segments) where segments identify
        which parts of the text belong to which language.
        """
        segments: List[CodeSwitchSegment] = []
        words = text.split()

        if len(words) < 3:
            return False, segments

        # Simple sliding window approach
        # In production, use a sequence labeling model (CRF or transformer)
        current_lang = "swahili"
        current_start = 0
        current_text_parts: List[str] = []

        for i, word in enumerate(words):
            word_lower = word.lower()
            detected_lang = self._classify_word_language(word_lower)

            if detected_lang != current_lang:
                # Language boundary detected
                if current_text_parts:
                    segment_text = " ".join(current_text_parts)
                    # Calculate character offset
                    prefix = " ".join(words[:current_start])
                    start_offset = len(prefix) + (1 if prefix else 0)
                    end_offset = start_offset + len(segment_text)

                    segments.append(CodeSwitchSegment(
                        text=segment_text,
                        start_offset=start_offset,
                        end_offset=end_offset,
                        language=current_lang,
                        confidence=0.7,
                    ))

                current_lang = detected_lang
                current_start = i
                current_text_parts = [word]
            else:
                current_text_parts.append(word)

        # Final segment
        if current_text_parts:
            segment_text = " ".join(current_text_parts)
            prefix = " ".join(words[:current_start])
            start_offset = len(prefix) + (1 if prefix else 0)
            segments.append(CodeSwitchSegment(
                text=segment_text,
                start_offset=start_offset,
                end_offset=start_offset + len(segment_text),
                language=current_lang,
                confidence=0.7,
            ))

        is_code_switched = len(set(s.language for s in segments)) > 1
        return is_code_switched, segments

    def _classify_word_language(self, word: str) -> str:
        """Classify a single word's language."""
        # Check Sheng first (highest priority for code-switching)
        if word in SHENG_MARKERS:
            return "sheng"

        # Check English (common function words)
        english_words = {
            "the", "is", "and", "but", "or", "can", "you", "help", "me",
            "my", "your", "we", "they", "he", "she", "it", "this", "that",
            "what", "where", "when", "how", "much", "very", "ok", "yes",
            "no", "please", "sorry", "hello", "good", "nice", "want",
            "need", "have", "give", "take", "make", "go", "come",
            "about", "for", "with", "from", "not", "all", "some",
            "like", "just", "also", "because", "so", "then", "now",
            "money", "price", "cost", "buy", "sell", "pay", "shop",
            "stock", "market", "business", "profit", "loss", "save",
            "bank", "account", "loan", "debt", "interest",
        }
        if word in english_words:
            return "english"

        # Check other dialect markers
        for dialect, markers in self.marker_sets.items():
            if word in markers:
                lang = dialect.split("_")[0]
                return lang

        # Default: assume Swahili for Bantu-looking words
        bantu_pattern = re.match(r'^(m|wa|ki|vi|n|u|ma|chi|zi|mi)\w{3,}', word)
        if bantu_pattern:
            return "swahili"

        return "unknown"

    def _get_language_family(self, dialect: str) -> LanguageFamily:
        """Map a dialect to its language family."""
        family_map = {
            "swahili_core": LanguageFamily.BANTU_EAST,
            "swahili_coast": LanguageFamily.BANTU_EAST,
            "swahili_inland": LanguageFamily.BANTU_EAST,
            "sheng_nairobi": LanguageFamily.BANTU_SHENG,
            "sheng_mombasa": LanguageFamily.BANTU_SHENG,
            "kikuyu_swahili": LanguageFamily.BANTU_EAST,
            "dholuo_swahili": LanguageFamily.NILOTIC,
            "luhya_swahili": LanguageFamily.BANTU_EAST,
            "kalenjin_swahili": LanguageFamily.NILOTIC,
            "maasai_swahili": LanguageFamily.NILOTIC,
            "somali_swahili": LanguageFamily.CUSHITIC,
            "yoruba_core": LanguageFamily.NIGER_CONGO_YORUBOID,
            "igbo_core": LanguageFamily.NIGER_CONGO_IGBO,
            "hausa_core": LanguageFamily.AFROASIATIC_CHADIC,
            "amharic_core": LanguageFamily.AFROASIATIC_SEMITIC,
            "zulu_core": LanguageFamily.BANTU_EAST,
            "xhosa_core": LanguageFamily.BANTU_EAST,
        }
        return family_map.get(dialect, LanguageFamily.UNKNOWN)

    def update_sheng_vocabulary(self, new_words: List[str]) -> None:
        """
        Dynamically update Sheng vocabulary from user interactions.

        Sheng evolves rapidly — this allows the system to learn new slang
        from user interactions without requiring model retraining.
        """
        SHENG_MARKERS.update(new_words)
        self.marker_sets["sheng_nairobi"] = SHENG_MARKERS

    def get_dialect_stats(self) -> Dict[str, int]:
        """Get distribution of detected dialects from user history."""
        from collections import Counter
        return dict(Counter(self.user_dialect_history))
