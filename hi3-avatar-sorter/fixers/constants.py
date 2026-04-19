import sys
from typing import TYPE_CHECKING, TypeAlias

if sys.version_info < (3, 15):
    from frozendict import frozendict

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

ReplacementMap: TypeAlias = frozendict[str, "RawAvatar"]
RawReplacementMap: TypeAlias = dict[AvatarComponents, AvatarComponents]


KIANA:     ValkyrieID = 1
KALLEN:    ValkyrieID = KIANA
MEI:       ValkyrieID = 2
SAKURA:    ValkyrieID = MEI
BRONYA:    ValkyrieID = 3
THERESA:   ValkyrieID = 4
HIMEKO:    ValkyrieID = 5
RITA:      ValkyrieID = 7
ELYSIA_P2: ValkyrieID = 10
ELYSIA_P1: ValkyrieID = 22
