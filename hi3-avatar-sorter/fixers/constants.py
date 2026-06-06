from types import MappingProxyType
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from ..models.avatar import RawAvatar


PartNo:       TypeAlias = int
ValkyrieID:   TypeAlias = int | str
BattlesuitID: TypeAlias = int | str
SkinRarityID: TypeAlias = int | str
SkinID:       TypeAlias = int | str
Note:         TypeAlias = str

AvatarComponents: TypeAlias = (
      tuple[PartNo, ValkyrieID, BattlesuitID]
    | tuple[PartNo, ValkyrieID, BattlesuitID, Note]
    | tuple[PartNo, ValkyrieID, BattlesuitID, SkinRarityID, SkinID]
    | tuple[PartNo, ValkyrieID, BattlesuitID, SkinRarityID, SkinID, Note]
)

ReplacementMap: TypeAlias = MappingProxyType[str, "RawAvatar"]
RawReplacementMap: TypeAlias = dict[AvatarComponents, AvatarComponents]


KIANA     = 1
KALLEN    = KIANA
MEI       = 2
SAKURA    = MEI
BRONYA    = 3
HIMEKO    = 4
THERESA   = 5
THELEMA   = 5
LANTERN   = 6
RITA      = 7
ELYSIA_P2 = 10
ELYSIA_P1 = 22


__all__ = [
    "AvatarComponents",
    "BRONYA",
    "BattlesuitID",
    "ELYSIA_P1",
    "ELYSIA_P2",
    "HIMEKO",
    "THELEMA",
    "LANTERN",
    "KALLEN",
    "KIANA",
    "MEI",
    "Note",
    "PartNo",
    "RITA",
    "RawReplacementMap",
    "ReplacementMap",
    "SAKURA",
    "SkinID",
    "SkinRarityID",
    "THERESA",
    "ValkyrieID",
]
