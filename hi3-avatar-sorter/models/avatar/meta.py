from abc import ABCMeta
from typing import TYPE_CHECKING

from ..part import Part
from ...containers import FrozenContainer

if TYPE_CHECKING:
    from . import Avatar


class AvatarMeta(ABCMeta):
    @property
    def parts(cls: type["Avatar"]) -> FrozenContainer[str, Part]: # pyright: ignore[reportGeneralTypeIssues]
        try:
            return cls.__parts
        except AttributeError:
            raise AttributeError(
                f"type object {cls.__name__!r} has no attribute 'parts'. "
                f"Maybe you forgot to call {cls.build_part_map.__qualname__!r}?"
            )

    @parts.setter
    def self(cls: type["Avatar"], parts: FrozenContainer[str, Part]) -> None: # pyright: ignore[reportGeneralTypeIssues]
        cls.__parts = parts


__all__ = ["AvatarMeta"]
