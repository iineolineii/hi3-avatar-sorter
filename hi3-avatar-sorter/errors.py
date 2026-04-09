import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from . import PartIDFormat
    from .models import Part


# NOTE#2: This function is placed here to prevent circular import of utils.py
def snake_case(text: str) -> str:
    # Source: https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-97.php
    # License: CC BY 4.0
    return "_".join(
        re.sub("([A-Z][a-z]+)",
        r" \1",
        re.sub("([A-Z]+)", r" \1",
        text.replace("-", " "))).split()).lower()


class BaseError(ValueError):
    pass

class ParsingError(BaseError):
    pass

class PathError(BaseError):
    pass


class EmptyNoteError(ParsingError):
    def __init__(self, note: str | None) -> None:
        self.note = note

        super().__init__(f"Note {note!r} is empty or None")


class MissingAvatarIDError(ParsingError):
    def __init__(self, raw_avatar: Any) -> None:
        self.raw_avatar = raw_avatar

        super().__init__(f"Raw avatar is missing Avatar ID: {raw_avatar!r}")

class MissingPartIDError(ParsingError):
    def __init__(self, raw_avatar: Any) -> None:
        self.raw_part = raw_avatar

        super().__init__(f"Raw avatar is missing Part ID: {raw_avatar!r}")

class MissingValkyrieIDError(ParsingError):
    def __init__(self, raw_avatar: Any) -> None:
        self.raw_valkyrie = raw_avatar

        super().__init__(f"Raw avatar is missing Valkyrie ID: {raw_avatar!r}")

class MissingBattlesuitIDError(ParsingError):
    def __init__(self, raw_avatar: Any) -> None:
        self.raw_battlesuit = raw_avatar

        super().__init__(f"Raw avatar is missing Battlesuit ID: {raw_avatar!r}")

class MissingSkinRarityIDError(ParsingError):
    def __init__(self, raw_avatar: Any) -> None:
        self.raw_avatar = raw_avatar

        super().__init__(
            "Raw avatar contains "
            "Skin ID but is missing Skin rarity ID: "
            + json.dumps(raw_avatar, indent=4)
        )

class MissingSkinIDError(ParsingError):
    def __init__(self, raw_avatar: Any) -> None:
        self.raw_avatar = raw_avatar

        super().__init__(
            "Raw avatar contains "
            "Skin rarity ID but is missing Skin ID: "
            + json.dumps(raw_avatar, indent=4)
        )


class EmptySourceFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Source folder {str(folder)!r} is empty")

class NonDirectoryOutputFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Output folder {str(folder)!r} is not a directory")

class NonDirectorySourceFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Source folder {str(folder)!r} is not a directory")

class NonEmptyOutputFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Output folder {str(folder)!r} is not empty")


class NonNumericIDError(ParsingError):
    def __init__(self, id: str, class_name: str) -> None:
        super().__init__(
            f"ID {id!r} is not numeric: "
            f"it contains non-digit characters "
            f"and is invalid for class {class_name!r}"
        )

class TooLongIDError(ParsingError):
    def __init__(self, id: str, max_length: int, class_name: str) -> None:
        self.id = id
        self.max_length = max_length
        self.class_name = class_name

        super().__init__(
            f"ID {id!r} is too long: "
            f"its length {len(id)!r} exceeds the maximum "
            f"{max_length!r} for class {class_name!r}"
        )


class TooLongSuffixError(ParsingError):
    def __init__(self, suffix: list[str]):
        self.suffix = suffix

        super().__init__(
            "Raw avatar suffix cannot contain more than "
            "3 elements (Skin rarity ID, Skin ID and Note): "
            + str(suffix)
        )


class AmbiguousPartNoError(ParsingError):
    def __init__(self, no: int, id_format: "PartIDFormat", candidates: list["Part"]) -> None:
        self.no = no
        self.id_format = id_format
        self.candidates = candidates

        super().__init__(
            f"Multiple parts with no {no!r} and "
            f"ID format {id_format!r} were found: {candidates!r}. "
            f"Maybe your Part map contains duplicates?"
        )

class UnknownPartIDError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        super().__init__(f"Unknown Part ID {id!r}")

class UnknownPartNoError(ParsingError):
    def __init__(self, no: int, id_format: "PartIDFormat") -> None:
        self.no = no
        self.id_format = id_format

        super().__init__(f"Unknown Part with no {no!r} and ID format {id_format!r}")

class UnknownValkyrieIDError(ParsingError):
    def __init__(self, valkyrie_id: str, battlesuit_id: str) -> None:
        self.valkyrie_id = valkyrie_id
        self.battlesuit_id = battlesuit_id

        super().__init__(f"Unknown Valkyrie ID {valkyrie_id!r} with Battlesuit ID {battlesuit_id!r}")

class UnknownSkinRarityIDError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        super().__init__(f"Unknown Skin rarity ID {id!r}")
