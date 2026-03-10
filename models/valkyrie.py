from dataclasses import dataclass
from typing import TYPE_CHECKING

from frozendict import frozendict

from ..relationships import ManyToOne, OneToMany
from ..valkyrie_db import ValkyrieDatabase

if TYPE_CHECKING:
    from .battlesuit import Battlesuit
    from .part import Part


@dataclass(kw_only=True)
class Valkyrie(OneToMany["Battlesuit"], ManyToOne["Part"]):
    name: str
    part: "Part"
    battlesuit_code_range: range

    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    battlesuits: frozendict[int, "Battlesuit"] = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_battlesuit` method
    """

    @classmethod
    def by_code( # pyright: ignore[reportIncompatibleMethodOverride]
        cls,
        code: int,
        battlesuit_code: int,
        part: "Part",
        valkyrie_db: "ValkyrieDatabase" = None # pyright: ignore[reportArgumentType]
    ):
        if valkyrie_db is None:
            from .. import VALKYRIE_DB as valkyrie_db

        valkyrie_db.get(code, battlesuit_code, part)

    def add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self._add_child(battlesuit)
