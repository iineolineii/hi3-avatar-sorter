import re
from dataclasses import dataclass, field
from typing import Literal, TypedDict

from frozendict import frozendict

from .errors import (
    EmptyNoteError,
    InvalidAvatarCodeError,
    InvalidExtraInfoError,
    InvalidSkinCodeError,
    InvalidSkinRarityCodeError,
    MissingSkinCodeError,
    MissingSkinRarityCodeError,
)
from .relationships import ManyToOne, OneToMany
from .valkyrie_db import ValkyrieDatabase


class AvatarFields(TypedDict):
    part: "Part"
    valkyrie_code: int
    battlesuit_code: int
    skin_rarity_code: int | None
    skin_code: int | None
    note: str | None

class Avatar:
    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:         str        | None  = None

    @classmethod
    def parse(cls, file_name: str) -> "AvatarFields":
        code, *extra_info_parts = file_name.split("_", maxsplit=3)

        part, valkyrie_code, battlesuit_code = cls._parse_avatar_code(code, file_name)
        skin_rarity_code, skin_code, note = cls._parse_extra_info(extra_info_parts, file_name)

        return {
            "part": part, "valkyrie_code": valkyrie_code, "battlesuit_code": battlesuit_code,
            "skin_rarity_code": skin_rarity_code, "skin_code": skin_code, "note": note
        }

    def __init__(
        self,
        part: "Part",
        valkyrie_code: int,
        battlesuit_code: int,
        skin_rarity_code: int | None = None,
        skin_code: int | None = None,
        note: str | None = None,
    ) -> None:
        from . import VALKYRIE_DB

        self.part = part
        self.note = note
        self.valkyrie = VALKYRIE_DB.get(valkyrie_code, part, battlesuit_code)

        # One Valkyrie -> Many Battlesuits
        self.battlesuit = self._get_or_create_battlesuit(battlesuit_code, self.valkyrie)

        if skin_rarity_code is None or skin_code is None:
            return

        # One Battlesuit -> Many Skin Rarities
        self.skin_rarity = self._get_or_create_skin_rarity(skin_rarity_code, self.battlesuit)

        # One Skin Rarity -> Many Skins
        self.skin = self._get_or_create_skin(skin_code, self.skin_rarity)

    @staticmethod
    def _parse_avatar_code(code: str, file_name: str) -> tuple[Part, int, int]:
        from . import ALL_PARTS

        for part in ALL_PARTS:
            if match := part.pattern.match(code.rjust(5, "0")):
                match_dict      = match.groupdict()
                valkyrie_code   = int(match_dict["valkyrie_code"])
                battlesuit_code = int(match_dict["battlesuit_code"])

                return part, valkyrie_code, battlesuit_code

        raise InvalidAvatarCodeError(code, file_name)

    @classmethod
    def _parse_extra_info(
        cls,
        info_parts: list[str],
        file_name: str
    ) -> tuple[int, int, str | None] | tuple[None, None, str | None]:
        if not info_parts:
            return None, None, None

        skin_rarity_code: str | None = None
        skin_code:        str | None = None
        note:             str | None = None

        match info_parts:
            case []:
                return None, None, None

            case [note_or_skin_rarity_code]:
                if note_or_skin_rarity_code.isnumeric():
                    skin_rarity_code = cls._validate_skin_rarity_code(note_or_skin_rarity_code, file_name)
                else:
                    note = cls._validate_note(note_or_skin_rarity_code, file_name)

            case [skin_rarity_code, skin_code]:
                skin_rarity_code = cls._validate_skin_rarity_code(skin_rarity_code, file_name)
                skin_code = cls._validate_skin_code(skin_code, file_name)

            case [skin_rarity_code, skin_code, note]:
                skin_rarity_code = cls._validate_skin_rarity_code(skin_rarity_code, file_name)
                skin_code = cls._validate_skin_code(skin_code, file_name)
                note = cls._validate_note(note, file_name)

            case _:
                raise InvalidExtraInfoError(info_parts, file_name)

        if skin_rarity_code is None:
            if skin_code is None:
                return None, None, note

            raise MissingSkinRarityCodeError(skin_code, file_name)

        if skin_code is None:
            raise MissingSkinCodeError(skin_rarity_code, file_name)

        return int(skin_rarity_code), int(skin_code), note

    @staticmethod
    def _validate_skin_rarity_code(skin_rarity_code: str, file_name: str) -> str:
        from . import VALID_SKIN_RARITY_CODES

        if skin_rarity_code.isnumeric() and int(skin_rarity_code) in VALID_SKIN_RARITY_CODES:
            return skin_rarity_code

        raise InvalidSkinRarityCodeError(skin_rarity_code, file_name)

    @staticmethod
    def _validate_skin_code(skin_code: str, file_name: str) -> str:
        if skin_code.isnumeric():
            return skin_code

        raise InvalidSkinCodeError(skin_code, file_name)

    @staticmethod
    def _validate_note(note: str, file_name: str) -> str:
        if note.lower() == "b":
            return "Veliona"

        if note:
            return note

        raise EmptyNoteError(note, file_name)

    def __iter__(self):
        return iter(
            (self.part.no, self.valkyrie.code, self.battlesuit.code)
            + (
                (self.skin_rarity.code, self.skin.code, self.note)
                if (self.skin_rarity is not None and self.skin is not None)
                else (self.note,)
            )
        )

