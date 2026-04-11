import sys
from dataclasses import dataclass, field
from functools import lru_cache, partial
from typing import TypeAlias

from sortedcontainers import SortedDict

from . import PartIDFormat
from .models import Avatar
from .models.avatar import RawAvatar

if sys.version_info < (3, 15):
    from frozendict import frozendict


KIANA = 1
KALLEN = KIANA
MEI = 2
SAKURA = MEI
BRONYA = 3
THERESA = 4
HIMEKO = 5
RITA = 7
ELYSIA_P2 = 10
ELYSIA_P1 = 22


PartNo:       TypeAlias = int
ValkyrieID:   TypeAlias = int | str
BattlesuitID: TypeAlias = int | str
SkinRarityID: TypeAlias = int | str
SkinID:       TypeAlias = int | str
Note:         TypeAlias = str

AvatarComponents: TypeAlias = (
    tuple[PartNo, ValkyrieID, BattlesuitID] |
    tuple[PartNo, ValkyrieID, BattlesuitID, Note] |
    tuple[PartNo, ValkyrieID, BattlesuitID, SkinRarityID, SkinID] |
    tuple[PartNo, ValkyrieID, BattlesuitID, SkinRarityID, SkinID, Note]
)

ReplacementMap: TypeAlias = frozendict[str, str]
RawReplacementMap: TypeAlias = dict[AvatarComponents, AvatarComponents]

@dataclass(frozen=True, slots=True)
class AvatarFixer:
    part_id_format: "PartIDFormat"
    raw_replacement_map: "RawReplacementMap"
    replacement_map: "ReplacementMap" = field(init=False, default_factory=dict) # pyright: ignore[reportAssignmentType]

    def __post_init__(self) -> None:
        self.build_replacement_map()
        object.__setattr__(self, "replacement_map", frozendict(self.replacement_map))


    def fix(self, avatar_string: str) -> str | None:
        return self.replacement_map.get(avatar_string)


    def build_replacement_map(self) -> None:
        for malformed_components, fixed_components in self.raw_replacement_map.items():
            malformed_string = (
                malformed_components if isinstance(malformed_components, str)
                else self._components_to_string(malformed_components)
            )

            fixed_string = self._components_to_string(fixed_components)

            self.replacement_map[malformed_string] = fixed_string # pyright: ignore[reportIndexIssue]


    def _components_to_string(self, avatar_components: "AvatarComponents") -> str:
        part_no = avatar_components[0]
        part = Avatar.get_part(part_no, self.part_id_format)
        string_components = [part.id] + list(avatar_components[1:])

        raw_avatar = RawAvatar.from_iterable(
            string_components,
            validate=True,
            # All string components are preserved as-is because of NOTE#5
            validate_string_ids=False
        )

        return str(raw_avatar)


@dataclass(frozen=True)
class PrefixFixer(AvatarFixer):
    # Keep longer prefixes first to avoid shadowing shorter ones.
    # Reverse order is emulated via key=lambda x: sys.maxsize - len(x).
    replacement_map: "ReplacementMap" = field(
        init=False,
        default_factory=partial(
            SortedDict,
            key=lambda x: sys.maxsize-len(x)
        )
    ) # pyright: ignore[reportAssignmentType]

    @lru_cache
    def fix(self, avatar_string: str) -> str | None: # pyright: ignore[reportIncompatibleMethodOverride]
        for malformed_string, fixed_string in self.replacement_map.items():
            if avatar_string.startswith(malformed_string):
                return fixed_string + avatar_string[len(malformed_string):]



# These avatars' battlesuit IDs are 1 character long instead of 2
TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP: RawReplacementMap = {
    (1, SAKURA, "1", 4, 1): (1, SAKURA, 1, 4, 1)
}

# These avatars' Valkyrie IDs are 1 character long instead of 2
TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP: RawReplacementMap = {
    (1, str(KIANA), 15, 4, 1): (1, KIANA, 15, 4, 1)
}

# These avatars do not have their battlesuit IDs
EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP: RawReplacementMap = {
    (1, KIANA,   "", 4, 1): (1, KIANA,   1, 4, 1),
    (1, MEI,     "", 4, 1): (1, MEI,     1, 4, 1),
    (1, BRONYA,  "", 4, 1): (1, BRONYA,  1, 4, 1),
    (1, THERESA, "", 4, 1): (1, THERESA, 1, 4, 1),
    (1, HIMEKO,  "", 4, 1): (1, HIMEKO,  1, 4, 1)
}

WRONG_ID_REPLACEMENT_MAP: RawReplacementMap = {
    # 3rd Elysia is not a new character
    (2, ELYSIA_P2, 1): (1, ELYSIA_P1, 3),

    # HoV is 5th Kiana, not 3rd Kallen.
    (1, KALLEN, 13): (1, KIANA, 5),

    # This avatar has wrong battlesuit ID.
    (1, RITA, 1, "special"): (1, RITA, 3, "special"),

    # NOTE#1:
    # Because Kallen and Kiana are completely messed up,
    # Kallen's battlesuits were shifted to the 50s range to free room for future
    # Kiana battlesuits.
    #
    # IMPORTANT: For this fix to work, Kiana's max battlesuit ID must also be set
    # to 50 in the Valkyrie map.
    #
    # EDGE CASE: Unrealistically likely to happen, but if a new Kallen battlesuit
    # appears, extend this list accordingly.
    (1, KALLEN, 11): (1, KALLEN, 40+11),
    (1, KALLEN, 12): (1, KALLEN, 40+12),
    (1, KALLEN, 14): (1, KALLEN, 40+14)
}
