import numpy as np

from .base import Engine

REPO_ID = "hexgrad/Kokoro-82M"
SAMPLE_RATE = 24000


class KokoroEngine(Engine):
    name = "kokoro"
    label = "Kokoro-82M (US/UK English voices)"
    voices = [
        "af_heart", "af_bella", "af_nicole", "af_sarah", "af_sky",
        "am_adam", "am_michael",
        "bf_emma", "bf_isabella", "bm_george", "bm_lewis",
    ]
    default_voice = "am_michael"
    supports_speed = True

    def synthesize(self, text, voice, speed=1.0):
        from kokoro import KPipeline

        # First letter of the voice name is the language code (a=US, b=UK).
        pipeline = KPipeline(lang_code=voice[0], repo_id=REPO_ID)
        parts = [
            r.audio.numpy()
            for r in pipeline(text, voice=voice, speed=speed, split_pattern=r"\n+")
            if r.audio is not None
        ]
        if not parts:
            raise RuntimeError("Kokoro produced no audio.")
        return np.concatenate(parts), SAMPLE_RATE
