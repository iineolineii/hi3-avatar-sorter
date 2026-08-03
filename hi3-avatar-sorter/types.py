from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from .utils import RawAvatar


PartNumber:   TypeAlias = int
ValkyrieID:   TypeAlias = int | str
BattlesuitID: TypeAlias = int | str
SkinRarityID: TypeAlias = int | str
SkinID:       TypeAlias = int | str
Note:         TypeAlias = str


AvatarComponents: TypeAlias = """
      tuple[PartNumber, ValkyrieID, BattlesuitID]
    | tuple[PartNumber, ValkyrieID, BattlesuitID, Note]
    | tuple[PartNumber, ValkyrieID, BattlesuitID, SkinRarityID, SkinID]
    | tuple[PartNumber, ValkyrieID, BattlesuitID, SkinRarityID, SkinID, Note]
"""

AvatarComponentsSuffix: TypeAlias = """
      tuple[None, None, None]
    | tuple[None, None, Note]
    | tuple[SkinRarityID, SkinID, None]
    | tuple[SkinRarityID, SkinID, Note]
"""

ReplacementMap: TypeAlias = dict[str, "RawAvatar"]
RawReplacementMap: TypeAlias = dict[AvatarComponents, AvatarComponents]
