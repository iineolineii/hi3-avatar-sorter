import sys
from dataclasses import dataclass, field

from .container import Container
from .skin_rarity import SkinRarity

if sys.version_info <= (3, 15):
    from frozendict import frozendict


@dataclass(kw_only=True)
class Battlesuit(Container[SkinRarity]):
    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    skin_rarities: "frozendict[str, SkinRarity]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_skin_rarity` method
    """

    def add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self._add_child(skin_rarity)

    def reserve_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self._reserve_child(skin_rarity)

    def get_or_create_skin_rarity(self, skin_rarity_id: str) -> "SkinRarity":
        return self._get_or_create_child(skin_rarity_id)


__all__ = ["Battlesuit"]
