import re
from collections.abc import Hashable, Iterable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Protocol

from frozendict import frozendict

if TYPE_CHECKING:
    from ..relationships import OneToMany
    from .valkyrie import Valkyrie


class HashableIterable[T](Hashable, Iterable[T], Protocol):
    pass


@dataclass(kw_only=True)
class Part(OneToMany["Valkyrie"]):
    ids_short: HashableIterable[str]
    ids_long:  HashableIterable[str]
    no: int

    pattern_short: re.Pattern = field(init=False)
    pattern_long: re.Pattern = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "pattern_short", re.compile(
            f"(?P<part_id>{'|'.join(sorted(
                self.ids_short,
                key=len,
                reverse=True
            ))})"
            r"(?P<valkyrie_id>\d{2})"
            r"(?P<battlesuit_id>\d{2})"
        ))
        object.__setattr__(self, "pattern_long", re.compile(
            f"(?P<part_id>{'|'.join(sorted(
                self.ids_long,
                key=len,
                reverse=True
            ))})"
            r"(?P<valkyrie_id>\d{2})"
            r"(?P<battlesuit_id>\d{2})"
        ))


    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    valkyries: frozendict[int, "Valkyrie"] = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_valkyrie` method
    """

    @classmethod
    def by_id(cls, id: str, format: Literal["short", "long"] = "long") -> "Part | None":
        from .. import ALL_PARTS

        for part in ALL_PARTS:
            if format == "short":
                ids = part.ids_short
            elif format == "long":
                ids = part.ids_long
            else:
                raise InvalidFormatError(format)

            if id in ids:
                return part

    def add_valkyrie(self, valkyrie: "Valkyrie") -> "Valkyrie":
        return self._add_child(valkyrie)
