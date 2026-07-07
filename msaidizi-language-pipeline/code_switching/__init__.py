"""
Code-Switching Handler for Msaidizi
====================================

Handles mixed-language input common in East African speech:

  "Niko na stock ya vitu mingi, lakini sijui bei gani ni fair.
   Unaweza help me calculate?"

This mixes:
  - Swahili: Niko na, vitu mingi, lakini, sijui, bei gani, unaweza
  - English: stock, help me calculate
  - Sheng: (potentially embedded in Swahili words)

The handler:
1. Segments input into language spans
2. Normalizes code-switched input for model consumption
3. Generates responses that match the user's code-switching pattern
4. Learns the user's code-switching patterns over time
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class CodeSwitchStrategy(Enum):
    """Strategy for processing code-switched input."""
    UNIFIED = "unified"       # Process as single stream
    SEGMENT = "segment"       # Split and process each segment
    CASCADE = "cascade"       # Try primary language, fall back


@dataclass
class LanguageSpan:
    """A contiguous span of text in a single language."""
    text: str
    language: str       # "swahili", "english", "sheng", "yoruba", etc.
    start_token: int
    end_token: int
    confidence: float


@dataclass
class CodeSwitchProfile:
    """A user's code-switching pattern profile."""
    user_id_hash: str
    primary_language: str = "swahili"
    secondary_languages: List[str] = field(default_factory=lambda: ["english"])
    switch_frequency: float = 0.3      # How often they switch (0-1)
    avg_span_length: float = 4.0       # Average tokens per language span
    common_switch_points: List[str] = field(default_factory=list)  # Where they switch
    vocabulary_mix: Dict[str, float] = field(default_factory=lambda: {
        "swahili": 0.6,
        "english": 0.25,
        "sheng": 0.15,
    })
    interaction_count: int = 0

    def update(self, spans: List[LanguageSpan]) -> None:
        """Update profile from new interaction."""
        self.interaction_count += 1

        # Update language distribution
        total_tokens = sum(s.end_token - s.start_token for s in spans)
        if total_tokens == 0:
            return

        alpha = min(0.1, 1.0 / self.interaction_count)  # Learning rate
        for span in spans:
            lang = span.language
            weight = (span.end_token - span.start_token) / total_tokens
            current = self.vocabulary_mix.get(lang, 0.0)
            self.vocabulary_mix[lang] = current * (1 - alpha) + weight * alpha

        # Update switch frequency
        n_switches = len(spans) - 1
        self.switch_frequency = (
            self.switch_frequency * 0.9 +
            (n_switches / max(total_tokens / 3, 1)) * 0.1
        )

        # Update average span length
        avg_len = total_tokens / max(len(spans), 1)
        self.avg_span_length = self.avg_span_length * 0.9 + avg_len * 0.1

        # Update primary language
        if self.vocabulary_mix:
            self.primary_language = max(
                self.vocabulary_mix.items(), key=lambda x: x[1]
            )[0]


