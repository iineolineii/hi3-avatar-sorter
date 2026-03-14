from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self

from frozendict import frozendict

from ..errors import UnknownPartIdError
from ..relationships import OneToMany

if TYPE_CHECKING:
    from .valkyrie import Valkyrie
    from ..utils import HashableIterable


@dataclass(eq=True, kw_only=True, order=True, unsafe_hash=True)
class Part(OneToMany["Valkyrie"]):
    ids: "HashableIterable[str]" = field(hash=True)
    no: int

    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    valkyries: "frozendict[int, Valkyrie]" = field(default=frozendict(), hash=False)
    """
    This field should not be updated from outside.
    Instead, use the `add_valkyrie` method
    """

    @classmethod
    def by_id(cls, id: str) -> Self:
        cls._validate_id(id)

        for part in ALL_PARTS:
            if id in part.ids:
                return part # pyright: ignore[reportReturnType]

        raise UnknownPartIdError(id)

    @classmethod
    def _validate_id(cls, id: str) -> None:
        pass

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"№{int(self)}"

    def add_valkyrie(self, valkyrie: "Valkyrie") -> "Valkyrie":
        return self._add_child(valkyrie)


PART1 = Part(no=1, ids=("000", "006"))
PART2 = Part(no=2, ids=("002", "062", "202", "302"))
ALL_PARTS = PART2, PART1

__all__ = ["PART1", "PART2", "ALL_PARTS"]
