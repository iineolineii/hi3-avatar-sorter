from collections.abc import Iterator
from dataclasses import dataclass, field

from frozendict import frozendict

from .constants import AvatarComponents, RawReplacementMap, ReplacementMap
from ..enums import PartIDFormats
from ..models import Avatar
from ..models.avatar import RawAvatar


@dataclass(frozen=True, slots=True)
class AvatarFixer:
    part_id_format: PartIDFormats
    raw_replacement_map: "RawReplacementMap"

    replacement_map: "ReplacementMap" = field(init=False, repr=False)

    def __post_init__(self) -> None:
        replacement_map = self.build_replacement_map(self.raw_replacement_map)
        object.__setattr__(self, "replacement_map", frozendict(replacement_map))

    def fix(self, avatar_string: str) -> RawAvatar | None:
        return self.replacement_map.get(avatar_string)

    def build_replacement_map(self, raw_replacement_map: "RawReplacementMap") -> dict[str, RawAvatar]:
        replacement_map: dict[str, RawAvatar] = {}

        for malformed_components, fixed_components in raw_replacement_map.items():
            malformed_dtos = self.dto_from_components(malformed_components)
            fixed_dtos = self.dto_from_components(fixed_components)

            for malformed_dto, fixed_dto in zip(malformed_dtos, fixed_dtos, strict=True):
                malformed_string = str(malformed_dto).lstrip("0")
                replacement_map[malformed_string] = fixed_dto

        return replacement_map

    def dto_from_components(self, avatar_components: "AvatarComponents") -> Iterator[RawAvatar]:
        part_no = avatar_components[0]
        parts = Avatar.get_part_by_no(part_no, self.part_id_format)

        for part in parts:
            normalized_components = [part.id, *avatar_components[1:]]

            yield RawAvatar.from_iterable(
                normalized_components,
                validate=True,
                validate_string_ids=False,
            )