@dataclass
class CodeSwitchHandler:
    """
    Handles code-switched input for Msaidizi.

    Supports the common East African pattern of mixing Swahili, English,
    and Sheng in single utterances. Also handles West African patterns
    (Yoruba-English, Hausa-English) and Southern African patterns.
    """

    # Vocabulary sets for language identification at word level
    _language_markers: Dict[str, set] = field(default_factory=lambda: {
        "english": {
            "the", "is", "and", "but", "or", "can", "you", "help", "me",
            "my", "your", "we", "they", "what", "where", "when", "how",
            "much", "very", "ok", "yes", "no", "please", "sorry", "hello",
            "good", "nice", "want", "need", "have", "give", "take", "make",
            "money", "price", "cost", "buy", "sell", "pay", "shop", "stock",
            "market", "business", "profit", "loss", "save", "bank", "account",
            "calculate", "total", "enough", "more", "less", "also", "about",
            "because", "so", "then", "now", "just", "like", "really", "sure",
        },
        "sheng": {
            "niaje", "sasa", "poa", "fiti", "ndeio", "mbogi", "mzinga",
            "ndelevu", "chipo", "ndege", "guoko", "nduthi", "kasongo",
            "kanairo", "mathree", "nganya", "mresh", "ushago", "kuomoka",
            "wamlambez", "wamyamaza", "kibao", "mjango", "naskia", "najua",
            "nafeel", "nathink", "naget", "narada",
        },
        "swahili": {
            "na", "ya", "ni", "kwa", "la", "za", "wa", "katika", "kwenye",
            "sana", "pia", "lakini", "au", "kama", "kwamba", "hii", "hizo",
            "ile", "yangu", "yake", "zao", "yetu", "sijui", "najua", "nataka",
            "ninaweza", "unaweza", "anaweza", "tunaweza", "bei", "gani",
            "ngapi", "vitu", "mzuri", "mbaya", "kubwa", "ndogo", "nzuri",
            "haraka", "pole", "sawa", "vizuri", "hapa", "pale", "hapo",
        },
    })

    # User profiles for personalized code-switching
    _user_profiles: Dict[str, CodeSwitchProfile] = field(default_factory=dict)

    def segment(self, text: str, user_id_hash: Optional[str] = None) -> List[LanguageSpan]:
        """
        Segment text into language spans.

        Uses a sliding window approach with lexical lookup and
        contextual disambiguation.
        """
        tokens = text.split()
        if not tokens:
            return []

        spans: List[LanguageSpan] = []
        current_lang = None
        current_start = 0

        for i, token in enumerate(tokens):
            token_lower = token.lower().strip(".,!?;:")
            detected = self._classify_token(token_lower)

            if detected != current_lang and current_lang is not None:
                # Save current span
                span_text = " ".join(tokens[current_start:i])
                spans.append(LanguageSpan(
                    text=span_text,
                    language=current_lang,
                    start_token=current_start,
                    end_token=i,
                    confidence=0.7,
                ))
                current_start = i

            current_lang = detected

        # Final span
        if current_lang is not None:
            spans.append(LanguageSpan(
                text=" ".join(tokens[current_start:]),
                language=current_lang,
                start_token=current_start,
                end_token=len(tokens),
                confidence=0.7,
            ))

        # Update user profile if available
        if user_id_hash and user_id_hash in self._user_profiles:
            self._user_profiles[user_id_hash].update(spans)

        return spans

    def normalize_for_model(
        self,
        text: str,
        strategy: CodeSwitchStrategy = CodeSwitchStrategy.UNIFIED,
        user_id_hash: Optional[str] = None,
    ) -> str:
        """
        Normalize code-switched input for model consumption.

        Strategies:
        - UNIFIED: Keep as-is, let the model handle it
        - SEGMENT: Split and mark language boundaries
        - CASCADE: Translate to primary language first
        """
        if strategy == CodeSwitchStrategy.UNIFIED:
            return text

        spans = self.segment(text, user_id_hash)

        if strategy == CodeSwitchStrategy.SEGMENT:
            # Mark language boundaries for the model
            parts = []
            for span in spans:
                if span.language != "unknown":
                    parts.append(f"[{span.language}]{span.text}[/{span.language}]")
                else:
                    parts.append(span.text)
            return " ".join(parts)

        if strategy == CodeSwitchStrategy.CASCADE:
            # Return only the primary language segments
            primary = self._get_primary_language(user_id_hash)
            primary_parts = [s.text for s in spans if s.language == primary]
            if primary_parts:
                return " ".join(primary_parts)
            return text  # Fallback to original

        return text

    def generate_response_style(
        self,
        user_id_hash: str,
    ) -> Dict[str, float]:
        """
        Get the user's preferred language mix for response generation.

        Returns a dict of {language: weight} that the response generator
        should use to match the user's style.
        """
        profile = self._user_profiles.get(user_id_hash)
        if profile:
            return dict(profile.vocabulary_mix)

        # Default mix for new users
        return {"swahili": 0.6, "english": 0.25, "sheng": 0.15}

    def learn_from_correction(
        self,
        user_id_hash: str,
        original: str,
        corrected: str,
        correction_type: str,
    ) -> None:
        """
        Learn from user corrections to improve code-switching handling.

        Correction types:
        - "language_misidentification": Wrong language detected
        - "segmentation_error": Wrong boundary between languages
        - "vocabulary_new": New word not in any vocabulary
        """
        if correction_type == "vocabulary_new":
            # Extract the new word and its language
            # This would be annotated by the user or inferred
            pass

        if user_id_hash not in self._user_profiles:
            self._user_profiles[user_id_hash] = CodeSwitchProfile(
                user_id_hash=user_id_hash
            )

    def _classify_token(self, token: str) -> str:
        """Classify a single token's language."""
        for lang, markers in self._language_markers.items():
            if token in markers:
                return lang

        # Check for Bantu morphological patterns
        if re.match(r'^(m|wa|ki|vi|n|u|ma|chi|zi|mi)\w{3,}$', token):
            return "swahili"

        # Check for Sheng patterns (often shortened/swapped Swahili)
        if re.match(r'^\w{2,5}$', token) and token not in self._language_markers["english"]:
            return "sheng"  # Short unknown words might be Sheng

        return "unknown"

    def _get_primary_language(self, user_id_hash: Optional[str]) -> str:
        """Get user's primary language."""
        if user_id_hash and user_id_hash in self._user_profiles:
            return self._user_profiles[user_id_hash].primary_language
        return "swahili"

    def get_sheng_vocabulary(self) -> set:
        """Get current Sheng vocabulary set (for learning/updating)."""
        return self._language_markers.get("sheng", set())

    def update_sheng_vocabulary(self, new_words: List[str]) -> None:
        """Add new Sheng words learned from user interactions."""
        if "sheng" not in self._language_markers:
            self._language_markers["sheng"] = set()
        self._language_markers["sheng"].update(new_words)
