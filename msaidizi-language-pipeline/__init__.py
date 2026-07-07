"""
Angavu Intelligence — Msaidizi African Language Training Pipeline
================================================================

The world's first live, federated, on-device African language training system.

This pipeline handles:
- Dialect detection across 14 African languages/dialects
- Ethical, consent-based voice data collection
- On-device LoRA fine-tuning via MobileFineTuner
- Federated aggregation with differential privacy
- Code-switching detection and handling (Swahili-English-Sheng)
- Per-dialect language quality scoring

Architecture:
  Voice → ASR (Whisper) → Dialect Detection → Code-Switch Analysis →
  Intent Routing → Response Generation → TTS → User

Training loop:
  User Interaction → Consent Check → Local Training Example →
  LoRA Fine-tuning (on-device, charging) → Gradient Delta →
  Differential Privacy → Federated Aggregation → Global Update

© 2026 Angavu Intelligence. All rights reserved.
"""

__version__ = "0.1.0"

SUPPORTED_DIALECTS = [
    # East African
    "swahili_core",       # Standard Kiswahili (lingua franca)
    "swahili_coast",      # Coastal dialect (Mombasa, Lamu)
    "swahili_inland",     # Inland/upcountry dialect
    "sheng_nairobi",      # Nairobi youth slang continuum
    "sheng_mombasa",      # Mombasa variant of Sheng
    "kikuyu_swahili",     # Kikuyu-influenced Swahili
    "dholuo_swahili",     # Luo-influenced Swahili
    "luhya_swahili",      # Luhya-influenced Swahili
    "kalenjin_swahili",   # Kalenjin-influenced Swahili
    "maasai_swahili",     # Maasai-influenced Swahili
    "somali_swahili",     # Somali-influenced Swahili
    # West African
    "yoruba_core",        # Standard Yoruba
    "igbo_core",          # Standard Igbo
    "hausa_core",         # Standard Hausa
    # East African (non-Bantu)
    "amharic_core",       # Standard Amharic
    # Southern African
    "zulu_core",          # Standard Zulu
    "xhosa_core",         # Standard Xhosa
]

# Language families for cross-lingual transfer
LANGUAGE_FAMILIES = {
    "bantu_east": ["swahili_core", "swahili_coast", "swahili_inland",
                    "kikuyu_swahili", "dholuo_swahili", "luhya_swahili",
                    "zulu_core", "xhosa_core"],
    "bantu_sheng": ["sheng_nairobi", "sheng_mombasa"],
    "nilotic": ["dholuo_swahili", "kalenjin_swahili", "maasai_swahili"],
    "cushitic": ["somali_swahili"],
    "afroasiatic_semitic": ["amharic_core"],
    "afroasiatic_chadic": ["hausa_core"],
    "niger_congo_yoruboid": ["yoruba_core"],
    "niger_congo_igbo": ["igbo_core"],
}

# Default language
DEFAULT_DIALECT = "swahili_core"
