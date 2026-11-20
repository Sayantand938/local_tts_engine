# Local TTS Toolkit

Three local text-to-speech engines behind one launcher. Output is a 24 kHz WAV.

| Engine | Model | Notes |
|---|---|---|
| `kitten` | Kitten TTS 2 Mini | Fast, offline (HF cache), speed control |
| `pocket` | Kyutai Pocket TTS | 8 voices or clone from a WAV, no speed control |
| `kokoro` | Kokoro-82M | US/UK English voices, speed control |

## Setup

Windows, with a [uv](https://docs.astral.sh/uv/)-managed `.venv` (no pip):

```powershell
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
```

Pocket and Kokoro download their models on first run.

## Usage

Put your text in `data/input.txt`, then run:

```powershell
.\.venv\Scripts\python.exe tts.py
```

You'll be prompted for engine, voice, speed, input file and output file. Pass flags to skip prompts (give all of them for a non-interactive run):

```powershell
.\.venv\Scripts\python.exe tts.py -e kokoro -v bf_emma -s 1.0 data/input.txt -o output/out.wav
.\.venv\Scripts\python.exe tts.py -e pocket -v C:\path\to\sample.wav data/input.txt -o output/cloned.wav
.\.venv\Scripts\python.exe tts.py --list-voices
```

| Flag | Meaning |
|---|---|
| `-e` | Engine |
| `-v` | Voice (Pocket: name or WAV path) |
| `-s` | Speed (Kitten, Kokoro) |
| `-o` | Output WAV |
| first arg | Input text file |

## Layout

- `tts.py` is the entry point (same as `python -m localtts`)
- `localtts/cli.py` is the launcher
- `localtts/core.py` has the shared helpers
- `localtts/engines/` has one module per engine plus the registry

To add an engine, subclass `Engine` in `localtts/engines/` and register it in `localtts/engines/__init__.py`.

## Troubleshooting

- **Seems to hang:** it's waiting at a prompt. Answer it or pass every flag.
- **Console encoding errors:** avoid emoji and non-ASCII in output.
- **Kitten can't find its model:** it forces HF offline mode, so download the model once with the offline variables unset.
