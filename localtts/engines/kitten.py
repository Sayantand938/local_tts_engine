import os

import numpy as np

from .base import Engine

MODEL_NAME = "KittenML/kitten-tts-2-mini"


class KittenEngine(Engine):
    name = "kitten"
    label = "Kitten TTS 2 Mini (offline, fast)"
    voices = ["Eleanor", "Martha", "Serena", "Iris", "Grace", "Edith", "Diana", "Otis", "Vincent", "Max", "Danny"]
    default_voice = "Eleanor"
    supports_speed = True

    def synthesize(self, text, voice, speed=1.0):
        # Use only the local HF cache; must be set before kittenml/huggingface_hub load.
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        from kittenml import KittenTTS

        model = KittenTTS(MODEL_NAME)
        audio = model.generate(text, voice=voice, speed=speed)
        return np.asarray(audio), model.sample_rate
