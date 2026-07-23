"""
Voice Data Collection Module with Ethical Consent Framework
===========================================================

Implements the CARE Principles for Indigenous Data Governance:
- Collective Benefit: Data serves the community
- Authority to Control: Users control their data on-device
- Responsibility: Angavu compensates through free tools
- Ethics: Wellbeing is central

Three-tier consent model:
  Level 0: Offline only — no data leaves device
  Level 1: Federated — only differentially-private model updates shared
  Level 2: Cloud — interaction data used for cloud-side improvement

Voice data is NEVER extracted. Only model deltas (gradients) leave the device,
and only with differential privacy applied.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime


class ConsentLevel(IntEnum):
    """User consent levels for data sharing."""
    OFFLINE = 0       # No data leaves device
    FEDERATED = 1     # Only model deltas (differentially private) shared
    CLOUD = 2         # Interaction data used for cloud improvement


@dataclass
class ConsentRecord:
    """Immutable record of user consent."""
    user_id_hash: str           # SHA-256 hash of user ID (never store raw)
    consent_level: ConsentLevel
    timestamp: float
    consent_version: str        # Version of consent terms
    granular_permissions: Dict[str, bool] = field(default_factory=lambda: {
        "voice_transcripts": False,
        "model_updates": False,
        "dialect_annotations": False,
        "usage_analytics": False,
    })
    locale: str = "sw"          # Language of consent form shown
    revocation_timestamp: Optional[float] = None

    @property
    def is_active(self) -> bool:
        return self.revocation_timestamp is None

    def revoke(self) -> None:
        self.revocation_timestamp = time.time()


@dataclass
class VoiceSample:
    """A collected voice sample with metadata."""
    sample_id: str
    user_id_hash: str
    timestamp: float
    duration_seconds: float
    dialect_detected: str
    dialect_confidence: float
    transcript: str
    language_segments: List[Dict[str, Any]]  # code-switch segments
    audio_path: Optional[str] = None         # local path, encrypted
    consent_level: ConsentLevel = ConsentLevel.OFFLINE
    is_used_for_training: bool = False
    quality_score: float = 0.0               # 0-1 quality metric

    def to_training_example(self) -> Optional[Dict[str, Any]]:
        """Convert to a training example if consent allows."""
        if self.consent_level < ConsentLevel.FEDERATED:
            return None
        if not self.transcript or len(self.transcript.strip()) < 5:
            return None
        return {
            "text": self.transcript,
            "dialect": self.dialect_detected,
            "dialect_confidence": self.dialect_confidence,
            "language_segments": self.language_segments,
            "quality_score": self.quality_score,
            "timestamp": self.timestamp,
        }


@dataclass
class ConsentManager:
    """
    Manages user consent with plain-language explanations.

    Key design decisions:
    - Consent is stored on-device only (never uploaded)
    - Consent can be changed at any time
    - Each data type has independent consent
    - Consent form is available in user's preferred language
    - Voice-based consent explanation available (audio consent)
    """

    consent_records: Dict[str, ConsentRecord] = field(default_factory=dict)
    current_consent_version: str = "1.0.0"

    # Localized consent explanations
    consent_explanations: Dict[str, Dict[str, str]] = field(default_factory=lambda: {
        "sw": {  # Swahili
            "level_0": (
                "Msaidizi itafanya kazi bila kutuma data yoyote nje ya simu yako. "
                "Hakuna mtu mwingine ataona data yako."
            ),
            "level_1": (
                "Msaidizi itajifunza kutoka mazungumzo yako na kuboresha huduma. "
                "Data yako ya sauti haitatoka kwenye simu yako. "
                "Tu mabadiliko madogo ya modeli (sio data yako) yatashirikiwa "
                "kuboresha AI kwa watumiaji wote."
            ),
            "level_2": (
                "Msaidizi itatumia mazungumzo yako kuboresha AI kwa watumiaji wote. "
                "Data yako itatibiwa na kutumika kwa ujifunzaji. "
                "Jina lako halitatumika — data yako itakuwa ya siri."
            ),
        },
        "en": {  # English
            "level_0": (
                "Msaidizi will work without sending any data outside your phone. "
                "Nobody else will see your data."
            ),
            "level_1": (
                "Msaidizi will learn from your conversations to improve the service. "
                "Your voice data will never leave your phone. "
                "Only tiny model updates (not your data) will be shared "
                "to improve AI for all users."
            ),
            "level_2": (
                "Msaidizi will use your conversations to improve AI for all users. "
                "Your data will be anonymized and used for training. "
                "Your name will never be used — your data will be kept private."
            ),
        },
        "yo": {  # Yoruba
            "level_0": (
                "Msaidizi yoo ṣiṣẹ lai fi data rẹ ranṣẹ kuro ninu foonu rẹ. "
                "Ko si ẹnikan ti yoo ri data rẹ."
            ),
        },
    })

    def request_consent(
        self,
        user_id_hash: str,
        level: ConsentLevel,
        locale: str = "sw",
        granular: Optional[Dict[str, bool]] = None,
    ) -> ConsentRecord:
        """
        Record a new consent decision.

        Args:
            user_id_hash: SHA-256 hash of user ID
            level: Requested consent level
            locale: Language for consent explanation
            granular: Optional granular permissions override

        Returns:
            ConsentRecord with the consent decision
        """
        record = ConsentRecord(
            user_id_hash=user_id_hash,
            consent_level=level,
            timestamp=time.time(),
            consent_version=self.current_consent_version,
            locale=locale,
        )

        # Set granular permissions based on consent level
        if granular:
            record.granular_permissions.update(granular)
        else:
            if level >= ConsentLevel.FEDERATED:
                record.granular_permissions["model_updates"] = True
            if level >= ConsentLevel.CLOUD:
                record.granular_permissions["voice_transcripts"] = True
                record.granular_permissions["dialect_annotations"] = True

        self.consent_records[user_id_hash] = record
        return record

    def revoke_consent(self, user_id_hash: str) -> bool:
        """Revoke all consent for a user. Data deletion triggered separately."""
        record = self.consent_records.get(user_id_hash)
        if record:
            record.revoke()
            return True
        return False

    def get_consent(self, user_id_hash: str) -> Optional[ConsentRecord]:
        """Get current active consent for a user."""
        record = self.consent_records.get(user_id_hash)
        if record and record.is_active:
            return record
        return None

    def get_explanation(self, level: ConsentLevel, locale: str = "sw") -> str:
        """Get plain-language consent explanation in user's language."""
        key = f"level_{level.value}"
        explanations = self.consent_explanations.get(locale, {})
        return explanations.get(key, self.consent_explanations["en"].get(key, ""))

    def can_share_model_updates(self, user_id_hash: str) -> bool:
        """Check if user has consented to share model updates."""
        consent = self.get_consent(user_id_hash)
        return consent is not None and consent.consent_level >= ConsentLevel.FEDERATED

    def can_use_for_training(self, user_id_hash: str) -> bool:
        """Check if interaction data can be used for training."""
        consent = self.get_consent(user_id_hash)
        return consent is not None and consent.consent_level >= ConsentLevel.FEDERATED

    def export_consent_log(self) -> List[Dict[str, Any]]:
        """Export consent log for audit purposes (no raw user IDs)."""
        return [
            {
                "user_hash": r.user_id_hash[:8] + "...",
                "level": r.consent_level.name,
                "timestamp": r.timestamp,
                "version": r.consent_version,
                "active": r.is_active,
            }
            for r in self.consent_records.values()
        ]


