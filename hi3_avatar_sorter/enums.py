from enum import StrEnum, auto
from typing import Any


class PartIDFormat(StrEnum):
    ICON     = auto()
    SPLASH   = auto()
    FRAGMENT = auto()


__all__ = ["PartIDFormat"]
