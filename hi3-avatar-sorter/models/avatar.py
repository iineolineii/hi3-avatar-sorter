from collections.abc import Iterator
from dataclasses import dataclass
from typing import ClassVar, TypedDict

from typing_extensions import Self

from .base import BaseModel
from .battlesuit import Battlesuit
from .part import Part
from .skin import Skin
from .skin_rarity import SkinRarity
from .valkyrie import Valkyrie
from ..errors import EmptyInputStringError, EmptyNoteError, MissingAvatarIdError


class RawAvatar(TypedDict):
    part_id:        int | str
    valkyrie_id:    int | str
    battlesuit_id:  int | str
    skin_rarity_id: int | str | None
    skin_id:        int | str | None
    note:           int | str | None


@dataclass(kw_only=True)
class Avatar(BaseModel):
    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:        "str        | None" = None

    id_length: ClassVar[int] = Part.id_length + Valkyrie.id_length + Battlesuit.id_length

    def reserve(self):
        # self.reserve_part(self.part)
        # self.part.reserve_valkyrie(self.valkyrie)
        self.valkyrie.reserve_battlesuit(self.battlesuit)

        if self.skin_rarity is not None and self.skin is not None:
            self.battlesuit.reserve_skin_rarity(self.skin_rarity)
            self.skin_rarity.reserve_skin(self.skin)

    def register(self):
        # self.add_part(self.part)
        # self.part.add_valkyrie(self.valkyrie)
        self.valkyrie.add_battlesuit(self.battlesuit)

        if self.skin_rarity is not None and self.skin is not None:
            self.battlesuit.add_skin_rarity(self.skin_rarity)
            self.skin_rarity.add_skin(self.skin)


    @classmethod
    def from_string(cls, string: str) -> Self:
        raw_avatar = cls._raw_from_string(string)
        self = cls.from_raw(**raw_avatar)
        self.register()

        return self

    @classmethod
    def from_raw(
        cls,
        part_id:        int | str,
        valkyrie_id:    int | str,
        battlesuit_id:  int | str,
        skin_rarity_id: int | str | None = None,
        skin_id:        int | str | None = None,
        note:           int | str | None = None
    ):
        part_id = str(part_id)
        valkyrie_id = str(valkyrie_id)
        battlesuit_id = str(battlesuit_id)

        avatar_id = part_id + valkyrie_id + battlesuit_id

        if skin_rarity_id is not None:
            skin_rarity_id = str(skin_rarity_id)

        if skin_id is not None:
            skin_id = str(skin_id)

        if note is not None:
            note = str(note)

        part = Part.by_id(part_id)
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

        return self

    from_dict = from_raw

    @classmethod
    def format_note(
        cls,
        note: str | None
    ) -> str:
        if not note:
            raise EmptyNoteError(note)

        if note.lower() == "b":
            note = "Veliona"

        return note.capitalize()


    @classmethod
    def _raw_from_string(cls, string: str) -> RawAvatar:
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

        avatar_id = cls._validate_id(avatar_id)

        # part_id, valkyrie_id, and battlesuit_id appear next to each other in avatar_id
        pos = 0

        part_id = avatar_id[pos:pos + Part.id_length]
        pos += Part.id_length

        valkyrie_id = avatar_id[pos:pos + Valkyrie.id_length]
        pos += Valkyrie.id_length

        battlesuit_id = avatar_id[pos:pos + Battlesuit.id_length]

        return {
            "part_id":        part_id,
            "valkyrie_id":    valkyrie_id,
            "battlesuit_id":  battlesuit_id,
            "skin_rarity_id": skin_rarity_id,
            "skin_id":        skin_id,
            "note":           note
        }


    def __iter__(self) -> Iterator[int | str]:
        result = (self.part.no, self.valkyrie.id, self.battlesuit.id)

        if self.skin_rarity is not None and self.skin is not None:
            result += (self.skin_rarity.id, self.skin.id)

        if self.note:
            result += (self.note,)

        return iter(result)

    def __int__(self) -> int:
        # Example: 010203_04_05_Special
        result = f"{int(self.part):02}{int(self.valkyrie):02}{self.battlesuit:02}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f", {self.skin_rarity} {self.skin}"

        if self.note:
            result += f", {self.note}"

        return int(result)

    def __str__(self) -> str:
        # Example: Raiden Mei №3, Skin 4★ №5, Special
        result = f"{self.valkyrie} {self.battlesuit}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f", Skin {self.skin_rarity} {self.skin}"

        if self.note:
            result += f", {self.note}"

        return result


    @property
    def raw(self):
        try:
            return self.__raw

        except AttributeError:
            self.__raw = self._raw_from_string(self.id)

            if self.skin_rarity is not None:
                self.__raw["skin_rarity_id"] = self.skin_rarity.id

            if self.skin is not None:
                self.__raw["skin_id"] = self.skin.id

            if self.note is not None:
                self.__raw["note"] = self.note

            return self.__raw

    to_dict = raw


__all__ = ["RawAvatar", "Avatar"]
