# Local TTS Toolkit

Three local text-to-speech engines behind one launcher:

| Engine | Model | Notes |
|---|---|---|
| `kitten` | Kitten TTS 2 Mini (`KittenML/kitten-tts-2-mini`) | Fast, runs fully offline from the Hugging Face cache. Speed control. |
| `pocket` | Kyutai Pocket TTS | 8 built-in voices, or clone a voice from a WAV file. No speed option. |
| `kokoro` | Kokoro-82M (`hexgrad/Kokoro-82M`) | US and UK English voices. Speed control. |

Output is a 24 kHz WAV file.

## Requirements

- Windows with Python in the project's `.venv` (created with [uv](https://docs.astral.sh/uv/); the venv has no pip).
- Packages: `typer`, `questionary`, `soundfile`, `kittenml`, `pocket-tts`, `kokoro`.
- Internet on the first run of Pocket and Kokoro, to download their models. They use the Hugging Face cache afterwards.

Install a missing package with:

```powershell
uv pip install --python .venv/Scripts/python.exe <package>
```

## Quick start

1. Put the text you want spoken in `data/input.txt` (UTF-8).
2. Run the launcher:

```powershell
.\.venv\Scripts\python.exe tts.py
```

It asks you, in order:

1. **Engine**: kitten, pocket or kokoro
2. **Voice**: pick from the list (Pocket also lets you enter a WAV path to clone a voice)
3. **Speed**: Kitten and Kokoro only (1.0 is normal)
4. **Input text file**: default `data/input.txt`
5. **Output WAV file**: default is `output/<engine>.wav`

Use the arrow keys and Enter to choose. Text prompts show a default you can accept with Enter, and Ctrl+C cancels. Prompts use [questionary](https://github.com/tmbo/questionary).

## Skipping the prompts

Pass flags to answer questions up front. Any flag you leave out is still asked, so give all of them for a fully non-interactive run.

| Flag | Meaning |
|---|---|
| `-e`, `--engine` | `kitten`, `pocket` or `kokoro` |
| `-v`, `--voice` | Voice name (Pocket: name or WAV path) |
| `-s`, `--speed` | Speech speed (Kitten, Kokoro) |
| `-o`, `--output` | Output WAV path |
| first argument | Input text file |

Examples:

```powershell
.\.venv\Scripts\python.exe tts.py -e kokoro -v bf_emma -s 1.0 data/input.txt -o output/out.wav
.\.venv\Scripts\python.exe tts.py -e kitten -v Max -s 1.2 data/input.txt -o output/out.wav
.\.venv\Scripts\python.exe tts.py -e pocket -v alba data/input.txt -o output/out.wav
.\.venv\Scripts\python.exe tts.py -e pocket -v C:\path\to\sample.wav data/input.txt -o output/cloned.wav
```

## Voices

- **Kitten (English):** Eleanor, Martha, Serena, Iris, Grace, Edith, Diana, Otis, Vincent, Max, Danny
- **Pocket:** alba, marius, javert, jean, fantine, cosette, eponine, azelma, or a path to a WAV file
- **Kokoro:** af_heart, af_bella, af_nicole, af_sarah, af_sky, am_adam, am_michael, bf_emma, bf_isabella, bm_george, bm_lewis. The first letter is the language (`a` US English, `b` UK English), the second is gender (`f`/`m`).

`python tts.py --list-voices` prints these lists. The menu shows them too. The Kitten model has more languages and the Kokoro model has more voices than the menu shows. You can pass any valid name with `-v`.

## Project layout

| Path | Purpose |
|---|---|
| `tts.py` | Entry point (same as `python -m localtts`) |
| `localtts/cli.py` | Interactive launcher |
| `localtts/core.py` | Shared helpers (text, chunking, WAV writing) |
| `localtts/engines/` | One module per engine, plus the registry |
| `data/input.txt` | Default input text |
| `output/` | Generated audio |
| `requirements.txt` | Dependencies |

To add an engine, subclass `Engine` in `localtts/engines/`, then register it in `localtts/engines/__init__.py`. The menu and flags pick it up.

## Tips and troubleshooting

- The script appears to hang: it is probably waiting at a prompt. Pass every flag, or answer the prompt.
- Models load on every run, so the first seconds are model loading, not synthesis.
- Pocket does not support `--speed`; the flag is ignored with a note.
- Avoid emoji or non-ASCII characters in script output; the Windows console can raise encoding errors.
- Kitten forces Hugging Face offline mode. If its model is missing from the cache, download it once with the offline variables unset.
