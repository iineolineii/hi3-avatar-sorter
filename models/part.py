import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

from frozendict import frozendict

if TYPE_CHECKING:
    from ..relationships import OneToMany
    from .valkyrie import Valkyrie


@dataclass(kw_only=True)
class Part(OneToMany["Valkyrie"]):
    codes_short: str | tuple[str, ...]
    codes_long:  str | tuple[str, ...]
    no: int

    pattern_short: re.Pattern = field(init=False)
    pattern_long: re.Pattern = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "pattern_short", re.compile(
            f"(?P<part_code>{'|'.join(sorted(
                self.codes_short,
                key=len,
                reverse=True
            ))})"
            r"(?P<valkyrie_code>\d{2})"
            r"(?P<battlesuit_code>\d{2})"
        ))
        object.__setattr__(self, "pattern_long", re.compile(
            f"(?P<part_code>{'|'.join(sorted(
                self.codes_long,
                key=len,
                reverse=True
            ))})"
            r"(?P<valkyrie_code>\d{2})"
            r"(?P<battlesuit_code>\d{2})"
        ))


    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    valkyries: frozendict[int, "Valkyrie"] = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_valkyrie` method
    """

    @classmethod
    def by_code(cls, code: str, format: Literal["short", "long"] = "long") -> "Part | None":
        from .. import ALL_PARTS

        for part in ALL_PARTS:
            if format == "short":
                codes = part.codes_short
            elif format == "long":
                codes = part.codes_long
            else:
                raise InvalidFormatError(format)

            if code in codes:
                return part

    def add_valkyrie(self, valkyrie: "Valkyrie") -> "Valkyrie":
        return self._add_child(valkyrie)
