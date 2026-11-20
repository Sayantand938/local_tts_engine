# CLAUDE.md

Local text-to-speech toolkit: Kitten TTS 2 Mini, Kyutai Pocket TTS and Kokoro-82M behind one launcher.

## Do NOT read or scan
- `.venv/` — Python virtual environment (tens of thousands of files)
- `output/` — generated audio (binary)

Never glob/grep/list recursively from the project root without excluding these. List the root with depth 0 only.

## Layout
- `tts.py` — thin entry point (`python tts.py` == `python -m localtts`)
- `localtts/cli.py` — Typer launcher: interactive questionary prompts (arrow-key menus) or flags; any omitted option is prompted
- `localtts/core.py` — shared helpers: `read_text`, `split_sentences`, `write_wav`, default paths
- `localtts/engines/base.py` — `Engine` ABC (`name`, `label`, `voices`, `supports_speed`, `accepts_custom_voice`, `synthesize()`)
- `localtts/engines/{kitten,pocket,kokoro}.py` — one engine each; heavy imports and model loading are lazy inside `synthesize()`
- `localtts/engines/__init__.py` — `ENGINES` registry
- `data/input.txt` — default input text
- `output/` — generated WAVs
- `requirements.txt`, `README.md`, `STATUS.md`

## Adding an engine
Subclass `Engine` in `localtts/engines/<name>.py`, import lazily inside `synthesize()`, and add an instance to `ENGINES` in `localtts/engines/__init__.py`. The CLI picks it up automatically.

## Usage
```powershell
.\.venv\Scripts\python.exe tts.py
.\.venv\Scripts\python.exe tts.py -e kokoro -v bf_emma -s 1.0 data/input.txt -o output/out.wav
.\.venv\Scripts\python.exe tts.py --list-voices
```

## Notes
- Install packages with `uv pip install --python .venv/Scripts/python.exe <pkg>` (the venv has no pip).
- Kitten sets `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` inside its engine (HF cache only). Pocket and Kokoro download their models on first run.
- Avoid emoji/non-ASCII in `typer.echo` output (Windows console encoding errors).
- Omitted CLI flags prompt on stdin; pass all of them for non-interactive runs.
- Models are reloaded on every invocation.
- Git repository (ignores .venv, output/, *.wav).
- See `STATUS.md` for current progress.
