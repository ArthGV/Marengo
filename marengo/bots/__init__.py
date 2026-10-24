"""Each module in this package (v1.py, v2.py, ...) exposes `bot(board) -> chess.Move`."""
import importlib
import pkgutil
from typing import Callable

import chess

Bot = Callable[[chess.Board], chess.Move]


def available() -> list[str]:
    return sorted(m.name for m in pkgutil.iter_modules(__path__))


def load_bot(name: str) -> Bot:
    try:
        return importlib.import_module(f"marengo.bots.{name}").bot
    except ModuleNotFoundError:
        raise SystemExit(f"Unknown bot '{name}'. Available: {', '.join(available())}")
