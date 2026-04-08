from abc import ABCMeta
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from functools import lru_cache
from typing import ClassVar, Literal, TypedDict, overload

from typing_extensions import Self

from .. import PartIDFormat
from ..containers import FrozenContainer
from ..errors import (
    AmbiguousPartNoError,
    EmptyInputStringError,
    EmptyNoteError,
    MissingAvatarIdError,
    MissingSkinIdError,
    MissingSkinRarityIdError,
    UnknownPartIdError,
    UnknownPartNoError
)
from .base import BaseModel
from .battlesuit import Battlesuit
from .part import Part
from .skin import Skin
from .skin_rarity import SkinRarity
from .valkyrie import Valkyrie


class RawAvatar(TypedDict):
    avatar_id:      str
    part_id:        str
    valkyrie_id:    str
    battlesuit_id:  str
    skin_rarity_id: str | None
    skin_id:        str | None
    note:           str | None


class AvatarMeta(ABCMeta):
    @property
    def parts(cls: type[Avatar]) -> FrozenContainer[str, Part]: # pyright: ignore[reportGeneralTypeIssues]
        try:
            return cls.__parts
        except AttributeError:
            raise AttributeError(
                f"type object {cls.__name__!r} has no attribute 'parts'. "
                f"Maybe you forgot to call {cls.build_part_map.__qualname__!r}?"
            )

    @parts.setter
    def self(cls, parts: FrozenContainer[str, Part]) -> None:
        cls.__parts = parts


