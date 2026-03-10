from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Self

from .. import ALL_PARTS
from ..errors import EmptyNoteError, MissingSkinCodeError, MissingSkinRarityCodeError
from ..valkyrie_db import ValkyrieDatabase

if TYPE_CHECKING:
    from . import Battlesuit, Part, Skin, SkinRarity, Valkyrie

@dataclass(kw_only=True)
class Avatar:
    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:        "str        | None" = None

    format: Literal["short", "long"] = "long"
    valkyrie_db: "ValkyrieDatabase" = field(default=None) # pyright: ignore[reportAssignmentType]

    file_name: str = field(init=False)

    def reserve(self):
        self._check_children_no()
        self.register()

    def register(self):
        self.part.add_valkyrie(self.valkyrie)
        self.valkyrie.add_battlesuit(self.battlesuit)

        if self.skin_rarity is None or self.skin is None:
            return

        self.battlesuit.add_skin_rarity(self.skin_rarity)
        self.skin_rarity.add_skin(self.skin)

    @classmethod
    def from_file(
        cls,
        file: str | Path,
        format: Literal["short", "long"] = "long"
    ) -> Self:
        file_name, raw_avatar = cls._raw_from_file(file, format)
        self = cls.from_raw(file_name, **raw_avatar)
        self.register()

        return self

    @classmethod
    def from_raw(
        cls,
        file_name: str,
        part_code:        str,
        valkyrie_code:    int,
        battlesuit_code:  int,
        skin_rarity_code: int | None = None,
        skin_code:        int | None = None,
        raw_note:         str | None = None,
        *,
        format: Literal["short", "long"] = "long"
    ) -> Self:
        part = cls._resolve_part(part_code, format, file_name)
        valkyrie = cls._resolve_valkyrie(valkyrie_code, battlesuit_code, part, file_name)
        battlesuit = cls._resolve_battlesuit(battlesuit_code, valkyrie, file_name)
        skin_rarity, skin = cls._resolve_rarity_and_skin(skin_rarity_code, skin_code, battlesuit, file_name)

        note = cls._format_note(raw_note, file_name)

        self = cls(
            part=part,
            valkyrie=valkyrie,
            battlesuit=battlesuit,
            skin_rarity=skin_rarity,
            skin=skin,
            note=note
        )
        self.file_name = file_name
        return self


    def _check_children_no(self):
        if self.part.no is None:
            raise ReserveMissingPartNo(self) # Failed to reserve part for avatar ... because the no field is missing

        if self.valkyrie.no is None:
            raise ReserveMissingValkyrieNo(self) # Failed to reserve valkyrie for avatar ... because the no field is missing


        if self.skin_rarity is None or self.skin is None:
            return

        if self.battlesuit.no is None:
            raise ReserveMissingBattlesuitNo(self) # Failed to reserve battlesuit for avatar ... because the no field is missing

        if self.skin_rarity.no is None:
            raise ReserveMissingSkinRarityNo(self) # Failed to reserve skin rarity for avatar ... because the no field is missing


    @classmethod
    def _resolve_part(cls, part_code: str, format: Literal["short", "long"], file_name: str) -> "Part":
        part = Part.by_code(part_code, format)

        if part is None:
            raise InvalidPartCodeError(part_code, file_name)

        return part

    @classmethod
    def _resolve_valkyrie(
        cls,
        valkyrie_code: int,
        battlesuit_code: int,
        part: "Part",
        file_name: str
    ) -> "Valkyrie":
        valkyrie = Valkyrie.by_code(valkyrie_code, battlesuit_code, part)

        if valkyrie is None:
            raise InvalidValkyrieCodeError(valkyrie_code, file_name)

        return valkyrie

    @classmethod
    def _resolve_battlesuit(
        cls,
        battlesuit_code: int,
        valkyrie: "Valkyrie",
        file_name: str
    ) -> "Battlesuit":
        battlesuit = Battlesuit.by_code(battlesuit_code, valkyrie)

        if battlesuit is None:
            raise InvalidBattlesuitCodeError(battlesuit_code, file_name)

        return battlesuit

    @classmethod
    def _resolve_rarity_and_skin(
        cls,
        skin_rarity_code: int | None,
        skin_code: int | None,
        battlesuit: "Battlesuit",
        file_name: str
    ) -> tuple[None, None] | tuple["SkinRarity", "Skin"]:
        match (skin_rarity_code, skin_code):
            case (None, None):
                skin_rarity = skin = None

            case (skin_rarity_code, None):
                raise MissingSkinCodeError(skin_rarity_code, file_name)

            case (None, skin_code):
                raise MissingSkinRarityCodeError(skin_code, file_name)

            case _:
                skin_rarity = SkinRarity.by_code(skin_rarity_code, battlesuit)
                if skin_rarity is None:
                    raise InvalidSkinRarityCodeError(skin_rarity_code, file_name)

                skin = Skin.by_code(skin_code, skin_rarity)
                if skin is None:
                    raise InvalidSkinCodeError(skin_code, file_name)

        return (skin_rarity, skin) # pyright: ignore[reportReturnType]

    @classmethod
    def _format_note(
        cls,
        note: str | None,
        file_name: str
    ) -> str:
        if not note:
            raise EmptyNoteError(note, file_name)

        if note.lower() == "b":
            note = "Veliona"

        return note


    @classmethod
    def _raw_from_file(
        cls,
        file: str | Path,
        format: Literal["short", "long"] = "long"
    ) -> tuple[str, dict[str, Any]]:
        file_name = Path(file).name
        code, *extra_info_parts = file_name.split("_", maxsplit=3)

        part_code, valkyrie_code, battlesuit_code = cls._parse_avatar_code(code, file_name, format)
        skin_rarity_code, skin_code, raw_note = cls._parse_extra_info(extra_info_parts, file_name)

        return file_name, {
            "part_code":        part_code,
            "valkyrie_code":    valkyrie_code,
            "battlesuit_code":  battlesuit_code,
            "skin_rarity_code": skin_rarity_code,
            "skin_code":        skin_code,
            "raw_note":         raw_note,
            "format":           format
        }


    @staticmethod
    def _parse_avatar_code(code: str, file_name: str, format: Literal["short", "long"]) -> tuple[Part, int, int]:
        for part in ALL_PARTS:
            pattern = part.pattern_short if format == "short" else part.pattern_long

            if match := pattern.match(code.rjust(5, "0")):
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
    ) -> (
        tuple[str, str, str]
        | tuple[str, str, None]
        | tuple[None, None, str]
        | tuple[None, None, None]
    ):
        skin_rarity_code: str | None
        skin_code: str | None
        note: str | None

        match info_parts:
            case [skin_rarity_code, skin_code, note]:
                return skin_rarity_code, skin_code, note

            case [skin_rarity_code, skin_code]:
                return skin_rarity_code, skin_code, None

            case [note]:
                return None, None, note

            case []:
                return None, None, None

            case _:
                raise InvalidExtraInfoError(info_parts, file_name)


    def __iter__(self):
        return iter(
            (self.part.no, self.valkyrie.code, self.battlesuit.code)
            + (
                (self.skin_rarity.code, self.skin.code, self.note)
                if (self.skin_rarity is not None and self.skin is not None)
                else (self.note,)
            )
        )
