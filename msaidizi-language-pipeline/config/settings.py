"""
Pipeline configuration — central settings for the language training system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path


@dataclass
class DialectDetectionConfig:
    """Configuration for the dialect detection module."""
    # Minimum confidence threshold to accept a dialect classification
    min_confidence: float = 0.65
    # Number of recent utterances to consider for context-aware detection
    context_window: int = 5
    # Model path for the dialect classifier (fine-tuned on African speech)
    classifier_model_path: str = "models/dialect_classifier_v1.pt"
    # Enable code-switching detection
    code_switching_enabled: bool = True
    # Minimum segment length (tokens) to classify as a distinct language
    min_segment_tokens: int = 3


@dataclass
class VoiceCollectionConfig:
    """Configuration for ethical voice data collection."""
    # Maximum recording duration in seconds
    max_recording_duration: int = 120
    # Sample rate for audio capture
    sample_rate: int = 16000
    # Audio format
    audio_format: str = "wav"
    # Minimum consent level required (0=none, 1=federated, 2=cloud)
    min_consent_level: int = 1
    # Enable voice activity detection to trim silence
    vad_enabled: bool = True
    # Local storage path for voice data (on-device)
    local_storage_path: str = "data/voice_samples"
    # Maximum local storage in MB
    max_local_storage_mb: int = 500
    # Auto-delete raw audio after transcription
    delete_raw_audio_after_transcribe: bool = True
    # Encryption key for local audio storage
    encrypt_local_audio: bool = True


@dataclass
class FineTuningConfig:
    """Configuration for on-device LoRA fine-tuning."""
    # Base model identifier
    base_model: str = "Qwen/Qwen2.5-0.5B"
    # LoRA rank (lower = less memory, less expressive)
    lora_rank: int = 8
    # LoRA alpha scaling factor
    lora_alpha: int = 16
    # Target modules for LoRA adaptation
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "v_proj", "k_proj", "o_proj"]
    )
    # Learning rate for fine-tuning
    learning_rate: float = 2e-4
    # Batch size (memory-constrained)
    batch_size: int = 2
    # Gradient accumulation steps
    gradient_accumulation_steps: int = 8
    # Max training examples per night
    max_examples_per_session: int = 500
    # Training duration cap in minutes
    max_training_minutes: int = 15
    # Only train during charging
    require_charging: bool = True
    # Minimum battery level to start training
    min_battery_level: int = 50
    # Training hour window (local time)
    training_window_start: int = 2  # 2 AM
    training_window_end: int = 5    # 5 AM
    # Mixed precision training
    use_mixed_precision: bool = True
    # Gradient checkpointing for memory efficiency
    use_gradient_checkpointing: bool = True
    # Minimum examples before triggering training
    min_examples_for_training: int = 20
    # Quantization for inference (4-bit for low-end devices)
    inference_quantization: str = "q4_k_m"


@dataclass
class FederatedLearningConfig:
    """Configuration for federated aggregation."""
    # Server endpoint for gradient upload
    server_endpoint: str = "https://api.angavu.ai/federated/v1"
    # Differential privacy epsilon (lower = more private)
    # Research recommends ε=0.1 for strong privacy with financial data
    dp_epsilon: float = 0.1
    # Differential privacy delta
    dp_delta: float = 1e-5
    # Gradient clipping norm
    gradient_clip_norm: float = 1.0
    # Aggregation method: "fedavg", "krum", "trimmed_mean"
    aggregation_method: str = "trimmed_mean"
    # Trimmed mean: fraction to trim from each end
    trim_fraction: float = 0.1
    # Minimum cohort size for aggregation
    min_cohort_size: int = 10
    # Maximum staleness (rounds) for async aggregation
    max_staleness: int = 3
    # Upload frequency in hours
    upload_interval_hours: int = 24
    # Enable secure aggregation
    secure_aggregation: bool = True
    # Anomaly detection threshold (standard deviations)
    anomaly_threshold: float = 3.0
    # Model delta compression
    compress_deltas: bool = True
    # Maximum delta upload size in KB
    max_upload_size_kb: int = 1024


@dataclass
class CodeSwitchingConfig:
    """Configuration for code-switching detection and handling."""
    # Enable real-time code-switch detection
    enabled: bool = True
    # Minimum confidence for language boundary detection
    boundary_confidence: float = 0.7
    # Languages to expect in code-switching
    expected_languages: List[str] = field(
        default_factory=lambda: ["swahili", "english", "sheng"]
    )
    # Strategy for handling code-switched input:
    # "unified" = process as single stream
    # "segment" = split and process each segment
    # "cascade" = try primary language first, fall back
    strategy: str = "unified"
    # Sheng vocabulary update frequency
    sheng_vocab_update_hours: int = 168  # weekly


@dataclass
class QualityScoringConfig:
    """Configuration for language quality scoring."""
    # Enable quality scoring
    enabled: bool = True
    # Metrics to track
    metrics: List[str] = field(
        default_factory=lambda: [
            "perplexity", "bleu", "user_satisfaction",
            "correction_rate", "response_coherence",
            "dialect_authenticity", "code_switch_fluency"
        ]
    )
    # Minimum interactions before scoring
    min_interactions_for_scoring: int = 50
    # Report generation interval in hours
    report_interval_hours: int = 168  # weekly
    # Quality threshold below which model triggers retraining
    quality_threshold: float = 0.6
    # Store historical scores for trend analysis
    history_retention_days: int = 90


@dataclass
class PipelineConfig:
    """Master configuration for the entire language training pipeline."""
    dialect_detection: DialectDetectionConfig = field(
        default_factory=DialectDetectionConfig
    )
    voice_collection: VoiceCollectionConfig = field(
        default_factory=VoiceCollectionConfig
    )
    fine_tuning: FineTuningConfig = field(
        default_factory=FineTuningConfig
    )
    federated_learning: FederatedLearningConfig = field(
        default_factory=FederatedLearningConfig
    )
    code_switching: CodeSwitchingConfig = field(
        default_factory=CodeSwitchingConfig
    )
    quality_scoring: QualityScoringConfig = field(
        default_factory=QualityScoringConfig
    )

    # Global settings
    device_profile: str = "low_end"  # "low_end", "mid_range", "high_end"
    debug_mode: bool = False
    log_level: str = "INFO"
    data_directory: str = "data"
    model_directory: str = "models"
