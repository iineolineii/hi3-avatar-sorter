import sys
from dataclasses import dataclass, field

from .base import NonUniqueIdModel
from .battlesuit import Battlesuit
from .container import Container

if sys.version_info <= (3, 15):
    from frozendict import frozendict


@dataclass(kw_only=True)
class Valkyrie(NonUniqueIdModel, Container[Battlesuit]):
    name: str

    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    battlesuits: "frozendict[str, Battlesuit]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_battlesuit` method
    """

    def add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self._add_child(battlesuit)

    def reserve_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self._reserve_child(battlesuit)

    def get_or_create_battlesuit(self, battlesuit_id: str) -> "Battlesuit":
        return self._get_or_create_child(battlesuit_id)

    def __str__(self) -> str:
        return self.name
