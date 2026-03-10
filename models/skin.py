from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..relationships import ManyToOne

if TYPE_CHECKING:
    from .skin_rarity import SkinRarity


@dataclass(kw_only=True)
class Skin(ManyToOne["SkinRarity"]):
    @classmethod
    def by_code(
        cls,
        code: int,
        skin_rarity: "SkinRarity"
    ):
        return super().by_code(code, skin_rarity)
