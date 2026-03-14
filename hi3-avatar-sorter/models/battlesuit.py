from dataclasses import dataclass
from typing import TYPE_CHECKING

from frozendict import frozendict

from ..relationships import ManyToOne, OneToMany

if TYPE_CHECKING:
    from .skin_rarity import SkinRarity
    from .valkyrie import Valkyrie


@dataclass(kw_only=True)
class Battlesuit(OneToMany["SkinRarity"], ManyToOne["Valkyrie"]):
    id: str

    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    skins_rarities: 'frozendict[int, "SkinRarity"]' = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_skin_rarity` method
    """

    @classmethod
    def by_id(
        cls,
        id: str,
        valkyrie: "Valkyrie"
    ):
        return super().by_id(id, valkyrie)

    def add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self._add_child(skin_rarity)
