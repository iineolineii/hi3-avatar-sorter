from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from frozendict import frozendict

from ..relationships import ManyToOne, OneToMany

if TYPE_CHECKING:
    from .battlesuit import Battlesuit
    from .skin import Skin


@dataclass(kw_only=True)
class SkinRarity(OneToMany["Skin"], ManyToOne["Battlesuit"]):
    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    skins: "frozendict[int, Skin]" = field(default=frozendict(), hash=False, compare=False)
    """
    This field should not be updated from outside.
    Instead, use the `add_skin` method
    """

    @classmethod
    def by_id(
        cls,
        id: int,
        battlesuit: "Battlesuit"
    ):
        return super().by_id(id, battlesuit)

    def add_skin(self, skin: "Skin") -> "Skin":
        return self._add_child(skin)
