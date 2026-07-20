"""
Tests for Seed Vocabulary Loading and Lookup.

Tests that the vocabulary marker sets in dialect_detection and
code_switching modules are:
- Properly loaded and non-empty
- Contain expected entries
- Correctly used for dialect/language classification
- Properly updatable
"""

import pytest
from dialect_detection import (
    DialectClassifier,
    SHENG_MARKERS,
    COASTAL_SWAHILI_MARKERS,
    INLAND_SWAHILI_MARKERS,
    KIKUYU_SWAHILI_MARKERS,
    DHOLOU_SWAHILI_MARKERS,
    YORUBA_MARKERS,
    HAUSA_MARKERS,
    AMHARIC_MARKERS,
    ZULU_MARKERS,
    XHOSA_MARKERS,
    IGBO_MARKERS,
    MAASAI_MARKERS,
    SOMALI_MARKERS,
    LUHYA_MARKERS,
    KALENJIN_MARKERS,
)
from code_switching import CodeSwitchHandler


class TestVocabularyLoading:
    """Test that all vocabulary sets are properly loaded."""

    @pytest.mark.parametrize("marker_set,name", [
        (SHENG_MARKERS, "SHENG_MARKERS"),
        (COASTAL_SWAHILI_MARKERS, "COASTAL_SWAHILI_MARKERS"),
        (INLAND_SWAHILI_MARKERS, "INLAND_SWAHILI_MARKERS"),
        (KIKUYU_SWAHILI_MARKERS, "KIKUYU_SWAHILI_MARKERS"),
        (DHOLOU_SWAHILI_MARKERS, "DHOLOU_SWAHILI_MARKERS"),
        (YORUBA_MARKERS, "YORUBA_MARKERS"),
        (HAUSA_MARKERS, "HAUSA_MARKERS"),
        (AMHARIC_MARKERS, "AMHARIC_MARKERS"),
        (ZULU_MARKERS, "ZULU_MARKERS"),
        (XHOSA_MARKERS, "XHOSA_MARKERS"),
        (IGBO_MARKERS, "IGBO_MARKERS"),
        (MAASAI_MARKERS, "MAASAI_MARKERS"),
        (SOMALI_MARKERS, "SOMALI_MARKERS"),
        (LUHYA_MARKERS, "LUHYA_MARKERS"),
        (KALENJIN_MARKERS, "KALENJIN_MARKERS"),
    ])
    def test_marker_set_non_empty(self, marker_set, name):
        """All marker sets should have at least one entry."""
        assert len(marker_set) > 0, f"{name} is empty"

    @pytest.mark.parametrize("marker_set,name", [
        (SHENG_MARKERS, "SHENG_MARKERS"),
        (COASTAL_SWAHILI_MARKERS, "COASTAL_SWAHILI_MARKERS"),
        (YORUBA_MARKERS, "YORUBA_MARKERS"),
        (HAUSA_MARKERS, "HAUSA_MARKERS"),
    ])
    def test_marker_set_is_set_type(self, marker_set, name):
        """All marker sets should be sets (for O(1) lookup)."""
        assert isinstance(marker_set, set), f"{name} should be a set"

    @pytest.mark.parametrize("marker_set,name,min_size", [
        (SHENG_MARKERS, "SHENG_MARKERS", 10),
        (COASTAL_SWAHILI_MARKERS, "COASTAL_SWAHILI_MARKERS", 5),
        (YORUBA_MARKERS, "YORUBA_MARKERS", 5),
        (HAUSA_MARKERS, "HAUSA_MARKERS", 5),
        (AMHARIC_MARKERS, "AMHARIC_MARKERS", 3),
        (ZULU_MARKERS, "ZULU_MARKERS", 5),
    ])
    def test_marker_set_minimum_size(self, marker_set, name, min_size):
        """Marker sets should have a minimum vocabulary size."""
        assert len(marker_set) >= min_size, \
            f"{name} has only {len(marker_set)} entries (need >= {min_size})"


