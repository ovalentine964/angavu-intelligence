"""
Shared fixtures for Msaidizi Language Pipeline tests.

Provides reusable test data including:
- Swahili/Sheng/English sample phrases
- Pre-configured classifier instances
- Mock voice samples and consent records
- Worker belief fixtures for Bayesian testing
"""

import sys
import os
import time
import pytest

# Ensure the pipeline package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dialect_detection import DialectClassifier, DialectResult, LanguageFamily
from code_switching import CodeSwitchHandler, CodeSwitchProfile, LanguageSpan
from federated_learning import DifferentialPrivacy, FederatedAggregator, GradientDelta
from agents.memory.tiered import WorkerBelief, WorkerBehavioralModel
from voice_collection import ConsentManager, ConsentLevel, ConsentRecord


# ───────────────────────────────────────────────────────────────
# Swahili / Sheng / English sample phrases
# ───────────────────────────────────────────────────────────────

@pytest.fixture
def swahili_phrases():
    """Standard Swahili phrases for dialect detection."""
    return [
        "Habari za asubuhi, mzee wangu",
        "Nataka kunua vitu vya soko kesho",
        "Bei ya nyanya imepanda sana wiki hii",
        "Tafadhali nisaidie kuhesabu faida yangu",
        "Nimepata wateja wengi leo sokoni",
        "Karibu duka langu, vitu vyote ni vizuri",
        "Shukrani kwa msaada wako rafiki yangu",
        "Ninahitaji kuhifadhi akiba yangu benki",
    ]


@pytest.fixture
def sheng_phrases():
    """Nairobi Sheng phrases for dialect detection."""
    return [
        "Niaje mbogi, sasa?",
        "Poa sana mjango, wamlambez!",
        "Naskia bei ya chipo imepanda kanairo",
        "Najua tu venye niko na mbogi zangu",
        "Ndege ya mzinga iko fiti sana",
        "Kuomoka na hii maisha ndeio rahisi",
        "Mresh wa nduthi ameniletea mzigo",
        "Naeza help, lakini ni bei gani?",
    ]


@pytest.fixture
def english_phrases():
    """English phrases that might appear in code-switching."""
    return [
        "What is the price of tomatoes today?",
        "Can you help me calculate my profit?",
        "I need to save money for my business",
        "The market is very busy this morning",
        "How much does it cost to transport goods?",
        "Please give me the total amount",
    ]


@pytest.fixture
def code_switched_phrases():
    """Realistic code-switched Swahili-English-Sheng phrases."""
    return [
        "Niko na stock ya vitu mingi, lakini sijui bei gani ni fair",
        "Unaweza help me calculate total ya mauzo yangu?",
        "Sasa mjango, bei ya market imepanda, nafeel stressed",
        "Najua business yangu inahitaji more capital",
        "Wamlambez! Can you check bei ya nduthi kanairo?",
        "Niko na plan ya kuexpand biashara yangu next month",
    ]


@pytest.fixture
def yoruba_phrases():
    """Yoruba phrases for West African dialect testing."""
    return [
        "Bawo ni, se daadaa ni?",
        "E ku ojumo, mo n lo si oja",
        "Ki ni owo tomato loni?",
        "Mo fe ra epo ati ata",
        "O dara, e se pupo",
    ]


@pytest.fixture
def hausa_phrases():
    """Hausa phrases for West African dialect testing."""
    return [
        "Sannu, yaya kake?",
        "Ina so in saya kayan masarufi",
        "Lafiya lau, na gode",
        "Nawa ne farashin tumatir?",
        "In sha Allah, za mu yi aiki gobe",
    ]


@pytest.fixture
def amharic_phrases():
    """Amharic phrases (romanized) for testing."""
    return [
        "Selam, tena yistilign",
        "Ameseginalehu behuala",
        "Dehna neh?",
        "Eh, aw, shi",
    ]


@pytest.fixture
def empty_input():
    """Empty and whitespace-only inputs."""
    return ["", "   ", "\n", "\t", "  \n  "]


@pytest.fixture
def mixed_script_input():
    """Input with mixed scripts (Latin + Ge'ez + Arabic)."""
    return [
        "Hello ሰላም مرحبا",
        "Niaje እንደምን ነህ?",
        "Habari سلام عليكم",
    ]


# ───────────────────────────────────────────────────────────────
# Pre-configured instances
# ───────────────────────────────────────────────────────────────

@pytest.fixture
def classifier():
    """A fresh DialectClassifier instance."""
    return DialectClassifier()


@pytest.fixture
def code_switch_handler():
    """A fresh CodeSwitchHandler instance."""
    return CodeSwitchHandler()


@pytest.fixture
def dp_strong():
    """DifferentialPrivacy with strong privacy (ε=0.1)."""
    return DifferentialPrivacy(epsilon=0.1, delta=1e-5, clip_norm=1.0)


@pytest.fixture
def dp_moderate():
    """DifferentialPrivacy with moderate privacy (ε=1.0)."""
    return DifferentialPrivacy(epsilon=1.0, delta=1e-5, clip_norm=1.0)


@pytest.fixture
def consent_manager():
    """A ConsentManager with some test consent records."""
    cm = ConsentManager()
    # Pre-register some users
    cm.request_consent("user_hash_001", ConsentLevel.FEDERATED, locale="sw")
    cm.request_consent("user_hash_002", ConsentLevel.CLOUD, locale="en")
    cm.request_consent("user_hash_003", ConsentLevel.OFFLINE, locale="sw")
    return cm


@pytest.fixture
def sample_gradient_delta():
    """A sample GradientDelta for federated learning tests."""
    return GradientDelta(
        device_id_hash="device_abc123",
        user_id_hash="user_xyz789",
        dialect="sheng_nairobi",
        adapter_type="user",
        weight_delta={
            "lora_A": 0.05,
            "lora_B": -0.03,
            "nested": {"w1": 0.01, "w2": -0.02},
            "vector": [0.1, -0.05, 0.02],
        },
        delta_l2_norm=0.15,
        num_examples=50,
        training_loss=1.2,
        timestamp=time.time(),
        round_id=1,
    )


@pytest.fixture
def worker_belief():
    """A WorkerBelief with default priors for testing Bayesian update."""
    return WorkerBelief(
        name="daily_revenue",
        mean=700.0,
        variance=500.0,
        confidence=0.3,
        update_count=0,
    )


@pytest.fixture
def sample_user_spans():
    """Sample language spans for code-switch profile testing."""
    return [
        LanguageSpan(text="Niko na", language="swahili", start_token=0, end_token=2, confidence=0.8),
        LanguageSpan(text="stock ya vitu mingi", language="english", start_token=2, end_token=6, confidence=0.7),
        LanguageSpan(text="lakini sijui bei gani", language="swahili", start_token=6, end_token=10, confidence=0.8),
        LanguageSpan(text="ni fair", language="english", start_token=10, end_token=12, confidence=0.7),
    ]
