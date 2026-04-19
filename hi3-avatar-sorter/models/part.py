import sys
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, ClassVar

from .base import BaseModel
from .battlesuit import Battlesuit
from .valkyrie import Valkyrie
from ..enums import PartIDFormats
from ..errors import UnknownValkyrieIDError

if sys.version_info < (3, 15):
    from frozendict import frozendict


@dataclass(frozen=True, slots=True)
class Part(BaseModel):
    no: int = field(init=True)
    id_format: "PartIDFormats"

    valkyries: frozendict[str, tuple[Valkyrie, ...]] = field(init=False)
    id_length: ClassVar[int] = 3


    @lru_cache # Add caching according to NOTE#4
    def get_valkyrie(self, valkyrie_id: str, battlesuit_id: str) -> Valkyrie:
        numeric_battlesuit_id = int(Battlesuit.validate_id(battlesuit_id))

        try:
            valkyries = self.valkyries[valkyrie_id]
        except KeyError as e:
            raise UnknownValkyrieIDError(valkyrie_id, battlesuit_id) from e

        for valkyrie in valkyries:
            if numeric_battlesuit_id in valkyrie.battlesuit_id_range:
                return valkyrie

        raise UnknownValkyrieIDError(valkyrie_id, battlesuit_id)


    def build_valkyrie_map(self, raw_valkyries: Iterable[tuple[str, str, int] | tuple[str, str]]) -> None:
        range_starts: dict[str, int] = {}
        valkyrie_map: dict[str, tuple[Valkyrie, ...]] = defaultdict(tuple)

        for no, (id, name, *rest) in enumerate(raw_valkyries, start=1):
            # Use default range if end is not provided
            if not rest:
                valkyrie = Valkyrie(id=id, no=no, name=name)

            else:
                # Get the last end for this id, or start from 0
                range_start = range_starts.get(id, 0)

                # Use explicitly provided end
                range_end = rest[0]

                battlesuit_id_range = range(range_start, range_end)

                valkyrie = Valkyrie(
                    id=id,
                    no=no,
                    name=name,
                    battlesuit_id_range=battlesuit_id_range
                )

            # Extend the valkyrie array for this id
            valkyrie_map[id] += (valkyrie,)

            # Current end is the next start
            range_starts[id] = valkyrie.battlesuit_id_range.stop

        # Freeze and assign the valkyrie container
        object.__setattr__(self, "valkyries", frozendict(valkyrie_map))


    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)

        except AttributeError:
            class_name = type(self).__name__
            base_message = f"{class_name!r} object has no attribute '{name}'."

            if name == "no":
                raise AttributeError(
                    base_message +
                    f"Perhaps it was created without using the "
                    f"'build_part_map' factory method?"
                )

            if name == "valkyries":
                raise AttributeError(
                    base_message +
                    f"Perhaps you forgot to call "
                    f"'build_valkyrie_map' method?"
                )

            raise


__all__ = ["Part"]
