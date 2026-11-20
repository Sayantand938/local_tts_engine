# STATUS

Last updated: 2026-11-21

## Working
- Refactored into the `localtts` package: `core.py` (shared helpers), `cli.py` (interactive launcher) and one engine class per backend under `localtts/engines/`.
- All three engines tested through `python -m localtts` on `data/input.txt`: kitten (50s), pocket (39s), kokoro (44s), all 24 kHz.
- Kitten: `KittenML/kitten-tts-2-mini` from the HF cache, offline. Voice and speed.
- Pocket: Kyutai Pocket TTS 4.0.1, 8 built-in voices or WAV cloning, sentence chunking. Downloads model on first run.
- Kokoro: `hexgrad/Kokoro-82M` via the `kokoro` package. Voice and speed. Downloads model on first run.
- `tts.py` launcher: interactive menu or flags; `--list-voices`.

## Known limitations / TODO
- Models are loaded on every run (no batch/server mode).
- Kitten and Kokoro do not use the shared sentence chunking; very long inputs are untested.
- Voice lists are hardcoded (Kitten: English only; Kokoro: curated US/UK set).
- `requirements.txt` is unpinned.
- Pocket voice cloning from a WAV path is untested.
- No tests.


## Ideas
- Playback option after generation.
- Add Zonos3 Mini (C++/ggml route, CPU) as a fourth engine.
- Per-engine language selection for Kitten.
