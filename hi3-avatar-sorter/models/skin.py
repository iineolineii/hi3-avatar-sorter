from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..relationships import ManyToOne

if TYPE_CHECKING:
    from .skin_rarity import SkinRarity


@dataclass(kw_only=True)
class Skin(ManyToOne["SkinRarity"]):
    @classmethod
    def by_id(
        cls,
        id: str,
        skin_rarity: "SkinRarity"
    ):
        return super().by_id(id, skin_rarity)
