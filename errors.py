class InvalidAvatarCodeError(ValueError):
    def __init__(self, code: int | str, file_name: str):
        self.code = code
        self.file_name = file_name

        super().__init__(f"Invalid avatar code {code!r} in file name {file_name!r}")

class InvalidAdditionalInfoError(ValueError):
    def __init__(self, name_parts, file_name: str):
        self.name_parts = name_parts
        self.file_name = file_name

        super().__init__(f"Invalid additional info {name_parts!r} in file name {file_name!r}")

class MissingSkinRarityCodeError(ValueError):
    def __init__(self, skin_code: int | str, file_name: str):
        self.skin_code = skin_code
        self.file_name = file_name

        super().__init__(f"Missing rarity code for skin code {skin_code!r} in file name {file_name!r}")

class MissingSkinCodeError(ValueError):
    def __init__(self, skin_rarity_code: int | str, file_name: str):
        self.skin_rarity_code = skin_rarity_code
        self.file_name = file_name

        super().__init__(f"Missing skin code for rarity code {skin_rarity_code!r} in file name {file_name!r}")

class InvalidSkinRarityCodeError(ValueError):
    def __init__(self, skin_rarity_code: int | str, file_name: str):
        self.skin_rarity_code = skin_rarity_code
        self.file_name = file_name

        super().__init__(f"Invalid skin rarity code {skin_rarity_code!r} in file name {file_name!r}")

class InvalidSkinCodeError(ValueError):
    def __init__(self, skin_code: int | str, file_name: str):
        self.skin_code = skin_code
        self.file_name = file_name

        super().__init__(f"Invalid skin code {skin_code!r} in file name {file_name!r}")

class EmptyNoteError(ValueError):
    def __init__(self, note, file_name: str):
        self.note = note
        self.file_name = file_name

        super().__init__(f"Invalid empty note {note!r} in file name {file_name!r}")

class ValkyrieNotFoundError(ValueError):
    def __init__(self, code: int | str, battlesuit_code: int | str):
        self.code = code
        self.battlesuit_code = battlesuit_code

        super().__init__(f"No Valkyrie found for code {code!r} containing battlesuit code {battlesuit_code!r}")
