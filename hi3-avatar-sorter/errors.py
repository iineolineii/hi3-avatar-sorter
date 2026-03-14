from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from .models import Part, Avatar


class InvalidAvatarIdError(ValueError):
    def __init__(self, avatar_id: str | str, file_name: str):
        self.avatar_id = avatar_id
        self.file_name = file_name

        super().__init__(f"Invalid avatar ID {avatar_id!r} in file name {file_name!r}")

class InvalidExtraInfoError(ValueError):
    def __init__(self, info_parts, file_name: str):
        self.name_parts = info_parts
        self.file_name = file_name

        super().__init__(f"Invalid extra info {info_parts!r} in file name {file_name!r}. Maybe it has length other that 1, 2 or 3?")

class InvalidPartIdError(ValueError):
    def __init__(self, part_id: str | str, file_name: str) -> None:
        self.part_id = part_id
        self.file_name = file_name

        super().__init__(f"Invalid part ID {part_id!r} in file name {file_name!r}")

class InvalidValkyrieIdError(ValueError):
    def __init__(self, valkyrie_id: str | str, file_name: str) -> None:
        self.valkyrie_id = valkyrie_id
        self.file_name = file_name

        super().__init__(f"Invalid valkyrie ID {valkyrie_id!r} in file name {file_name!r}")

class InvalidBattlesuitIdError(ValueError):
    def __init__(self, battlesuit_id: str | str, file_name: str) -> None:
        self.battlesuit_id = battlesuit_id
        self.file_name = file_name

        super().__init__(f"Invalid battlesuit ID {battlesuit_id!r} in file name {file_name!r}")

class InvalidSkinRarityIdError(ValueError):
    def __init__(self, skin_rarity_id: str | str, file_name: str):
        self.skin_rarity_id = skin_rarity_id
        self.file_name = file_name

        super().__init__(f"Invalid skin rarity ID {skin_rarity_id!r} in file name {file_name!r}")

class InvalidSkinIdError(ValueError):
    def __init__(self, skin_id: str | str, file_name: str):
        self.skin_id = skin_id
        self.file_name = file_name

        super().__init__(f"Invalid skin ID {skin_id!r} in file name {file_name!r}")

class EmptyNoteError(ValueError):
    def __init__(self, note, file_name: str):
        self.note = note
        self.file_name = file_name

        super().__init__(f"Invalid empty note {note!r} in file name {file_name!r}")

class ValkyrieNotFoundError(ValueError):
    def __init__(self, valkyrie_id: str | str, part: "Part", battlesuit_id: str | str):
        self.valkyrie_id = valkyrie_id
        self.battlesuit_id = battlesuit_id

        super().__init__(f"No Valkyrie found in part {part.no!r} with ID {valkyrie_id!r} containing battlesuit ID {battlesuit_id!r}")

class MissingSkinRarityIdError(AttributeError):
    def __init__(self, skin_id: str | str, file_name: str):
        self.skin_id = skin_id
        self.file_name = file_name

        super().__init__(f"Missing rarity ID for skin ID {skin_id!r} in file name {file_name!r}")

class MissingSkinIdError(AttributeError):
    def __init__(self, skin_rarity_id: str | str, file_name: str):
        self.skin_rarity_id = skin_rarity_id
        self.file_name = file_name

        super().__init__(f"Missing skin ID for rarity ID {skin_rarity_id!r} in file name {file_name!r}")

class ReserveMissingPartNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)!r} because the .part.no field is missing")

class ReserveMissingValkyrieNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)!r} because the .valkyrie.no field is missing")

class ReserveMissingBattlesuitNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)!r} because the .battlesuit.no field is missing")

class ReserveMissingSkinRarityNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)!r} because the .skin_rarity.no field is missing")

class SourceFolderIsNotDirectoryError(ValueError):
    def __init__(self, source_folder: "str | Path") -> None:
        self.source_folder = source_folder

        super().__init__(f"Source folder {str(source_folder)!r} is not a directory")

class SourceFolderIsEmptyError(ValueError):
    def __init__(self, source_folder: "str | Path") -> None:
        self.source_folder = source_folder

        super().__init__(f"Source folder {str(source_folder)!r} is empty")

class OutputFolderIsNotDirectoryError(ValueError):
    def __init__(self, output_folder: "str | Path") -> None:
        self.output_folder = output_folder

        super().__init__(f"Output folder {str(output_folder)!r} is not a directory")

class OutputFolderIsNotEmptyError(ValueError):
    def __init__(self, output_folder: "str | Path") -> None:
        self.output_folder = output_folder

        super().__init__(f"Output folder {str(output_folder)!r} is not empty")


class IdValidationError(ValueError):
    msg: str

    def __init__(self, id: str, file: "str | Path | None" = None) -> None:
        self.id   = id
        self.file = file

        if self.file is not None:
            self.msg += f" in file {str(self.file)!r}"

        super().__init__(self.msg % self.id)


    def with_file(self, file: "str | Path"):
        IdValidationError.__init__(self, self.id, file)
        return self

class UnknownPartIdError(IdValidationError):
    msg = "Unknown Part ID %r"
