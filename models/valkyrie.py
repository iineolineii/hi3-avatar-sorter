from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from frozendict import frozendict

from ..relationships import ManyToOne, OneToMany

if TYPE_CHECKING:
    from ..valkyrie_db import ValkyrieDatabase
    from . import Battlesuit, Part


@dataclass(kw_only=True)
class Valkyrie(OneToMany["Battlesuit"], ManyToOne["Part"]):
    name: str
    part: "Part"
    battlesuit_id_range: range

    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    battlesuits: "frozendict[int, Battlesuit]" = field(default=frozendict(), hash=False, compare=False)
    """
    This field should not be updated from outside.
    Instead, use the `add_battlesuit` method
    """

    @classmethod
    def by_id( # pyright: ignore[reportIncompatibleMethodOverride]
        cls,
        id: int,
        battlesuit_id: int,
        part: "Part",
        valkyrie_db: "ValkyrieDatabase" = None # pyright: ignore[reportArgumentType]
    ):
        if valkyrie_db is None:
            from .. import VALKYRIE_DB as valkyrie_db

        valkyrie_db.get(id, battlesuit_id, part)

    def add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self._add_child(battlesuit)