class TestShengVocabulary:
    """Test Sheng vocabulary specifically."""

    def test_core_sheng_words_present(self):
        """Core Sheng words should be in the marker set."""
        core_words = {"niaje", "sasa", "poa", "fiti", "mbogi", "wamlambez"}
        for word in core_words:
            assert word in SHENG_MARKERS, f"Core Sheng word '{word}' missing"

    def test_sheng_is_lowercase(self):
        """Sheng markers should be lowercase for consistent matching."""
        for word in SHENG_MARKERS:
            assert word == word.lower(), f"Sheng marker '{word}' should be lowercase"

    def test_sheng_no_empty_strings(self):
        """No empty strings in Sheng markers."""
        for word in SHENG_MARKERS:
            assert word.strip() != "", "Empty string in SHENG_MARKERS"

    def test_sheng_no_spaces_in_single_words(self):
        """Single-word markers should not have leading/trailing spaces."""
        for word in SHENG_MARKERS:
            if " " not in word:
                assert word == word.strip()


class TestSwahiliVocabulary:
    """Test Swahili vocabulary sets."""

    def test_coastal_swahili_markers(self):
        """Coastal markers should contain Arabic-influenced words."""
        arabic_influenced = {"inshallah", "mashallah", "wallahi", "habibi"}
        found = arabic_influenced.intersection(COASTAL_SWAHILI_MARKERS)
        assert len(found) > 0, "Coastal markers should contain Arabic-influenced words"

    def test_inland_swahili_markers(self):
        """Inland markers should contain upcountry vocabulary."""
        assert "sawa" in INLAND_SWAHILI_MARKERS or "vizuri" in INLAND_SWAHILI_MARKERS

    def test_no_overlap_sheng_coastal(self):
        """Sheng and Coastal markers should have minimal overlap."""
        overlap = SHENG_MARKERS.intersection(COASTAL_SWAHILI_MARKERS)
        # Some overlap is acceptable, but they should be mostly distinct
        total = len(SHENG_MARKERS) + len(COASTAL_SWAHILI_MARKERS)
        assert len(overlap) < total * 0.3, \
            f"Too much overlap between Sheng and Coastal: {overlap}"


class TestWestAfricanVocabulary:
    """Test West African vocabulary sets."""

    def test_yoruba_markers(self):
        """Yoruba markers should contain expected words."""
        assert "bawo" in YORUBA_MARKERS
        assert "o dara" in YORUBA_MARKERS or "e se" in YORUBA_MARKERS

    def test_hausa_markers(self):
        """Hausa markers should contain expected words."""
        assert "sannu" in HAUSA_MARKERS
        assert "na gode" in HAUSA_MARKERS

    def test_igbo_markers(self):
        """Igbo markers should contain expected words."""
        assert "ndewo" in IGBO_MARKERS or "kedu" in IGBO_MARKERS


class TestVocabularyLookup:
    """Test vocabulary lookup performance and correctness."""

    def test_lookup_is_case_insensitive(self, classifier):
        """Lookup should handle case variations."""
        # The classifier lowercases input before lookup
        result1 = classifier.detect("NIAJE MBogi")
        result2 = classifier.detect("niaje mbogi")
        # Both should produce similar results
        assert result1.primary_dialect == result2.primary_dialect

    def test_vocabulary_in_classifier_marker_sets(self, classifier):
        """Classifier should have all marker sets loaded."""
        expected_sets = [
            "sheng_nairobi", "swahili_coast", "swahili_inland",
            "kikuyu_swahili", "dholuo_swahili", "yoruba_core",
            "hausa_core", "amharic_core", "zulu_core", "xhosa_core",
            "igbo_core", "maasai_swahili", "somali_swahili",
            "luhya_swahili", "kalenjin_swahili",
        ]
        for name in expected_sets:
            assert name in classifier.marker_sets, \
                f"Missing marker set '{name}' in classifier"

    def test_each_marker_set_has_entries(self, classifier):
        """Each marker set in the classifier should have entries."""
        for name, markers in classifier.marker_sets.items():
            assert len(markers) > 0, f"Marker set '{name}' is empty"


