import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, ClassVar, Self

from .meta import AvatarMeta
from .raw import RawAvatar
from ..base import BaseModel
from ..battlesuit import Battlesuit
from ..part import Part
from ..skin import Skin
from ..skin_rarity import SkinRarity
from ..valkyrie import Valkyrie
from ... import PartIDFormats, PartNumbers
from ...errors import EmptyNoteError, UnknownPartIDError, UnknownPartNoError

if sys.version_info < (3, 15):
    from frozendict import frozendict


@dataclass(frozen=True, slots=True)
class Avatar(BaseModel, metaclass=AvatarMeta):
    """
    High-level avatar model.

    Represents a fully assembled avatar with normalized components.
    Wraps a `RawAvatar` instance into domain objects (`Part`, `Valkyrie`,
    `Battlesuit`, `SkinRarity`, `Skin`) and optionally formats the note.
    """
    part:        Part
    valkyrie:    Valkyrie
    battlesuit:  Battlesuit
    skin_rarity: SkinRarity | None = None
    skin:        Skin       | None = None
    note:        str        | None = None

    parts: ClassVar[frozendict[str, Part]]
    id_length: ClassVar[int] = Part.id_length + Valkyrie.id_length + Battlesuit.id_length

    raw: RawAvatar = field(init=False, repr=False)
    """
    Original `RawAvatar` DTO used to construct this model.

    Note:
        This attribute is not present if the instance was not
        created via any of the `from_<something>` factory methods.
    """

    @classmethod
    def get_part(cls, part_id: str) -> Part:
        """
        Retrieve a `Part` by its ID.

        Args:
            part_id (`str`):
                Part ID.

        Raises:
            `UnknownPartIDError`:
                If the Part ID does not exist.

        Returns:
            `Part`: The corresponding Part.
        """
        try:
            return cls.parts[part_id]
        except KeyError as e:
            raise UnknownPartIDError(part_id) from e

    @classmethod
    @lru_cache
    # NOTE#4: Using cache is beneficial only when
    # the result is computed using loops
    # and the children container is immutable.
    # Otherwise it may produce stale or misleading results.
    def get_part_by_no(cls, part_no: int, part_id_format: PartIDFormats) -> list[Part]:
        """
        Retrieve all `Part`s with the given number and ID format.

        Args:
            part_no (`int`):
                Part number.

            part_id_format (`PartIDFormat`):
                Format of the Part ID.

        Raises:
            `UnknownPartNoError`:
                If no Part matches the given number and format.

        Returns:
            `list[Part]`: The found `Part`s.
        """
        found = [
            part
            for part in cls.parts.values()
            if part.no == part_no and part.id_format == part_id_format
        ]

        if not found:
            raise UnknownPartNoError(part_no, part_id_format)

        return found


    @classmethod
    def build_part_map(cls, raw_parts: dict[str, tuple["PartIDFormats", "PartNumbers"]]) -> None:
        """
        Initialize the class-level Part map from raw Part data.

        Args:
            raw_parts (`dict[str, tuple[PartIDFormat, PartNumbers]]`):
                Mapping from Part ID to a tuple of (Part ID format, Part number).
        """
        cls.parts = frozendict({
            id: Part(id=id, no=no, id_format=id_format)
            for id, (id_format, no) in raw_parts.items()
        })


    @classmethod
    def from_raw(cls, raw: RawAvatar) -> Self:
        """
        Construct an `Avatar` from a `RawAvatar` instance.

        Args:
            raw (`RawAvatar`):
                Raw avatar data.

        Returns:
            `Self`: Fully assembled avatar model.
        """
        part = cls.get_part(raw.part_id)
        valkyrie = part.get_valkyrie(raw.valkyrie_id, raw.battlesuit_id)
        battlesuit = valkyrie.get_or_add_battlesuit(Battlesuit(id=raw.battlesuit_id))

        if raw.skin_rarity_id is not None and raw.skin_id is not None:
            skin_rarity = battlesuit.get_or_add_skin_rarity(SkinRarity(id=raw.skin_rarity_id))
            skin = skin_rarity.get_or_add_skin(Skin(id=raw.skin_id))
        else:
            skin_rarity = skin = None

        note = cls.validate_note(raw.note) if raw.note is not None else None

        self = cls(
            id=raw.id,
            part=part,
            valkyrie=valkyrie,
            battlesuit=battlesuit,
            skin_rarity=skin_rarity,
            skin=skin,
            note=note
        )
        object.__setattr__(self, "raw", raw)
        return self


    @classmethod
    def from_string(cls, string: str) -> Self:
        """
        Construct an `Avatar` from a string representation.

        Args:
            string (`str`):
                Raw string input.

        Returns:
            `Self`: Parsed avatar model.
        """
        return cls.from_raw(RawAvatar.from_string(string))

    @classmethod
    def from_iterable(cls, iterable: Iterable[str]) -> Self:
        """
        Construct an `Avatar` from an iterable of string components.

        Args:
            iterable (`Iterable[str]`):
                Iterable containing Part ID, Valkyrie ID, Battlesuit ID,
                and optionally Skin rarity ID, Skin ID with Note

        Returns:
            `Self`: Parsed avatar model.
        """
        return cls.from_raw(RawAvatar.from_iterable(iterable))


    @classmethod
    def validate_note(cls, note: str | None) -> str:
        """
        Normalize and validate given note string.

        Args:
            note (`str | None`):
                Raw note.

        Raises:
            `EmptyNoteError`:
                If the note is empty or `None`.

        Returns:
            `str`: Formatted note.
        """
        if not note:
            raise EmptyNoteError(note)

        if note.lower() == "b":
            note = "Veliona"

        return note.capitalize()


    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)

        except AttributeError:
            class_name = type(self).__name__
            base_message = f"{class_name!r} object has no attribute {name!r}."

            if name == "raw":
                raise AttributeError(
                    base_message +
                    f" Perhaps it was not created via any of the "
                    f"'{class_name}.from_<something>' factory methods?"
                )

            raise


    def __iter__(self) -> Iterator[str]:
        # Example: ["01", "02", "03", "04", "05", "Special"]
        result = [f"{self.part.no:02}", f"{self.valkyrie.no:02}", f"{self.battlesuit.no:02}"]

        if self.skin_rarity is not None and self.skin is not None:
            result += [f"{self.skin_rarity.no:02}", f"{self.skin.no:02}"]

        if self.note:
            result += [f"{self.note}"]

        return iter(result)

    def __int__(self) -> int:
        # Example: 0102030405 or 0102030000
        result = f"{self.part.no:02}{self.valkyrie.no:02}{self.battlesuit.no:02}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f"{self.skin_rarity.no:02}{self.skin.no:02}"
        else:
            result += "0000"

        return int(result)

    def __repr__(self) -> str:
        # Example: 010203_04_05_Special
        result = f"{self.part.no:02}{self.valkyrie.no:02}{self.battlesuit.no:02}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f"_{self.skin_rarity.no:02}_{self.skin.no:02}"

        if self.note:
            result += f"_{self.note}"

        return result

    def __str__(self) -> str:
        # Example: Raiden Mei №3, Skin 4★ №5, Special
        result = f"{self.valkyrie} {self.battlesuit}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f", Skin {self.skin_rarity} {self.skin}"

        if self.note:
            result += f", {self.note}"

        return result


__all__ = ["Avatar"]
