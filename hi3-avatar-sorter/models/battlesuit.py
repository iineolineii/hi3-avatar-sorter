from dataclasses import dataclass, field

from .base import BaseModel
from .skin_rarity import SkinRarity
from ..containers import MutableContainer


@dataclass
class Battlesuit(BaseModel):
    skin_rarities: "MutableContainer[str, SkinRarity]" = field(default_factory=MutableContainer) # pyright: ignore[reportAssignmentType]

    def add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        self.skin_rarities[skin_rarity.id] = skin_rarity
        return skin_rarity

    def get_or_add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self.skin_rarities.get(skin_rarity.id, skin_rarity)

    def reserve_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self.skin_rarities.reserve(skin_rarity.id, skin_rarity, int(skin_rarity.id))


__all__ = ["Battlesuit"]