@dataclass
class Avatar(BaseModel, metaclass=AvatarMeta):
    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:        "str        | None" = None

    id_length: ClassVar[int] = Part.id_length + Valkyrie.id_length + Battlesuit.id_length

    @overload
    @classmethod
    def get_part(cls, part_id: str, /) -> Part: ...

    @overload
    @classmethod
    def get_part(cls, part_no: int, part_id_format: "PartIDFormat", /) -> Part: ...

    @lru_cache
    # NOTE#4: Using cache is beneficial only when
    # the result is computed using loops
    # and the children container is immutable.
    # Otherwise it may produce stale or misleading results.
    @classmethod
    def get_part(cls, part_no_or_id: int | str, part_id_format: "PartIDFormat | None" = None, /) -> Part:
        if part_id_format is None:
            part_id: str = part_no_or_id # pyright: ignore[reportAssignmentType]
            return cls._get_part_by_id(part_id)

        part_no: int = part_no_or_id # pyright: ignore[reportAssignmentType]
        return cls._get_part_by_no(part_no, part_id_format)

    @classmethod
    def _get_part_by_id(cls, part_id: str) -> Part:
        try:
            return cls.parts[part_id]
        except KeyError as e:
            raise UnknownPartIdError(part_id) from e

    @classmethod
    def _get_part_by_no(cls, part_no: int, part_id_format: "PartIDFormat") -> Part:
        found: list[Part] = [
            part
            for part in cls.parts.values()
            if part.no == part_no and part.id_format == part_id_format
        ]

        if len(found) == 1:
            return found[0]

        if not found:
            raise UnknownPartNoError(part_no, part_id_format)

        raise AmbiguousPartNoError(part_no, part_id_format, found)

    @classmethod
    def build_part_map(cls, raw_parts: dict[str, tuple["PartIDFormat", Literal[1, 2]]]) -> None:
        cls.parts = FrozenContainer({
            id: Part(id=id, no=no, id_format=id_format)
            for id, (id_format, no) in raw_parts.items()
        })


    def reserve(self) -> None:
        # self.reserve_part(self.part)
        # self.part.reserve_valkyrie(self.valkyrie)
        self.valkyrie.reserve_battlesuit(self.battlesuit)

        if self.skin_rarity is not None and self.skin is not None:
            self.battlesuit.reserve_skin_rarity(self.skin_rarity)
            self.skin_rarity.reserve_skin(self.skin)

    @classmethod
    def from_string(cls, string: str, *, reserve: bool = False) -> Self:
        raw_avatar = cls.raw_from_string(string)
        self = cls.from_raw(**raw_avatar)

        if reserve:
            self.reserve()

        return self

    @classmethod
    def from_raw(
        cls,
        avatar_id:      str,
        part_id:        str,
        valkyrie_id:    str,
        battlesuit_id:  str,
        skin_rarity_id: str | None = None,
        skin_id:        str | None = None,
        note:           str | None = None,
        *,
        reserve: bool = False
    ) -> Self:
        if skin_rarity_id is not None:
            skin_rarity_id = skin_rarity_id

        if skin_id is not None:
            skin_id = skin_id

        if note is not None:
            note = note

        part = cls.get_part(part_id)
        valkyrie = part.get_valkyrie(valkyrie_id, battlesuit_id)
        battlesuit = valkyrie.get_or_add_battlesuit(Battlesuit(id=battlesuit_id))

        if skin_rarity_id is not None and skin_id is not None:
            skin_rarity = battlesuit.get_or_add_skin_rarity(SkinRarity(id=skin_rarity_id))
            skin = skin_rarity.get_or_add_skin(Skin(id=skin_id))
        else:
            skin_rarity = skin = None

        if note is not None:
            note = cls.format_note(note)
        # else:
        #     note = None

        self = cls(
            id=avatar_id,
            part=part,
            valkyrie=valkyrie,
            battlesuit=battlesuit,
            skin_rarity=skin_rarity,
            skin=skin,
            note=note
        )

        self.__raw = { # pyright: ignore[reportAttributeAccessIssue]
            "part_id":        part_id,
            "valkyrie_id":    valkyrie_id,
            "battlesuit_id":  battlesuit_id,
            "skin_rarity_id": skin_rarity_id,
            "skin_id":        skin_id,
            "note":           note
        }

        if reserve:
            self.reserve()

        return self

    from_dict = from_raw

    @classmethod
    def format_note(cls, note: str | None) -> str:
        if not note:
            raise EmptyNoteError(note)

        if note.lower() == "b":
            note = "Veliona"

        return note.capitalize()


    @classmethod
    def raw_from_string(cls, string: str, validate: bool = False) -> RawAvatar:
        if not string:
            raise EmptyInputStringError(string)

        name_parts = string.split("_", maxsplit=3)

        skin_rarity_id: str | None = None
        skin_id:        str | None = None
        note:           str | None = None

        match name_parts:
            # Length is 0: Invalid file name (empty string or "_")
            case []:
                raise MissingAvatarIdError(string)

            # Length is 1: Only avatar ID
            case [avatar_id]:
                pass

            # Length is 2: Avatar ID with a note
            case [avatar_id, note]:
                pass

            # Length is 3: Avatar ID with a skin
            case [avatar_id, skin_rarity_id, skin_id]:
                pass

            # Length is 4: Avatar ID with a skin and a note
            case [avatar_id, skin_rarity_id, skin_id, note]:
                pass

            # Length is 5: Unreachable because max length here is 4 (maxsplit+1)
            case _:
                raise AssertionError("This code should be unreachable")

        avatar_id = cls.validate_id(avatar_id)

        # part_id, valkyrie_id, and battlesuit_id appear next to each other in avatar_id
        pos = 0

        part_id = avatar_id[pos:pos + Part.id_length]
        pos += Part.id_length

        valkyrie_id = avatar_id[pos:pos + Valkyrie.id_length]
        pos += Valkyrie.id_length

        battlesuit_id = avatar_id[pos:pos + Battlesuit.id_length]

        avatar_raw: RawAvatar = {
            "avatar_id":      avatar_id,
            "part_id":        part_id,
            "valkyrie_id":    valkyrie_id,
            "battlesuit_id":  battlesuit_id,
            "skin_rarity_id": skin_rarity_id,
            "skin_id":        skin_id,
            "note":           note
        }

        if validate:
            cls.validate_raw(avatar_raw)

        return avatar_raw


    @classmethod
    def int_from_string(cls, string: str) -> int:
        raw_avatar = cls.raw_from_string(string)
        result = raw_avatar["avatar_id"]

        if raw_avatar["skin_rarity_id"] is not None and raw_avatar["skin_id"] is not None:
            result += raw_avatar["skin_rarity_id"]
            result += raw_avatar["skin_id"]
        else:
            result += "0000"

        return int(result)


    @staticmethod
    def validate_raw(raw_avatar: RawAvatar):
        Part.validate_id(raw_avatar["part_id"])
        Valkyrie.validate_id(raw_avatar["valkyrie_id"])
        Battlesuit.validate_id(raw_avatar["battlesuit_id"])

        if raw_avatar["skin_rarity_id"] is not None:
            SkinRarity.validate_id(raw_avatar["skin_rarity_id"])

            if raw_avatar["skin_id"] is not None:
                Skin.validate_id(raw_avatar["skin_id"])
            else:
                raise MissingSkinIdError(raw_avatar)

        elif raw_avatar["skin_id"] is not None:
            raise MissingSkinRarityIdError(raw_avatar)


    def __iter__(self) -> Iterator[str]:
        result = (str(self.part.no), self.valkyrie.id, self.battlesuit.id)

        if self.skin_rarity is not None and self.skin is not None:
            result += (self.skin_rarity.id, self.skin.id)

        if self.note:
            result += (self.note,)

        return iter(result)

    def __int__(self) -> int:
        # Example: 0102030405 or 0102030000
        result = f"{self.part.no:02}{self.valkyrie.no:02}{self.battlesuit.no:02}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f"_{self.skin_rarity.no:02}_{self.skin.no:02}"
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


    @property
    def raw(self) -> RawAvatar:
        try:
            return self.__raw

        except AttributeError:
            self.__raw = self.raw_from_string(self.id)

            if self.skin_rarity is not None:
                self.__raw["skin_rarity_id"] = self.skin_rarity.id

            if self.skin is not None:
                self.__raw["skin_id"] = self.skin.id

            if self.note is not None:
                self.__raw["note"] = self.note

            return self.__raw

    to_dict = raw


__all__ = ["RawAvatar", "Avatar"]
