from enum import IntEnum, StrEnum, auto


class PartIDFormats(StrEnum):
    ICON     = auto()
    SPLASH   = auto()
    FRAGMENT = auto()


class PartNumbers(IntEnum):
    PART1 = 1
    PART2 = 2


__all__ = ["PartIDFormats", "PartNumbers"]
