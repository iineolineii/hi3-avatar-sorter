import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Literal

from typing_extensions import Self

from .container import NonUniqueIdContainer
from .valkyrie import Valkyrie
from ..errors import (
    UnknownPartIdError,
    UnknownPartIdFormatError,
    UnknownValkyrieIdError,
)

if sys.version_info <= (3, 15):
    from frozendict import frozendict


PartIDFormat = Literal["short", "long", "skin_long", "fragment"]

@dataclass(kw_only=True)
class Part(NonUniqueIdContainer[Valkyrie]):
    id_length = 3
    id_format: "PartIDFormat"

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
    def by_format_and_no(cls, id_format: "PartIDFormat", no: int) -> Self:
        try:
            return PART_MAP[id_format][no] # pyright: ignore[reportReturnType]
        except KeyError:
            raise UnknownPartIdFormatError(id_format, no)

    @classmethod
    def by_id(cls, id: str) -> Self:
        try:
            return PARTS_BY_ID[id] # pyright: ignore[reportReturnType]
        except KeyError:
            raise UnknownPartIdError(id)


    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    valkyries: "frozendict[str, list[Valkyrie]]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_valkyrie` method
    """


PART_IDS: dict["PartIDFormat", list[str]] = {
    "short":     ["000", "002"],
    "long":      ["006", "302"],
    "skin_long": [   "", "062"],
    "fragment":  ["001", "202"]
}

PART_MAP: dict["PartIDFormat", dict[int, Part]] = defaultdict(dict)
PARTS_BY_ID: dict[str, "Part"] = {}


def build_part_map():
    for id_format, ids in PART_IDS.items():
        for idx, id in enumerate(ids):
            if id:
                PART_MAP[id_format][idx+1] = Part(id=id, no=idx+1, id_format=id_format)
                PARTS_BY_ID[id] = PART_MAP[id_format][idx+1]

__all__ = ["Part", "build_part_map"]