class TestVocabularyUpdate:
    """Test dynamic vocabulary updates."""

    def test_update_sheng_vocabulary_adds_words(self):
        """Updating Sheng vocabulary should add new words."""
        initial_size = len(SHENG_MARKERS)
        new_words = ["testword1", "testword2", "testword3"]
        classifier = DialectClassifier()
        classifier.update_sheng_vocabulary(new_words)
        assert len(SHENG_MARKERS) >= initial_size + len(new_words)

    def test_code_switch_handler_vocabulary_update(self, code_switch_handler):
        """CodeSwitchHandler vocabulary should be updatable."""
        initial = code_switch_handler.get_sheng_vocabulary()
        code_switch_handler.update_sheng_vocabulary(["newsheng1", "newsheng2"])
        updated = code_switch_handler.get_sheng_vocabulary()
        assert "newsheng1" in updated
        assert "newsheng2" in updated


class TestCodeSwitchingVocabulary:
    """Test vocabulary in the code-switching module."""

    def test_handler_has_language_markers(self, code_switch_handler):
        """Handler should have language markers for classification."""
        markers = code_switch_handler._language_markers
        assert "english" in markers
        assert "sheng" in markers
        assert "swahili" in markers

    def test_english_markers_non_empty(self, code_switch_handler):
        """English markers should be non-empty."""
        markers = code_switch_handler._language_markers["english"]
        assert len(markers) > 0

    def test_sheng_markers_non_empty(self, code_switch_handler):
        """Sheng markers should be non-empty."""
        markers = code_switch_handler._language_markers["sheng"]
        assert len(markers) > 0

    def test_swahili_markers_non_empty(self, code_switch_handler):
        """Swahili markers should be non-empty."""
        markers = code_switch_handler._language_markers["swahili"]
        assert len(markers) > 0

    def test_common_english_words_present(self, code_switch_handler):
        """Common English words should be in the English marker set."""
        common = {"the", "is", "and", "can", "you", "help", "me", "what", "how"}
        english_markers = code_switch_handler._language_markers["english"]
        for word in common:
            assert word in english_markers, f"Common English word '{word}' missing"

    def test_common_swahili_words_present(self, code_switch_handler):
        """Common Swahili words should be in the Swahili marker set."""
        common = {"na", "ya", "ni", "kwa", "lakini", "sana"}
        swahili_markers = code_switch_handler._language_markers["swahili"]
        for word in common:
            assert word in swahili_markers, f"Common Swahili word '{word}' missing"


class TestVocabularyEdgeCases:
    """Test vocabulary edge cases."""

    def test_no_none_values_in_markers(self):
        """No marker set should contain None values."""
        all_sets = [
            SHENG_MARKERS, COASTAL_SWAHILI_MARKERS, INLAND_SWAHILI_MARKERS,
            YORUBA_MARKERS, HAUSA_MARKERS, AMHARIC_MARKERS,
            ZULU_MARKERS, XHOSA_MARKERS, IGBO_MARKERS,
        ]
        for marker_set in all_sets:
            for word in marker_set:
                assert word is not None, f"None value found in marker set"

    def test_no_empty_strings_in_markers(self):
        """No marker set should contain empty strings."""
        all_sets = [
            SHENG_MARKERS, COASTAL_SWAHILI_MARKERS, INLAND_SWAHILI_MARKERS,
            YORUBA_MARKERS, HAUSA_MARKERS, AMHARIC_MARKERS,
        ]
        for marker_set in all_sets:
            for word in marker_set:
                assert isinstance(word, str) and len(word) > 0, \
                    f"Empty or non-string value in marker set: {repr(word)}"

    def test_marker_sets_are_hashable(self):
        """All marker values should be hashable (they're in sets)."""
        # This is implicitly tested by being sets, but let's be explicit
        for word in SHENG_MARKERS:
            hash(word)  # Should not raise
