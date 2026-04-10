import sys
from abc import ABCMeta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Avatar
    from .. import Part
    from ... import PartIDFormat

if sys.version_info < (3, 15):
    from frozendict import frozendict


class AvatarMeta(ABCMeta):
    @property
    def parts(cls: type["Avatar"]) -> "frozendict[str, Part]": # pyright: ignore[reportGeneralTypeIssues]
        try:
            return cls.__parts_by_id
        except AttributeError:
            raise AttributeError(
                f"type object {cls.__name__!r} has no attribute 'parts'. "
                f"Maybe you forgot to call {cls.build_part_map.__qualname__!r}?"
            )

    @parts.setter
    def self(cls: type["Avatar"], parts: FrozenContainer[str, Part]) -> None: # pyright: ignore[reportGeneralTypeIssues]
        cls.__parts = parts


__all__ = ["AvatarMeta"]