@dataclass
class VoiceCollector:
    """
    Collects voice data with ethical safeguards.

    Pipeline:
    1. User speaks → Audio captured (on-device)
    2. Voice Activity Detection → Trim silence
    3. Whisper ASR → Transcript (on-device)
    4. Dialect detection → Language metadata
    5. Consent check → If allowed, store for training
    6. Raw audio → Encrypted local storage (optional)
    7. Transcript + metadata → Training example (if consented)

    Privacy guarantees:
    - Raw audio never leaves device (unless Level 2 consent)
    - Transcripts stored locally only
    - User can delete all data at any time
    - Storage is encrypted at rest
    """

    consent_manager: ConsentManager
    storage_path: str = "data/voice_samples"
    max_storage_mb: int = 500
    delete_raw_audio: bool = True
    encrypt_storage: bool = True
    _samples: List[VoiceSample] = field(default_factory=list)
    _on_sample_collected: Optional[Callable] = None

    def collect_sample(
        self,
        user_id_hash: str,
        audio_data: bytes,
        transcript: str,
        dialect: str,
        dialect_confidence: float,
        language_segments: List[Dict[str, Any]],
    ) -> Optional[VoiceSample]:
        """
        Collect a voice sample with consent verification.

        Returns None if consent is not given or storage limits exceeded.
        """
        # Check consent
        consent = self.consent_manager.get_consent(user_id_hash)
        if not consent:
            return None

        # Check storage limits
        if self._get_storage_usage_mb() >= self.max_storage_mb:
            self._cleanup_old_samples()

        sample = VoiceSample(
            sample_id=hashlib.sha256(
                f"{user_id_hash}:{time.time()}".encode()
            ).hexdigest()[:16],
            user_id_hash=user_id_hash,
            timestamp=time.time(),
            duration_seconds=len(audio_data) / (16000 * 2),  # 16kHz 16-bit
            dialect_detected=dialect,
            dialect_confidence=dialect_confidence,
            transcript=transcript,
            language_segments=language_segments,
            consent_level=consent.consent_level,
        )

        # Handle raw audio based on consent
        if consent.consent_level >= ConsentLevel.CLOUD and not self.delete_raw_audio:
            audio_path = self._store_audio(sample.sample_id, audio_data)
            sample.audio_path = audio_path

        # Quality scoring
        sample.quality_score = self._assess_quality(sample)

        self._samples.append(sample)

        # Callback for training pipeline
        if self._on_sample_collected and sample.quality_score > 0.3:
            self._on_sample_collected(sample)

        return sample

    def get_training_samples(
        self, user_id_hash: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get training-ready samples for a user."""
        samples = [
            s.to_training_example()
            for s in self._samples
            if s.user_id_hash == user_id_hash
            and s.quality_score > 0.3
            and s.consent_level >= ConsentLevel.FEDERATED
        ]
        return [s for s in samples if s is not None][:limit]

    def delete_user_data(self, user_id_hash: str) -> int:
        """
        Delete all data for a user. Right to erasure.

        Returns number of samples deleted.
        """
        to_delete = [s for s in self._samples if s.user_id_hash == user_id_hash]

        for sample in to_delete:
            if sample.audio_path and os.path.exists(sample.audio_path):
                os.remove(sample.audio_path)
            self._samples.remove(sample)

        return len(to_delete)

    def _assess_quality(self, sample: VoiceSample) -> float:
        """
        Assess the quality of a voice sample for training.

        Factors:
        - Transcript length (too short = low quality)
        - Dialect confidence
        - Audio duration (too short/long = low quality)
        - Code-switching consistency
        """
        score = 0.0

        # Transcript length
        word_count = len(sample.transcript.split())
        if word_count >= 5:
            score += 0.3
        elif word_count >= 3:
            score += 0.15

        # Dialect confidence
        score += sample.dialect_confidence * 0.3

        # Duration (5-60 seconds is ideal)
        if 5 <= sample.duration_seconds <= 60:
            score += 0.2
        elif 2 <= sample.duration_seconds <= 120:
            score += 0.1

        # Code-switching penalty (mixed language is harder to learn from)
        if len(sample.language_segments) > 1:
            # Not a penalty per se, but lower confidence
            score *= 0.9

        return min(score, 1.0)

    def _store_audio(self, sample_id: str, audio_data: bytes) -> str:
        """Store audio locally with optional encryption."""
        path = Path(self.storage_path)
        path.mkdir(parents=True, exist_ok=True)

        filepath = path / f"{sample_id}.wav"

        if self.encrypt_storage:
            # In production: use Android Keystore / AES-256-GCM
            # Simplified here — XOR is NOT used in production
            encrypted = self._encrypt_audio(audio_data)
            filepath.write_bytes(encrypted)
        else:
            filepath.write_bytes(audio_data)

        return str(filepath)

    def _encrypt_audio(self, data: bytes) -> bytes:
        """Encrypt audio data using AES-256-GCM."""
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        import os
        # Derive a key from device-specific material (in production: Android Keystore)
        key = hashlib.sha256(b"msaidizi-device-key-placeholder").digest()  # 256-bit
        nonce = os.urandom(12)  # 96-bit nonce for GCM
        aesgcm = AESGCM(key)
        # AES-256-GCM provides confidentiality + authenticity
        ciphertext = aesgcm.encrypt(nonce, data, None)
        # Prepend nonce to ciphertext for decryption
        return nonce + ciphertext

    def _get_storage_usage_mb(self) -> float:
        """Get current storage usage in MB."""
        total = sum(
            os.path.getsize(s.audio_path)
            for s in self._samples
            if s.audio_path and os.path.exists(s.audio_path)
        )
        return total / (1024 * 1024)

    def _cleanup_old_samples(self) -> None:
        """Remove oldest samples when storage limit is reached."""
        # Sort by timestamp, oldest first
        self._samples.sort(key=lambda s: s.timestamp)

        while self._get_storage_usage_mb() > self.max_storage_mb * 0.8:
            if not self._samples:
                break
            oldest = self._samples.pop(0)
            if oldest.audio_path and os.path.exists(oldest.audio_path):
                os.remove(oldest.audio_path)
