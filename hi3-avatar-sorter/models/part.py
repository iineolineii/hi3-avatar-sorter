from dataclasses import dataclass, field
from typing import Self

from frozendict import frozendict

from .container import NonUniqueIdContainer
from .valkyrie import Valkyrie
from ..errors import UnknownPartIdError, UnknownValkyrieIdError
from ..utils import HashableIterable


@dataclass(kw_only=True)
class Part(NonUniqueIdContainer[Valkyrie]):
    ids: "HashableIterable[str]"

    id: str = field(init=False)
    id_length = 3

    def add_valkyrie(self, valkyrie: "Valkyrie") -> "Valkyrie":
        return self._add_child(valkyrie)

    def reserve_valkyrie(self, valkyrie: "Valkyrie") -> "Valkyrie":
        return self._reserve_child(valkyrie)

    def get_valkyrie(self, valkyrie_id: str, battlesuit_id: str) -> "Valkyrie":
        valkyrie = self._get_child(valkyrie_id, battlesuit_id)

        if valkyrie is None:
            raise UnknownValkyrieIdError(valkyrie_id, battlesuit_id)

        return valkyrie

    @classmethod
    def by_id(cls, id: str) -> Self:
        for part in ALL_PARTS:
            if id in part.ids:
                return part # pyright: ignore[reportReturnType]

        raise UnknownPartIdError(id)

    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    valkyries: "frozendict[str, list[Valkyrie]]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_valkyrie` method
    """


PART1 = Part(no=1, ids=("000", "006"))
PART2 = Part(no=2, ids=("002", "062", "202", "302"))
ALL_PARTS = PART2, PART1

__all__ = ["PART1", "PART2", "ALL_PARTS"]
