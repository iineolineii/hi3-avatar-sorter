from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from functools import lru_cache
from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, Self

from ...enums import PartIDFormat
from ...errors import UnknownPartIDError

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
    raw:         "RawAvatar"
    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:        "str        | None" = None

    parts: ClassVar[MappingProxyType[str, Part]]
    id_length: ClassVar[int] = Part.id_length + Valkyrie.id_length + Battlesuit.id_length

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
    # NOTE#2: Using cache is beneficial only when
    # the result is computed using loops
    # and the children container is immutable.
    # Otherwise it may produce stale or misleading results.
    def get_part_by_no(cls, part_no: "int", part_id_format: "PartIDFormat") -> list[Part]:
        """
        Retrieve all `Part`s with the given number and ID format.

        Args:
            part_no (`int`):
                Part number.

            part_id_format (`"PartIDFormat"`):
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
    def build_parts_map(cls, raw_parts: dict[str, tuple["PartIDFormat", "int"]]) -> MappingProxyType[str, "Part"]:
        """
        Build a read-only mapping of Part IDs to their :class:`Part` instances.

        :param raw_parts: Source mapping from Part ID to a tuple containing Part ID format and Part number.
        :type raw_parts: dict[str, tuple[:class:`PartIDFormat`, int]]

        :return: Read-only mapping of Part IDs to their :class:`Part` instances.
        :rtype: MappingProxyType[str, :class:`Part`]
        """
        cls.parts = MappingProxyType({
            id: Part(id=id, no=no, id_format=id_format)
            for id, (id_format, no) in raw_parts.items()
        })

        return cls.parts


    @classmethod
    def from_raw(cls, raw: "RawAvatar", index: int | None = None) -> "Self":
        """
        Construct an `Avatar` from a `RawAvatar` instance.

        Args:
            raw (`RawAvatar`):
                Raw avatar data.

        Returns:
            `Self`: Fully assembled avatar model.
        """
        no = int(raw)
        id = raw.id

        part       = cls.get_part(raw.part)
        valkyrie   = cls.part.add_child(Valkyrie(raw.valkyrie_id))
        battlesuit = valkyrie.add_child(Battlesuit(raw.battlesuit_id), exists_ok=True)

        if raw.skin_rarity_id is not None and raw.skin_id is not None:
            skin_rarity = battlesuit.add_child(SkinRarity(raw.skin_rarity_id), exists_ok=True)
            skin        = skin_rarity.add_child(Skin(raw.skin_id), exists_ok=True)
        else:
            skin_rarity = skin = None

        note = raw.note

        return cls(
            no, id, raw,
            part, valkyrie, battlesuit,
            skin_rarity, skin, note
        )


    @classmethod
    def from_string(cls, string: str) -> "Self":
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
