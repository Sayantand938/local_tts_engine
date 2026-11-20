from .base import Engine
from .kitten import KittenEngine
from .kokoro import KokoroEngine
from .pocket import PocketEngine

ENGINES: dict[str, Engine] = {e.name: e for e in (KittenEngine(), PocketEngine(), KokoroEngine())}

__all__ = ["Engine", "ENGINES"]
