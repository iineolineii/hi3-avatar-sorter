import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from functools import lru_cache
from typing import ClassVar, Self, overload

from .meta import AvatarMeta
from .raw import RawAvatar
from ..base import BaseModel
from ..battlesuit import Battlesuit
from ..part import Part
from ..skin import Skin
from ..skin_rarity import SkinRarity
from ..valkyrie import Valkyrie
from ... import PartIDFormat, PartNumbers
from ...errors import (
    DuplicatePartNoError,
    EmptyNoteError,
    UnknownPartIDError,
    UnknownPartNoError
)

if sys.version_info < (3, 15):
    from frozendict import frozendict


@dataclass
class Avatar(BaseModel, metaclass=AvatarMeta):
    """
    High-level avatar model.

    Represents a fully assembled avatar with normalized components.
    Wraps a `RawAvatar` instance into domain objects (`Part`, `Valkyrie`,
    `Battlesuit`, `SkinRarity`, `Skin`) and optionally formats the note.
    """
    part: Part
    valkyrie: Valkyrie
    battlesuit: Battlesuit
    skin_rarity: SkinRarity | None = None
    skin: Skin | None = None
    note: str | None = None

    id_length: ClassVar[int] = Part.id_length + Valkyrie.id_length + Battlesuit.id_length

    @overload
    @classmethod
    def get_part(cls, part_no: int, part_id_format: PartIDFormat, /) -> Part: ...
    """
    Retrieve a `Part` by its number and ID format.

    Args:
        part_no (`int`):
            Part number.

        part_id_format (`PartIDFormat`):
            Format of the Part ID.

    Raises:
        `UnknownPartNoError`:
            If no Part matches the given number and format.

        `AmbiguousPartNoError`:
            If multiple parts match the given number and format.

    Returns:
        `Part`: The corresponding Part.
    """

    @overload
    @classmethod
    def get_part(cls, part_id: str, /) -> Part: ...
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

    @lru_cache
    # NOTE#4: Using cache is beneficial only when
    # the result is computed using loops
    # and the children container is immutable.
    # Otherwise it may produce stale or misleading results.
    @classmethod
    def get_part(
        cls,
        part_no_or_id: int | str,
        part_id_format: PartIDFormat | None = None, /
    ) -> Part:
        if part_id_format is None:
            return cls._get_part_by_id(part_no_or_id) # pyright: ignore[reportArgumentType]

        return cls._get_part_by_no(part_no_or_id, part_id_format) # pyright: ignore[reportArgumentType]

    @classmethod
    def _get_part_by_id(cls, part_id: str) -> Part:
        try:
            return cls.parts[part_id]
        except KeyError as e:
            raise UnknownPartIDError(part_id) from e

    @classmethod
    def _get_part_by_no(cls, part_no: int, part_id_format: PartIDFormat) -> Part:
        try:
            return cls.part_by_no[(part_no, part_id_format)]
        except KeyError as e:
            raise UnknownPartNoError(part_no, part_id_format) from e


    @classmethod
    def build_part_map(cls, raw_parts: dict[str, tuple["PartIDFormat", "PartNumbers"]]) -> None:
        """
        Initialize the class-level Part map from raw Part data.

        Args:
            raw_parts (`dict[str, tuple[PartIDFormat, PartNumbers]]`):
                Mapping from Part ID to a tuple of (Part ID format, Part number).
        """
        part_by_id: dict[str, Part] = {}
        part_by_no: dict[tuple["PartIDFormat", "PartNumbers"], Part] = {}

        for id, (id_format, no) in raw_parts.items():
            part = Part(id=id, no=no, id_format=id_format)
            part_by_id[id] = part

            if (id_format, no) in part_by_no:
                raise DuplicatePartNoError(no, id_format, raw_parts)

            part_by_no[(id_format, no)] = part

        cls.__part_by_id = frozendict(part_by_id)
        cls.__part_by_no = frozendict(part_by_no)


    def reserve(self) -> None:
        """
        Reserve domain objects in related containers.

        Registers this avatar's battlesuit and skin components for internal
        tracking in `Valkyrie` and `Battlesuit` instances.
        """
        self.valkyrie.reserve_battlesuit(self.battlesuit)

        if self.skin_rarity is not None and self.skin is not None:
            self.battlesuit.reserve_skin_rarity(self.skin_rarity)
            self.skin_rarity.reserve_skin(self.skin)


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
        self.__raw = raw # pyright: ignore[reportAttributeAccessIssue]
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


    @property
    def raw(self) -> RawAvatar:
        """
        Original `RawAvatar` DTO used to construct this model.

        Note:
            This attribute is not present if the instance was not
            created via any of the `from_<something>` factory methods.
        """
        try:
            return self.__raw # pyright: ignore[reportAttributeAccessIssue]
        except AttributeError as e:
            classname = type(self).__name__
            raise AttributeError(
                f"{classname!r} object has no attribute 'raw'. "
                f"Maybe it was created without using any of the "
                f"'{classname}.from_<something>' factory methods?"
            )


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
