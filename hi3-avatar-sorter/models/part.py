from collections.abc import Iterable
import sys
from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass, field
from functools import lru_cache
from typing import ClassVar

from .base import BaseModel
from .valkyrie import Valkyrie
from .. import PartIDFormat
from ..errors import UnknownValkyrieIDError

if sys.version_info < (3, 15):
    from frozendict import frozendict


@dataclass
class Part(BaseModel):
    no: int = field(init=True)
    id_format: "PartIDFormat"

    id_length: ClassVar[int] = 3

    @property
    def valkyries(self) -> frozendict[str, list[Valkyrie]]:
        try:
            return self.__valkyries
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__!r} object has no attribute 'valkyries'. "
                f"Maybe you forgot to call {self.build_valkyrie_map.__qualname__!r}?"
            )

    @lru_cache # Add caching according to NOTE#4
    def get_valkyrie(self, valkyrie_id: str, battlesuit_id: str) -> Valkyrie:
        with suppress(KeyError):
            for valkyrie in self.valkyries[valkyrie_id]:
                if battlesuit_id in valkyrie.battlesuit_id_range:
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


__all__ = ["Valkyrie"]
