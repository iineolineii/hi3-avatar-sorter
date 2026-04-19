from dataclasses import dataclass, field

from .base import BaseModel
from .skin_rarity import SkinRarity
from ..mex_container import MexContainer


@dataclass
class Battlesuit(BaseModel):
    skin_rarities: "MexContainer[str, SkinRarity]" = field(default_factory=MexContainer) # pyright: ignore[reportAssignmentType]

    def add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        self.skin_rarities[skin_rarity.id] = skin_rarity
        return skin_rarity

    def get_or_add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self.skin_rarities.setdefault(skin_rarity.id, skin_rarity)


__all__ = ["Battlesuit"]
