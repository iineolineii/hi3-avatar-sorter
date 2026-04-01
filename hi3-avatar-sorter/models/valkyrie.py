import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .base import NonUniqueIdModel
from .battlesuit import Battlesuit
from .containers import Container

if sys.version_info <= (3, 15):
    from frozendict import frozendict

if TYPE_CHECKING:
    from .part import Part


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

    def get_or_add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self._get_or_add_child(battlesuit)

    def __str__(self) -> str:
        return self.name


def build_valkyrie_map(
    part1_valkyries: tuple[list[tuple[str, str, int] | tuple[str, str]], Part],
    part2_valkyries: tuple[list[tuple[str, str, int] | tuple[str, str]], Part]
):
    # Store range start for each ID
    range_starts: dict[tuple[str, "Part"], int] = {}

    # Merge raw data preserving the order
    valkyries = [part1_valkyries, part2_valkyries]

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


__all__ = ["Valkyrie", "build_valkyrie_map"]
