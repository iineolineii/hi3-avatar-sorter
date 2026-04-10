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

    @valkyries.setter
    def valkyries(self, valkyries: frozendict[str, list[Valkyrie]]) -> None:
        self.__valkyries = valkyries

    @lru_cache # Add caching according to NOTE#4
    def get_valkyrie(self, valkyrie_id: str, battlesuit_id: str) -> Valkyrie:
        with suppress(KeyError):
            for valkyrie in self.valkyries[valkyrie_id]:
                if battlesuit_id in valkyrie.battlesuit_id_range:
                    return valkyrie

        raise UnknownValkyrieIDError(valkyrie_id, battlesuit_id)

    def build_valkyrie_map(self, raw_valkyries: dict[str, tuple[str] | tuple[str, int]]) -> None:
        # Store range start for each ID
        range_starts: dict[str, int] = {}

        valkyrie_map: dict[str, list[Valkyrie]] = defaultdict(list)

        for id, raw in raw_valkyries.items():
            name: str = raw[0]

            # Current start is the previous end
            # Or 0 if current valkyrie is the first one with current ID
            start = range_starts.get(id, 0)

            if len(raw) > 1:
                end = raw[1]

                valkyrie = Valkyrie(
                    id=id,
                    name=name,
                    battlesuit_id_range=range(start, end)
                )
            else:
                valkyrie = Valkyrie(
                    id=id,
                    name=name
                )
                end = valkyrie.battlesuit_id_range.stop

            valkyrie_map[id].append(valkyrie)

            # Current end is the next start
            range_starts[id] = end

        self.valkyries = frozendict(valkyrie_map)

__all__ = ["Valkyrie"]
