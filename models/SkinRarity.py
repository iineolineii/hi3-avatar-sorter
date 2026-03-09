from ..relationships import ManyToOne, OneToMany
from .Battlesuit import Battlesuit
from .Skin import Skin


from frozendict import frozendict


from dataclasses import dataclass, field


@dataclass
class SkinRarity(OneToMany["Skin"], ManyToOne["Battlesuit"]):
    code: int

    no: int = field(init=False)

    # We don't use default_factory here because this field
    # will be replaced by __children in Container.__post_init__
    skins: frozendict[int, "Skin"] = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_skin` method
    """

    @classmethod
    def by_code(
        cls,
        code: int,
        battlesuit: Battlesuit
    ):
        if code in battlesuit.skins_rarities:
            return battlesuit.skins_rarities[code]

        return cls(code)

    def add_skin(self, skin: "Skin") -> "Skin":
        return self._add_child(skin)
