from abc import ABC, abstractmethod

import numpy as np


class Engine(ABC):
    """A TTS backend. Heavy imports and model loading happen lazily in synthesize()."""

    name: str
    label: str
    voices: list[str]
    default_voice: str
    supports_speed: bool = False
    accepts_custom_voice: bool = False  # e.g. a WAV path for voice cloning

    @property
    def default_output(self) -> str:
        return f"{self.name}.wav"

    @abstractmethod
    def synthesize(self, text: str, voice: str, speed: float = 1.0) -> tuple[np.ndarray, int]:
        """Return (mono float audio, sample_rate)."""
