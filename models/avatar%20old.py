from typing import TYPE_CHECKING

from ..errors import (
    EmptyNoteError,
    InvalidAvatarIdError,
    InvalidExtraInfoError,
    InvalidSkinIdError,
    InvalidSkinRarityIdError,
    MissingSkinIdError,
    MissingSkinRarityIdError,
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
    def _parse_avatar_id(id: str, file_name: str) -> tuple[Part, int, int]:
        from .. import ALL_PARTS

        for part in ALL_PARTS:
            if match := part.pattern.match(id.rjust(5, "0")):
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
    ) -> tuple[int, int, str | None] | tuple[None, None, str | None]:
        if not info_parts:
            return None, None, None

        skin_rarity_id: str | None = None
        skin_id:        str | None = None
        note:             str | None = None

        match info_parts:
            case []:
                return None, None, None

            case [note_or_skin_rarity_id]:
                if note_or_skin_rarity_id.isnumeric():
                    skin_rarity_id = cls._validate_skin_rarity_id(note_or_skin_rarity_id, file_name)
                else:
                    note = cls.format_note(note_or_skin_rarity_id, file_name)

            case [skin_rarity_id, skin_id]:
                skin_rarity_id = cls._validate_skin_rarity_id(skin_rarity_id, file_name)
                skin_id = cls._validate_skin_id(skin_id, file_name)

            case [skin_rarity_id, skin_id, note]:
                skin_rarity_id = cls._validate_skin_rarity_id(skin_rarity_id, file_name)
                skin_id = cls._validate_skin_id(skin_id, file_name)
                note = cls.format_note(note, file_name)

            case _:
                raise InvalidExtraInfoError(info_parts, file_name)

        if skin_rarity_id is None:
            if skin_id is None:
                return None, None, note

            raise MissingSkinRarityIdError(skin_id, file_name)

        if skin_id is None:
            raise MissingSkinIdError(skin_rarity_id, file_name)

        return int(skin_rarity_id), int(skin_id), note

    @staticmethod
    def _validate_skin_rarity_id(skin_rarity_id: str, file_name: str) -> str:
        from .. import VALID_SKIN_RARITY_idS

        if skin_rarity_id.isnumeric() and int(skin_rarity_id) in VALID_SKIN_RARITY_idS:
            return skin_rarity_id

        raise InvalidSkinRarityIdError(skin_rarity_id, file_name)

    @staticmethod
    def _validate_skin_id(skin_id: str, file_name: str) -> str:
        if skin_id.isnumeric():
            return skin_id

        raise InvalidSkinIdError(skin_id, file_name)

    @staticmethod
    def format_note(note: str, file_name: str) -> str:
        if note.lower() == "b":
            return "Veliona"

        if note:
            return note

        raise EmptyNoteError(note, file_name)

    def __iter__(self):
        return iter(
            (self.part.no, self.valkyrie.id, self.battlesuit.id)
            + (
                (self.skin_rarity.id, self.skin.id, self.note)
                if (self.skin_rarity is not None and self.skin is not None)
                else (self.note,)
            )
        )
