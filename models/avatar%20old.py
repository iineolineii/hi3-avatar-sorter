from typing import TYPE_CHECKING

from ..errors import (
    EmptyNoteError,
    InvalidAvatarCodeError,
    InvalidExtraInfoError,
    InvalidSkinCodeError,
    InvalidSkinRarityCodeError,
    MissingSkinCodeError,
    MissingSkinRarityCodeError,
)

if TYPE_CHECKING:
    from . import Battlesuit, Part, Skin, SkinRarity, Valkyrie

class Avatar:
    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:         str        | None  = None

    @staticmethod
    def _parse_avatar_code(code: str, file_name: str) -> tuple[Part, int, int]:
        from .. import ALL_PARTS

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
                    note = cls.format_note(note_or_skin_rarity_code, file_name)

            case [skin_rarity_code, skin_code]:
                skin_rarity_code = cls._validate_skin_rarity_code(skin_rarity_code, file_name)
                skin_code = cls._validate_skin_code(skin_code, file_name)

            case [skin_rarity_code, skin_code, note]:
                skin_rarity_code = cls._validate_skin_rarity_code(skin_rarity_code, file_name)
                skin_code = cls._validate_skin_code(skin_code, file_name)
                note = cls.format_note(note, file_name)

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
        from .. import VALID_SKIN_RARITY_CODES

        if skin_rarity_code.isnumeric() and int(skin_rarity_code) in VALID_SKIN_RARITY_CODES:
            return skin_rarity_code

        raise InvalidSkinRarityCodeError(skin_rarity_code, file_name)

    @staticmethod
    def _validate_skin_code(skin_code: str, file_name: str) -> str:
        if skin_code.isnumeric():
            return skin_code

        raise InvalidSkinCodeError(skin_code, file_name)

    @staticmethod
    def format_note(note: str, file_name: str) -> str:
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
