from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Battlesuit, Part, Valkyrie, Skin, SkinRarity
    from ..utils.raw_avatar import RawAvatar


@dataclass(frozen=True)
class Avatar:
    """
    High-level avatar domain model.

    Represents a fully assembled avatar with normalized components.
    Wraps a :class:`RawAvatar` instance into domain objects.
    """
    no:          "int"
    id:          "str"
    raw:         "RawAvatar"
    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:        "str        | None" = None

    def __iter__(self) -> Iterator[str]:
        result = [f"{self.part.no:02}", f"{self.valkyrie.no:02}", f"{self.battlesuit.no:02}"]

        if self.skin_rarity is not None and self.skin is not None:
            result += [f"{self.skin_rarity.id:02}", f"{self.skin.no:02}"]

        if self.note:
            result += [f"{self.note}"]

        return iter(result)

    def __int__(self) -> int:
        from . import Skin, SkinRarity

        result = f"{self.part.no:02}{self.valkyrie.no:02}{self.battlesuit.no:02}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f"{self.skin_rarity.id:02}{self.skin.no:02}"
        else:
            result += "0" * SkinRarity.id_length
            result += "0" * Skin.id_length

        return int(result)

    def __repr__(self) -> str:
        result = f"{self.part.no:02}{self.valkyrie.no:02}{self.battlesuit.no:02}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f"_{self.skin_rarity.id:02}_{self.skin.no:02}"

        if self.note:
            result += f"_{self.note}"

        return result.lstrip("0")

    def __str__(self) -> str:
        result = f"{self.valkyrie.name} №{self.battlesuit.no}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f", Skin {self.skin_rarity.no}★ №{self.skin.no}"

        if self.note == "B":
            result += f", Veliona"

        elif self.note:
            result += f", {self.note}"

        return result
