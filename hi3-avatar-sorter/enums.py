from enum import IntEnum, StrEnum, auto


class PartIDFormat(StrEnum):
    ICON     = auto()
    SPLASH   = auto()
    FRAGMENT = auto()


class PartNumber(IntEnum):
    PART1 = 1
    PART2 = 2


__all__ = ["PartIDFormat", "PartNumber"]
