from ..core import split_sentences
from .base import Engine


class PocketEngine(Engine):
    name = "pocket"
    label = "Kyutai Pocket TTS (voice cloning from a WAV)"
    voices = ["alba", "marius", "javert", "jean", "fantine", "cosette", "eponine", "azelma"]
    default_voice = "alba"
    accepts_custom_voice = True

    def synthesize(self, text, voice, speed=1.0):
        import torch
        from pocket_tts import TTSModel

        model = TTSModel.load_model()
        state = model.get_state_for_audio_prompt(voice)
        # The model caps tokens per call, so synthesize sentence-sized chunks.
        chunks = [model.generate_audio(state, c, max_tokens=200) for c in split_sentences(text)]
        return torch.cat(chunks).numpy(), model.sample_rate
