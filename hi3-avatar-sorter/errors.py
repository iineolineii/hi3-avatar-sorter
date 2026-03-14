from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Part, Avatar

class InvalidAvatarIdError(ValueError):
    def __init__(self, avatar_id: int | str, file_name: str):
        self.avatar_id = avatar_id
        self.file_name = file_name

        super().__init__(f"Invalid avatar ID {avatar_id!r} in file name {file_name!r}")

class InvalidExtraInfoError(ValueError):
    def __init__(self, info_parts, file_name: str):
        self.name_parts = info_parts
        self.file_name = file_name

        super().__init__(f"Invalid extra info {info_parts!r} in file name {file_name!r}. Maybe it has length other that 1, 2 or 3?")

class InvalidPartIdError(ValueError):
    def __init__(self, part_id: int | str, file_name: str) -> None:
        self.part_id = part_id
        self.file_name = file_name

        super().__init__(f"Invalid part ID {part_id!r} in file name {file_name!r}")

class InvalidValkyrieIdError(ValueError):
    def __init__(self, valkyrie_id: int | str, file_name: str) -> None:
        self.valkyrie_id = valkyrie_id
        self.file_name = file_name

        super().__init__(f"Invalid valkyrie ID {valkyrie_id!r} in file name {file_name!r}")

class InvalidBattlesuitIdError(ValueError):
    def __init__(self, battlesuit_id: int | str, file_name: str) -> None:
        self.battlesuit_id = battlesuit_id
        self.file_name = file_name

        super().__init__(f"Invalid battlesuit ID {battlesuit_id!r} in file name {file_name!r}")

class InvalidSkinRarityIdError(ValueError):
    def __init__(self, skin_rarity_id: int | str, file_name: str):
        self.skin_rarity_id = skin_rarity_id
        self.file_name = file_name

        super().__init__(f"Invalid skin rarity ID {skin_rarity_id!r} in file name {file_name!r}")

class InvalidSkinIdError(ValueError):
    def __init__(self, skin_id: int | str, file_name: str):
        self.skin_id = skin_id
        self.file_name = file_name

        super().__init__(f"Invalid skin ID {skin_id!r} in file name {file_name!r}")

class EmptyNoteError(ValueError):
    def __init__(self, note, file_name: str):
        self.note = note
        self.file_name = file_name

        super().__init__(f"Invalid empty note {note!r} in file name {file_name!r}")

class ValkyrieNotFoundError(ValueError):
    def __init__(self, valkyrie_id: int | str, part: "Part", battlesuit_id: int | str):
        self.valkyrie_id = valkyrie_id
        self.battlesuit_id = battlesuit_id

        super().__init__(f"No Valkyrie found in part {part.no!r} with ID {valkyrie_id!r} containing battlesuit ID {battlesuit_id!r}")

class MissingSkinRarityIdError(AttributeError):
    def __init__(self, skin_id: int | str, file_name: str):
        self.skin_id = skin_id
        self.file_name = file_name

        super().__init__(f"Missing rarity ID for skin ID {skin_id!r} in file name {file_name!r}")

class MissingSkinIdError(AttributeError):
    def __init__(self, skin_rarity_id: int | str, file_name: str):
        self.skin_rarity_id = skin_rarity_id
        self.file_name = file_name

        super().__init__(f"Missing skin ID for rarity ID {skin_rarity_id!r} in file name {file_name!r}")

class ReserveMissingPartNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)} because the .part.no field is missing")

class ReserveMissingValkyrieNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)} because the .valkyrie.no field is missing")

class ReserveMissingBattlesuitNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)} because the .battlesuit.no field is missing")

class ReserveMissingSkinRarityNo(AttributeError):
    def __init__(self, avatar: "Avatar") -> None:
        self.avatar = avatar

        super().__init__(f"Failed to reserve avatar {str(avatar)} because the .skin_rarity.no field is missing")
