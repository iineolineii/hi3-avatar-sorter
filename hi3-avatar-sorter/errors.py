from pathlib import Path


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


class EmptyFileNameError(PathError):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

        super().__init__(f"File name is empty")


class MissingAvatarIdError(ParsingError):
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

        super().__init__(f"Avatar ID is missing in file {file_name!r}")


class UnknownPartIdError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        super().__init__(f"Unknown part ID {id!r}")


class UnknownValkyrieIdError(ParsingError):
    def __init__(self, valkyrie_id: str, battlesuit_id: str) -> None:
        self.valkyrie_id = valkyrie_id
        self.battlesuit_id = battlesuit_id

        super().__init__(f"Unknown valkyrie ID {valkyrie_id!r} with battlesuit ID {battlesuit_id!r}")


class UnknownSkinRarityIdError(ParsingError):
    def __init__(self, id: str) -> None:
        self.id = id

        super().__init__(f"Unknown skin rarity ID {id!r}")


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


class EmptyReservationNoError(ParsingError, AttributeError):
    def __init__(self, class_name: str, id: str) -> None:
        self.class_name = class_name
        self.id = id

        super().__init__(f"Reservation No is empty for {class_name!r} ID {id!r}")


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
    "EmptyFileNameError",
    "MissingAvatarIdError",
    "UnknownPartIdError",
    "UnknownValkyrieIdError",
    "UnknownSkinRarityIdError",
    "TooLongIdError",
    "EmptyNoteError",
    "EmptyReservationNoError",
    "MissingChildrenAttributeError"
]
