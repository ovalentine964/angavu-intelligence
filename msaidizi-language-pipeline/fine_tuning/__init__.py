"""
On-Device Fine-Tuning Pipeline for Msaidizi
=============================================

Implements incremental model learning from user corrections using
LoRA (Low-Rank Adaptation) on-device, inspired by MobileFineTuner
and Confidant frameworks.

Architecture:
  User Interaction → Training Example Creation → Local Dataset →
  LoRA Fine-Tuning (nightly, charging) → Updated Local Adapter →
  Gradient Delta → Federated Learning Client

Key design decisions:
- Qwen 0.5B as base model (runs on $50 Android phones via llama.cpp NDK)
- LoRA rank 8-16 (0.2% trainable parameters = ~1M)
- Training only during charging + idle (2-5 AM window)
- Gradient checkpointing + mixed precision for memory efficiency
- Per-user adapter + per-dialect adapter layered on base model
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TrainingTrigger(Enum):
    """What triggered a training session."""
    SCHEDULED = "scheduled"         # Nightly scheduled training
    CORRECTION = "correction"       # User corrected model output
    QUALITY_DROP = "quality_drop"   # Quality score below threshold
    NEW_DIALECT = "new_dialect"     # New dialect detected, adapt
    MANUAL = "manual"               # Explicit user request


@dataclass
class TrainingExample:
    """A single training example from user interaction."""
    example_id: str
    user_id_hash: str
    input_text: str
    target_text: str              # Expected/corrected output
    dialect: str
    task_type: str                # "question", "advice", "calculation", "chat"
    source: str                   # "correction", "interaction", "feedback"
    quality_weight: float = 1.0   # Higher for corrections vs. interactions
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_training_pair(self) -> Dict[str, str]:
        """Convert to input/target pair for fine-tuning."""
        return {
            "input": self.input_text,
            "target": self.target_text,
        }


@dataclass
class LocalDataset:
    """On-device training dataset with lifecycle management."""

    user_id_hash: str
    examples: List[TrainingExample] = field(default_factory=list)
    max_examples: int = 5000
    min_examples_for_training: int = 20

    def add_example(self, example: TrainingExample) -> bool:
        """Add a training example. Returns True if dataset is ready for training."""
        self.examples.append(example)

        # Evict oldest if over limit
        if len(self.examples) > self.max_examples:
            self.examples = self.examples[-self.max_examples:]

        return self.is_ready_for_training()

    def is_ready_for_training(self) -> bool:
        """Check if we have enough examples to trigger training."""
        return len(self.examples) >= self.min_examples_for_training

    def get_training_batch(self, max_size: int = 500) -> List[Dict[str, str]]:
        """Get a batch of training examples, prioritizing corrections."""
        # Sort: corrections first (higher quality), then by recency
        sorted_examples = sorted(
            self.examples,
            key=lambda e: (e.quality_weight, e.timestamp),
            reverse=True,
        )
        batch = sorted_examples[:max_size]
        return [e.to_training_pair() for e in batch]

    def clear(self) -> None:
        """Clear all training data."""
        self.examples.clear()

    @property
    def size(self) -> int:
        return len(self.examples)

    def save(self, path: str) -> None:
        """Persist dataset to local storage."""
        data = {
            "user_id_hash": self.user_id_hash,
            "examples": [
                {
                    "example_id": e.example_id,
                    "input_text": e.input_text,
                    "target_text": e.target_text,
                    "dialect": e.dialect,
                    "task_type": e.task_type,
                    "source": e.source,
                    "quality_weight": e.quality_weight,
                    "timestamp": e.timestamp,
                }
                for e in self.examples
            ],
        }
        Path(path).write_text(json.dumps(data, indent=2))

    def load(self, path: str) -> None:
        """Load dataset from local storage."""
        data = json.loads(Path(path).read_text())
        self.user_id_hash = data["user_id_hash"]
        self.examples = [
            TrainingExample(
                example_id=e["example_id"],
                user_id_hash=data["user_id_hash"],
                input_text=e["input_text"],
                target_text=e["target_text"],
                dialect=e["dialect"],
                task_type=e["task_type"],
                source=e["source"],
                quality_weight=e["quality_weight"],
                timestamp=e["timestamp"],
            )
            for e in data["examples"]
        ]


@dataclass
class LoRAAdapter:
    """
    Represents a LoRA adapter for a specific purpose.

    Layer hierarchy:
    1. Base model (Qwen 0.5B) — frozen
    2. Domain adapter (finance, business) — pretrained, shared
    3. Dialect adapter (sheng, coastal, etc.) — pretrained, shared
    4. User adapter — personalized, on-device only
    """

    adapter_id: str
    adapter_type: str      # "base", "domain", "dialect", "user"
    dialect: Optional[str] = None
    rank: int = 8
    alpha: int = 16
    target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "v_proj", "k_proj", "o_proj"]
    )
    weights_path: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)
    training_steps: int = 0
    is_active: bool = True

    @property
    def trainable_params(self) -> int:
        """Estimate trainable parameters (rank * 2 * hidden_dim * n_modules)."""
        # Qwen 0.5B: hidden_dim=896, n_heads=14
        hidden_dim = 896
        return self.rank * 2 * hidden_dim * len(self.target_modules)

    def to_config(self) -> Dict[str, Any]:
        """Export adapter configuration."""
        return {
            "adapter_id": self.adapter_id,
            "adapter_type": self.adapter_type,
            "dialect": self.dialect,
            "rank": self.rank,
            "alpha": self.alpha,
            "target_modules": self.target_modules,
            "trainable_params": self.trainable_params,
            "training_steps": self.training_steps,
        }


@dataclass
class DeviceCapabilities:
    """Device hardware profile for adaptive training."""

    ram_mb: int = 4000
    cpu_cores: int = 4
    cpu_arch: str = "arm64"
    has_gpu: bool = False
    gpu_ram_mb: int = 0
    storage_free_mb: int = 2000
    battery_level: int = 100
    is_charging: bool = False
    is_idle: bool = True
    current_hour: int = 12

    @property
    def can_train(self) -> bool:
        """Check if device conditions allow training."""
        return (
            self.ram_mb >= 3000 and
            self.storage_free_mb >= 500 and
            self.battery_level >= 50 and
            self.is_charging and
            self.is_idle
        )

    @property
    def optimal_lora_rank(self) -> int:
        """Determine optimal LoRA rank based on device capabilities."""
        if self.ram_mb >= 6000:
            return 16
        elif self.ram_mb >= 4000:
            return 8
        else:
            return 4

    @property
    def optimal_batch_size(self) -> int:
        """Determine optimal batch size."""
        if self.ram_mb >= 6000:
            return 4
        elif self.ram_mb >= 4000:
            return 2
        else:
            return 1


@dataclass
class TrainingConfig:
    """Configuration for a single training run."""

    base_model: str = "Qwen/Qwen2.5-0.5B"
    lora_rank: int = 8
    lora_alpha: int = 16
    learning_rate: float = 2e-4
    batch_size: int = 2
    gradient_accumulation_steps: int = 8
    max_steps: int = 100
    warmup_steps: int = 10
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    use_mixed_precision: bool = True
    use_gradient_checkpointing: bool = True
    save_steps: int = 50
    logging_steps: int = 10


@dataclass
class FineTuningPipeline:
    """
    On-device LoRA fine-tuning pipeline.

    Runs during charging/idle hours (2-5 AM by default).
    Produces gradient deltas for federated learning.
    """

    device_caps: DeviceCapabilities
    training_config: TrainingConfig = field(default_factory=TrainingConfig)
    adapters: Dict[str, LoRAAdapter] = field(default_factory=dict)
    datasets: Dict[str, LocalDataset] = field(default_factory=dict)

    # Training state
    _is_training: bool = False
    _last_training_time: float = 0
    _training_history: List[Dict[str, Any]] = field(default_factory=list)

    # Callbacks
    _on_training_complete: Optional[Callable] = None
    _on_training_progress: Optional[Callable] = None

    def add_training_example(
        self,
        user_id_hash: str,
        input_text: str,
        target_text: str,
        dialect: str,
        task_type: str = "chat",
        source: str = "interaction",
        quality_weight: float = 1.0,
    ) -> bool:
        """
        Add a training example from user interaction.

        Returns True if training should be triggered.
        """
        if user_id_hash not in self.datasets:
            self.datasets[user_id_hash] = LocalDataset(user_id_hash=user_id_hash)

        example = TrainingExample(
            example_id=f"{user_id_hash}_{int(time.time())}",
            user_id_hash=user_id_hash,
            input_text=input_text,
            target_text=target_text,
            dialect=dialect,
            task_type=task_type,
            source=source,
            quality_weight=quality_weight,
        )

        dataset = self.datasets[user_id_hash]
        return dataset.add_example(example)

    def add_correction(
        self,
        user_id_hash: str,
        original_input: str,
        incorrect_output: str,
        correct_output: str,
        dialect: str,
    ) -> bool:
        """
        Add a user correction (highest quality training signal).

        User corrections are weighted 3x normal interactions because
        they represent explicit knowledge of what the model got wrong.
        """
        return self.add_training_example(
            user_id_hash=user_id_hash,
            input_text=original_input,
            target_text=correct_output,
            dialect=dialect,
            task_type="correction",
            source="correction",
            quality_weight=3.0,
        )

    def should_train(self, user_id_hash: str) -> Tuple[bool, str]:
        """
        Check if training should be triggered.

        Returns (should_train, reason).
        """
        # Check device conditions
        if not self.device_caps.can_train:
            return False, "device_not_ready"

        # Check if already training
        if self._is_training:
            return False, "already_training"

        # Check if enough time since last training
        min_interval = 3600 * 6  # 6 hours minimum between training sessions
        if time.time() - self._last_training_time < min_interval:
            return False, "too_soon"

        # Check dataset readiness
        dataset = self.datasets.get(user_id_hash)
        if not dataset or not dataset.is_ready_for_training():
            return False, "insufficient_data"

        # Check if within training window
        hour = self.device_caps.current_hour
        if not (2 <= hour <= 5):
            return False, "outside_training_window"

        return True, "ready"

    def start_training(self, user_id_hash: str) -> Dict[str, Any]:
        """
        Start a fine-tuning session.

        Returns training results including gradient delta.
        """
        should, reason = self.should_train(user_id_hash)
        if not should:
            return {"status": "skipped", "reason": reason}

        self._is_training = True
        start_time = time.time()

        try:
            # Get training batch
            dataset = self.datasets[user_id_hash]
            batch = dataset.get_training_batch(
                max_size=self.training_config.max_steps * self.training_config.batch_size
            )

            # Configure adapter for this user's dialect
            adapter = self._get_or_create_adapter(user_id_hash, dataset.examples[0].dialect)

            # Run training (in production: llama.cpp NDK LoRA training)
            result = self._run_lora_training(batch, adapter)

            # Update training state
            adapter.training_steps += result.get("steps", 0)
            adapter.last_updated = time.time()
            self._last_training_time = time.time()

            # Record history
            history_entry = {
                "user_id_hash": user_id_hash,
                "timestamp": time.time(),
                "duration_seconds": time.time() - start_time,
                "steps": result.get("steps", 0),
                "loss": result.get("final_loss", 0.0),
                "examples_used": len(batch),
                "adapter_id": adapter.adapter_id,
            }
            self._training_history.append(history_entry)

            # Trigger callback
            if self._on_training_complete:
                self._on_training_complete(history_entry)

            return {
                "status": "completed",
                "adapter_id": adapter.adapter_id,
                "gradient_delta": result.get("gradient_delta"),
                "loss": result.get("final_loss", 0.0),
                "steps": result.get("steps", 0),
                "duration_seconds": time.time() - start_time,
            }

        except Exception as e:
            logger.error(f"Training failed for {user_id_hash}: {e}")
            return {"status": "failed", "error": str(e)}

        finally:
            self._is_training = False

    def get_user_adapter(self, user_id_hash: str) -> Optional[LoRAAdapter]:
        """Get the current adapter for a user."""
        return self.adapters.get(f"user_{user_id_hash}")

    def get_dialect_adapter(self, dialect: str) -> Optional[LoRAAdapter]:
        """Get the shared adapter for a dialect."""
        return self.adapters.get(f"dialect_{dialect}")

    def _get_or_create_adapter(
        self, user_id_hash: str, dialect: str
    ) -> LoRAAdapter:
        """Get or create a user adapter, layered on dialect adapter."""
        adapter_key = f"user_{user_id_hash}"

        if adapter_key not in self.adapters:
            rank = self.device_caps.optimal_lora_rank
            self.adapters[adapter_key] = LoRAAdapter(
                adapter_id=adapter_key,
                adapter_type="user",
                dialect=dialect,
                rank=rank,
                alpha=rank * 2,
            )

        return self.adapters[adapter_key]

    def _run_lora_training(
        self,
        batch: List[Dict[str, str]],
        adapter: LoRAAdapter,
    ) -> Dict[str, Any]:
        """
        Run LoRA fine-tuning on the given batch.

        In production, this calls llama.cpp NDK's LoRA training API.
        Here we simulate the training loop structure.
        """
        config = self.training_config

        # Adapt config to device capabilities
        config.batch_size = self.device_caps.optimal_batch_size
        config.lora_rank = adapter.rank

        # Simulate training loop
        # In production: llama_cpp.lora_train(batch, config)
        steps = min(len(batch) // config.batch_size, config.max_steps)
        final_loss = 2.5  # Placeholder — would be actual loss

        # Generate gradient delta (LoRA weight changes)
        # In production: extract actual LoRA weight deltas
        gradient_delta = self._compute_gradient_delta(adapter, batch)

        return {
            "steps": steps,
            "final_loss": final_loss,
            "gradient_delta": gradient_delta,
        }

    def _compute_gradient_delta(
        self,
        adapter: LoRAAdapter,
        batch: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Compute the gradient delta for federated learning.

        Returns only the LoRA weight changes (not raw data).
        In production, this extracts actual weight deltas from the
        training loop and applies differential privacy.
        """
        return {
            "adapter_id": adapter.adapter_id,
            "adapter_type": adapter.adapter_type,
            "dialect": adapter.dialect,
            "rank": adapter.rank,
            "trainable_params": adapter.trainable_params,
            "steps": len(batch),
            # In production: actual weight deltas, clipped and noised
            "weight_delta_summary": {
                "l2_norm": 0.0,  # Placeholder
                "max_abs": 0.0,
                "mean_abs": 0.0,
            },
        }

    def export_training_history(self) -> List[Dict[str, Any]]:
        """Export training history for quality analysis."""
        return list(self._training_history)
