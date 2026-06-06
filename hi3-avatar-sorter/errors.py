import json
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

from .enums import PartNumber

if TYPE_CHECKING:
    from .enums import PartIDFormat
    from .models.avatar import RawAvatar


class BaseError(ValueError):
    pass

class ParsingError(BaseError):
    pass

class PathError(BaseError):
    pass


class EmptyNoteError(ParsingError):
    def __init__(self, note: str | None) -> None:
        self.note = note

        return super().__init__(f"Note {note!r} is empty or None.")


class MissingAvatarIDError(ParsingError):
    def __init__(self, raw_avatar: dict[str, str | None] | Iterable[str | int]) -> None:
        self.raw_avatar = raw_avatar

        return super().__init__(f"Raw avatar is missing Avatar ID: {raw_avatar!r}.")

class MissingPartIDError(ParsingError):
    def __init__(self, raw_avatar: dict[str, str | None] | Iterable[str | int]) -> None:
        self.raw_part = raw_avatar

        return super().__init__(f"Raw avatar is missing Part ID: {raw_avatar!r}.")

class MissingValkyrieIDError(ParsingError):
    def __init__(self, raw_avatar: dict[str, str | None] | Iterable[str | int]) -> None:
        self.raw_valkyrie = raw_avatar

        return super().__init__(f"Raw avatar is missing Valkyrie ID: {raw_avatar!r}.")

class MissingBattlesuitIDError(ParsingError):
    def __init__(self, raw_avatar: dict[str, str | None] | Iterable[str | int]) -> None:
        self.raw_battlesuit = raw_avatar

        return super().__init__(f"Raw avatar is missing Battlesuit ID: {raw_avatar!r}.")

class MissingSkinRarityIDError(ParsingError):
    def __init__(self, raw_avatar: dict[str, str | None] | Iterable[str | int]) -> None:
        self.raw_avatar = raw_avatar

        return super().__init__(
            "Raw avatar contains "
            "Skin ID but is missing Skin rarity ID: "
            f"{json.dumps(raw_avatar, indent=4)}."
        )

class MissingSkinIDError(ParsingError):
    def __init__(self, raw_avatar: dict[str, str | None] | Iterable[str | int]) -> None:
        self.raw_avatar = raw_avatar

        return super().__init__(
            "Raw avatar contains "
            "Skin rarity ID but is missing Skin ID: "
            f"{json.dumps(raw_avatar, indent=4)}."
        )

class DuplicateRawAvatarError(ParsingError):
    def __init__(self, raw_avatar: RawAvatar, file_name: str, duplicate_file_name: str) -> None:
        self.raw_avatar = raw_avatar
        self.file_name = file_name
        self.duplicate_file_name = duplicate_file_name

        return super().__init__(
            f"Duplicate Raw avatar {str(raw_avatar)!r} "
            f"in {file_name!r} and {duplicate_file_name!r}."
        )


class EmptySourceFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        return super().__init__(f"Source folder {str(folder)!r} is empty.")

class NonDirectoryOutputFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        return super().__init__(f"Output folder {str(folder)!r} is not a directory.")

class NonDirectorySourceFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        return super().__init__(f"Source folder {str(folder)!r} is not a directory.")

class NonEmptyOutputFolderError(PathError):
    def __init__(self, folder: str | Path) -> None:
        self.folder = folder

        return super().__init__(f"Output folder {str(folder)!r} is not empty.")

class UnknownSourceFolderNameError(PathError):
    def __init__(self, folder: str | Path, known_folder_names: Iterable[str]) -> None:
        self.folder = folder
        self.known_folder_names = known_folder_names

        return super().__init__(
            f"Could not recognize Part ID format by source folder name: {str(folder)!r}. "
            f"Consider renaming it to one of the following: {', '.join(known_folder_names)}. "
            f"Or specify 'part_id_format' manually in the 'main' function."
        )


class NonNumericIDError(ParsingError):
    def __init__(self, id: str, class_name: str) -> None:
        return super().__init__(
            f"ID {id!r} is not numeric: "
            f"it contains non-digit characters "
            f"and is invalid for class {class_name!r}."
        )

class TooLongIDError(ParsingError):
    def __init__(self, id: str, max_length: int, class_name: str) -> None:
        self.id = id
        self.max_length = max_length
        self.class_name = class_name

        return super().__init__(
            f"ID {id!r} is too long: "
            f"its length {len(id)!r} exceeds the maximum "
            f"{max_length!r} for class {class_name!r}."
        )


class TooLongSuffixError(ParsingError):
    def __init__(self, suffix: list[str]):
        self.suffix = suffix

        return super().__init__(
            "Raw avatar suffix cannot contain more than "
            "3 elements (Skin rarity ID, Skin ID and Note): "
            f"{suffix!r}."
        )


class UnknownPartIDError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        return super().__init__(f"Unknown Part ID {id!r}.")

class WrongPartIDFormat(ParsingError):
    def __init__(self, id_format: "PartIDFormat", expected_id_format: "PartIDFormat") -> None:
        self.id_format = id_format
        self.expected_id_format = expected_id_format

        return super().__init__(
            f"Wrong Part ID format {id_format.value!r}. "
            f"Expected {expected_id_format.value!r}"
        )

class UnknownPartNoError(ParsingError):
    def __init__(self, no: "PartNumber", id_format: "PartIDFormat") -> None:
        self.no = no
        self.id_format = id_format

        return super().__init__(
            f"Unknown Part with number {no.value!r} "
            f"and ID format {id_format.value!r}."
        )


class UnknownValkyrieIDError(ParsingError):
    def __init__(self, id: str, battlesuit_id: str, part_no: "PartNumber") -> None:
        self.id = id
        self.battlesuit_id = battlesuit_id
        self.part_no = part_no

        return super().__init__(
            f"Unknown Valkyrie ID {id!r} "
            f"with Battlesuit ID {battlesuit_id!r} "
            f"for Part number {part_no.value!r}."
        )


class InvalidBattlesuitIDError(ParsingError):
    def __init__(self, id: str, valkyrie_name: str, id_range: range) -> None:
        self.id = id
        self.valkyrie_name = valkyrie_name
        self.id_range = id_range

        return super().__init__(
            f"Battlesuit ID {id!r} is invalid "
            f"for Valkyrie {valkyrie_name!r}: "
            f"it must be in range from "
            f"{id_range.start!r} to {id_range.stop!r}."
        )


class UnknownSkinRarityIDError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        return super().__init__(f"Unknown Skin rarity ID {id!r}.")


__all__ = [
    "BaseError",
    "EmptyNoteError",
    "EmptySourceFolderError",
    "InvalidBattlesuitIDError",
    "MissingAvatarIDError",
    "MissingBattlesuitIDError",
    "MissingPartIDError",
    "MissingSkinIDError",
    "MissingSkinRarityIDError",
    "MissingValkyrieIDError",
    "NonDirectoryOutputFolderError",
    "NonDirectorySourceFolderError",
    "NonEmptyOutputFolderError",
    "NonNumericIDError",
    "ParsingError",
    "PathError",
    "TooLongIDError",
    "TooLongSuffixError",
    "UnknownPartIDError",
    "UnknownPartNoError",
    "UnknownSkinRarityIDError",
    "UnknownSourceFolderNameError",
    "UnknownValkyrieIDError"
]
