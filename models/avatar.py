from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Self

from .. import ALL_PARTS
from ..errors import EmptyNoteError, InvalidAvatarIdError, InvalidBattlesuitIdError, InvalidExtraInfoError, InvalidPartIdError, InvalidSkinIdError, InvalidSkinRarityIdError, InvalidValkyrieIdError, MissingSkinIdError, MissingSkinRarityIdError, ReserveMissingBattlesuitNo, ReserveMissingPartNo, ReserveMissingSkinRarityNo, ReserveMissingValkyrieNo
from ..valkyrie_db import ValkyrieDatabase

if TYPE_CHECKING:
    from . import Battlesuit, Part, Skin, SkinRarity, Valkyrie

@dataclass
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
        part_id:        str,
        valkyrie_id:    int,
        battlesuit_id:  int,
        skin_rarity_id: int | None = None,
        skin_id:        int | None = None,
        raw_note:         str | None = None,
        *,
        format: Literal["short", "long"] = "long"
    ) -> Self:
        part = cls._resolve_part(part_id, format, file_name)
        valkyrie = cls._resolve_valkyrie(valkyrie_id, battlesuit_id, part, file_name)
        battlesuit = cls._resolve_battlesuit(battlesuit_id, valkyrie, file_name)
        skin_rarity, skin = cls._resolve_rarity_and_skin(skin_rarity_id, skin_id, battlesuit, file_name)

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
            raise ReserveMissingPartNo(self)

        if self.valkyrie.no is None:
            raise ReserveMissingValkyrieNo(self)

        if self.skin_rarity is None or self.skin is None:
            return

        if self.battlesuit.no is None:
            raise ReserveMissingBattlesuitNo(self)

        if self.skin_rarity.no is None:
            raise ReserveMissingSkinRarityNo(self)


    @classmethod
    def _resolve_part(cls, part_id: str, format: Literal["short", "long"], file_name: str) -> "Part":
        part = Part.by_id(part_id, format)

        if part is None:
            raise InvalidPartIdError(part_id, file_name)

        return part

    @classmethod
    def _resolve_valkyrie(
        cls,
        valkyrie_id: int,
        battlesuit_id: int,
        part: "Part",
        file_name: str
    ) -> "Valkyrie":
        valkyrie = Valkyrie.by_id(valkyrie_id, battlesuit_id, part)

        if valkyrie is None:
            raise InvalidValkyrieIdError(valkyrie_id, file_name)

        return valkyrie

    @classmethod
    def _resolve_battlesuit(
        cls,
        battlesuit_id: int,
        valkyrie: "Valkyrie",
        file_name: str
    ) -> "Battlesuit":
        battlesuit = Battlesuit.by_id(battlesuit_id, valkyrie)

        if battlesuit is None:
            raise InvalidBattlesuitIdError(battlesuit_id, file_name)

        return battlesuit

    @classmethod
    def _resolve_rarity_and_skin(
        cls,
        skin_rarity_id: int | None,
        skin_id: int | None,
        battlesuit: "Battlesuit",
        file_name: str
    ) -> tuple[None, None] | tuple["SkinRarity", "Skin"]:
        match (skin_rarity_id, skin_id):
            case (None, None):
                skin_rarity = skin = None

            case (skin_rarity_id, None):
                raise MissingSkinIdError(skin_rarity_id, file_name)

            case (None, skin_id):
                raise MissingSkinRarityIdError(skin_id, file_name)

            case _:
                skin_rarity = SkinRarity.by_id(skin_rarity_id, battlesuit)
                if skin_rarity is None:
                    raise InvalidSkinRarityIdError(skin_rarity_id, file_name)

                skin = Skin.by_id(skin_id, skin_rarity)
                if skin is None:
                    raise InvalidSkinIdError(skin_id, file_name)

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
        id, *extra_info_parts = file_name.split("_", maxsplit=3)

        part_id, valkyrie_id, battlesuit_id = cls._parse_avatar_id(id, file_name, format)
        skin_rarity_id, skin_id, raw_note = cls._parse_extra_info(extra_info_parts, file_name)

        return file_name, {
            "part_id":        part_id,
            "valkyrie_id":    valkyrie_id,
            "battlesuit_id":  battlesuit_id,
            "skin_rarity_id": skin_rarity_id,
            "skin_id":        skin_id,
            "raw_note":         raw_note,
            "format":           format
        }


    @staticmethod
    def _parse_avatar_id(id: str, file_name: str, format: Literal["short", "long"]) -> tuple[Part, int, int]:
        for part in ALL_PARTS:
            pattern = part.pattern_short if format == "short" else part.pattern_long

            if match := pattern.match(id.rjust(5, "0")):
                match_dict      = match.groupdict()
                valkyrie_id   = int(match_dict["valkyrie_id"])
                battlesuit_id = int(match_dict["battlesuit_id"])

                return part, valkyrie_id, battlesuit_id

        raise InvalidAvatarIdError(id, file_name)

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
        skin_rarity_id: str | None
        skin_id: str | None
        note: str | None

        match info_parts:
            case [skin_rarity_id, skin_id, note]:
                return skin_rarity_id, skin_id, note

            case [skin_rarity_id, skin_id]:
                return skin_rarity_id, skin_id, None

            case [note]:
                return None, None, note

            case []:
                return None, None, None

            case _:
                raise InvalidExtraInfoError(info_parts, file_name)


    def __iter__(self):
        result = (self.part.no, self.valkyrie.id, self.battlesuit.id)

        if self.skin_rarity is not None and self.skin is not None:
            result += (self.skin_rarity.id, self.skin.id)

        if self.note:
            result += (self.note,)

        return iter(result)
