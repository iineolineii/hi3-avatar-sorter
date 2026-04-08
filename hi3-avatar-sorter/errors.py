import json
import re
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import PartIDFormat
    from .models import Part
    from .models.avatar import RawAvatar


# NOTE#2: This function is placed here to prevent circular import of utils.py
def snake_case(text: str) -> str:
    # Source: https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-97.php
    # License: CC BY 4.0
    return "_".join(
        re.sub("([A-Z][a-z]+)", r" \1",
        re.sub("([A-Z]+)", r" \1",
        text.replace("-", " "))).split()).lower()

class BaseError(ValueError):
    pass


class PathError(BaseError):
    pass


class ParsingError(BaseError):
    pass


class NonDirectorySourceFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Source folder {str(folder)!r} is not a directory")


class EmptySourceFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Source folder {str(folder)!r} is empty")


class NonDirectoryOutputFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Output folder {str(folder)!r} is not a directory")


class NonEmptyOutputFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        super().__init__(f"Output folder {str(folder)!r} is not empty")


class EmptyInputStringError(ParsingError):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

        super().__init__(f"Input string is empty")


class MissingAvatarIdError(ParsingError):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

        super().__init__(f"Avatar ID is missing in file {file_name!r}")


class UnknownPartIdError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        super().__init__(f"Unknown part ID {id!r}")

class UnknownPartNoError(ParsingError):
    def __init__(self, no: int, id_format: "PartIDFormat") -> None:
        self.no = no
        self.id_format = id_format

        super().__init__(f"Unknown part with no {no!r} and ID format {id_format!r}")

class AmbiguousPartNoError(ParsingError):
    def __init__(self, no: int, id_format: "PartIDFormat", candidates: list["Part"]) -> None:
        self.no = no
        self.id_format = id_format
        self.candidates = candidates

        super().__init__(
            f"Multiple parts with no {no!r} and "
            f"ID format {id_format!r} were found: {candidates!r}. "
            f"Maybe your part map contains duplicates?"
        )


class UnknownValkyrieIdError(ParsingError):
    def __init__(self, valkyrie_id: str, battlesuit_id: str) -> None:
        self.valkyrie_id = valkyrie_id
        self.battlesuit_id = battlesuit_id

        super().__init__(f"Unknown valkyrie ID {valkyrie_id!r} with battlesuit ID {battlesuit_id!r}")


class UnknownSkinRarityIdError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        super().__init__(f"Unknown skin rarity ID {id!r}")

class MissingSkinRarityIdError(ParsingError):
    def __init__(self, raw_avatar: "RawAvatar") -> None:
        self.raw_avatar = raw_avatar

        super().__init__(
            "The following avatar structure contains "
            "skin_id but is missing skin_rarity_id: "
            + json.dumps(raw_avatar, indent=4)
        )


class MissingSkinIdError(ParsingError):
    def __init__(self, raw_avatar: "RawAvatar") -> None:
        self.raw_avatar = raw_avatar

        super().__init__(
            "The following avatar structure contains "
            "skin_rarity_id but is missing skin_id: "
            + json.dumps(raw_avatar, indent=4)
        )


class TooLongIdError(ParsingError):
    def __init__(self, id: str, max_length: int, class_name: str) -> None:
        self.id = id
        self.max_length = max_length
        self.class_name = class_name

        super().__init__(f"ID {id!r} is too long: it's length {len(id)!r} exceeds the maximum {max_length!r} for class {class_name!r}")


class EmptyNoteError(ParsingError):
    def __init__(self, note: str | None) -> None:
        self.note = note

        super().__init__(f"Note {note!r} is empty or None")


class MissingReservationAttributeError(ParsingError, AttributeError):
    def __init__(self, key: str, class_name: str, attr_name: str) -> None:
        self.class_name = class_name
        self.key = key

        super().__init__(
            f"Could not reserve key {key!r}: "
            f"{class_name!r} object has no {attr_name!r} attribute. "
            f"Maybe you forgot to call 'get_or_add_{snake_case(attr_name)}'?"
        )


class MissingChildrenAttributeError(ParsingError, AttributeError):
    def __init__(self, class_name: str) -> None:
        self.class_name = class_name

        super().__init__(f"Children attribute is missing for {class_name!r}")


__all__ = [
    "BaseError",
    "PathError",
    "ParsingError",
    "NonDirectorySourceFolderError",
    "EmptySourceFolderError",
    "NonDirectoryOutputFolderError",
    "NonEmptyOutputFolderError",
    "EmptyInputStringError",
    "MissingAvatarIdError",
    "UnknownPartIdError",
    "UnknownValkyrieIdError",
    "UnknownSkinRarityIdError",
    "TooLongIdError",
    "EmptyNoteError",
    "MissingReservationAttributeError",
    "MissingChildrenAttributeError"
]