@dataclass
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

    @classmethod
    def by_code(cls, code: str, format: Literal["short", "long"] = "long") -> "Part | None":
        from . import ALL_PARTS

        for part in ALL_PARTS:
            if format == "short":
                codes = part.codes_short
            elif format == "long":
                codes = part.codes_long
            else:
                raise InvalidFormatError(format)

            if code in codes:
                return part


@dataclass
class Valkyrie(OneToMany["Battlesuit"], ManyToOne["Part"]):
    name: str
    part: "Part"
    battlesuit_code_range: range

    # We don't use default_factory here because this field
    # will be replaced by __children in Container.__post_init__
    battlesuits: frozendict[int, "Battlesuit"] = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_battlesuit` method
    """

    @classmethod
    def by_code(
        cls,
        code: int,
        battlesuit_code: int,
        part: "Part",
        valkyrie_db: "ValkyrieDatabase" = ... # pyright: ignore[reportArgumentType]
    ):
        if valkyrie_db is ...:
            from . import VALKYRIE_DB as valkyrie_db

        valkyrie_db.get(code, battlesuit_code, part)

    def add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self._add_child(battlesuit)


@dataclass
class Battlesuit(OneToMany["SkinRarity"], ManyToOne["Valkyrie"]):
    code: int

    no: int = field(init=False)

    # We don't use default_factory here because this field
    # will be replaced by __children in Container.__post_init__
    skins_rarities: 'frozendict[int, "SkinRarity"]' = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_skin_rarity` method
    """

    @classmethod
    def by_code(
        cls,
        code: int,
        valkyrie: Valkyrie
    ):
        if code in valkyrie.battlesuits:
            return valkyrie.battlesuits[code]

        return cls(code)

    def add_skin_rarity(self, skin_rarity: "SkinRarity") -> "SkinRarity":
        return self._add_child(skin_rarity)

@dataclass
class SkinRarity(OneToMany["Skin"], ManyToOne["Battlesuit"]):
    code: int

    no: int = field(init=False)

    # We don't use default_factory here because this field
    # will be replaced by __children in Container.__post_init__
    skins: frozendict[int, "Skin"] = frozendict()
    """
    This field should not be updated from outside.
    Instead, use the `add_skin` method
    """

    @classmethod
    def by_code(
        cls,
        code: int,
        battlesuit: Battlesuit
    ):
        if code in battlesuit.skins_rarities:
            return battlesuit.skins_rarities[code]

        return cls(code)

    def add_skin(self, skin: "Skin") -> "Skin":
        return self._add_child(skin)

@dataclass
class Skin(ManyToOne["SkinRarity"]):
    code: int

    no: int = field(init=False)

    @classmethod
    def by_code(
        cls,
        code: int,
        skin_rarity: SkinRarity
    ):
        if code in skin_rarity.skins:
            return skin_rarity.skins[code]

        return cls(code)
