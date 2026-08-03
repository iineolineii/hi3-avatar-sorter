from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..utils import RawAvatar

if TYPE_CHECKING:
    from ..types import (
        RawReplacementMap,
        ReplacementMap,
    )
    from ..registry import AvatarRegistry


@dataclass(frozen=True)
class AvatarFixer:
    registry: "AvatarRegistry"
    raw_replacement_map: "RawReplacementMap"

    replacement_map: "ReplacementMap" = field(init=False, repr=False, default_factory=dict)

    def __post_init__(self) -> None:
        self.replacement_map.update(self.build_replacement_map(self.raw_replacement_map))


    def fix(self, avatar_string: str) -> "RawAvatar | None":
        return self.replacement_map.get(avatar_string)


    def build_replacement_map(self, raw_replacement_map: "RawReplacementMap") -> dict[str, "RawAvatar"]:
        replacement_map: dict[str, "RawAvatar"] = {}

        for malformed_components, fixed_components in raw_replacement_map.items():
            malformed_dtos = RawAvatar.from_components(malformed_components, self.registry, preserve_strings=True)
            fixed_dtos = RawAvatar.from_components(fixed_components, self.registry, preserve_strings=False)

            for malformed_dto, fixed_dto in zip(malformed_dtos, fixed_dtos, strict=True):
                malformed_string = str(malformed_dto)
                replacement_map[malformed_string] = fixed_dto

        return replacement_map


__all__ = ["AvatarFixer"]
