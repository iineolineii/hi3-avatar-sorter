import sys
from dataclasses import dataclass, field
from typing import ClassVar

from typing_extensions import Self, deprecated

from .container import NonUniqueIdContainer
from .valkyrie import Valkyrie
from ..errors import UnknownPartIdError, UnknownValkyrieIdError
from ..utils import HashableIterable

if sys.version_info <= (3, 15):
    from frozendict import frozendict


@dataclass(kw_only=True)
class Part(NonUniqueIdContainer[Valkyrie]):
    ids: "HashableIterable[str]"

    id: ClassVar[None] = field(init=False) # pyright: ignore[reportRedeclaration]
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

    @property
    @deprecated("Part does not have a single id. Use ids field instead")
    def id(self) -> None: # pyright: ignore[reportIncompatibleVariableOverride]
        raise AttributeError("Part does not have a single id. Use ids field instead")


    def __post_init__(self):
        for id in self.ids:
            self._validate_id(id)

        self._rename_children_attr()

    def __hash__(self) -> int:
        return hash((self.ids, self.no))


def build_valkyrie_db(
    part1_valkyries: list[tuple[str, str, int] | tuple[str, str]],
    part2_valkyries: list[tuple[str, str, int] | tuple[str, str]]
):
    # Store range start for each ID
    range_starts: dict[tuple[str, "Part"], int] = {}

    # Merge raw data preserving the order
    valkyries = [(part1_valkyries, PART1), (part2_valkyries, PART2)]

    for raw_valkyries, part in valkyries:
        for raw in raw_valkyries:
            id:   str = raw[0]
            name: str = raw[1]

            # Current start is the previous end
            # Or 0 if current valkyrie is the first one with current ID
            start = range_starts.get((id, part), 0)

            if len(raw) > 2:
                end = raw[2]

                valkyrie = Valkyrie(
                    id=id,
                    name=name,
                    children_id_range=range(start, end)
                )
            else:
                valkyrie = Valkyrie(
                    id=id,
                    name=name
                )
                end = valkyrie.children_id_range.stop

            part.add_valkyrie(valkyrie)

            # Current end is the next start
            range_starts[(id, part)] = end


PART1 = Part(no=1, ids=("000", "006"))
PART2 = Part(no=2, ids=("002", "062", "202", "302"))
ALL_PARTS = PART2, PART1

__all__ = ["Part", "PART1", "PART2", "ALL_PARTS", "build_valkyrie_db"]
