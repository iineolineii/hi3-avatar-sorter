from ..relationships import ManyToOne, OneToMany
from .valkyrie import Valkyrie
from .skin_rarity import SkinRarity


from frozendict import frozendict


from dataclasses import dataclass, field


@dataclass
class Battlesuit(OneToMany["SkinRarity"], ManyToOne["Valkyrie"]):
    code: int

    no: int = field(init=False)

    # We don't use default_factory here because this field
    # will be replaced by __children in Container.__post_init__
    skins_rarities: 'frozendict[int, "SkinRarity"]' = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_skin_rarity` method
    """

    @classmethod
    def by_code(
        cls,
        code: int,
        valkyrie: Valkyrie
    ):
        if code in valkyrie.battlesuits:
            return valkyrie.battlesuits[code]

        return cls(code)

    def add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self._add_child(skin_rarity)
