"""Shared helpers: text loading, sentence chunking, WAV writing."""
import re
from pathlib import Path

import numpy as np
import soundfile as sf

DEFAULT_INPUT = Path("data/input.txt")
OUTPUT_DIR = Path("output")


def read_text(path: Path) -> str:
    text = Path(path).read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"{path} is empty.")
    return text


def split_sentences(text: str, max_chars: int = 300) -> list[str]:
    """Split text into sentence-sized chunks of at most ~max_chars characters."""
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\r", " ").replace("\n", " "))
    chunks: list[str] = []
    cur = ""
    for part in parts:
        if cur and len(cur) + len(part) + 1 > max_chars:
            chunks.append(cur)
            cur = part
        else:
            cur = f"{cur} {part}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def write_wav(path: Path, audio: np.ndarray, sample_rate: int) -> float:
    """Write mono audio to `path`, creating parent dirs. Returns duration in seconds."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, audio, sample_rate)
    return len(audio) / sample_rate
