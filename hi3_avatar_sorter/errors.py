from collections.abc import Iterable, Sequence
from typing import Any


class BaseError(ValueError):
    pass


class EmptyNoteError(BaseError):
    def __init__(self, note: str | None) -> None:
        self.note = note

        return super().__init__(f"Note {note!r} is empty or None.")


class TooLongSuffixError(BaseError):
    def __init__(self, suffix: Sequence[int | str]):
        self.suffix = suffix

        return super().__init__(
            "Raw avatar suffix cannot contain more than "
            "3 elements (Skin rarity ID, Skin ID and Note): "
            f"{suffix!r}."
        )


class BattlesuitIDOutOfRangeError(BaseError):
    def __init__(
        self,
        battlesuit_id: int | str,
        expected_range: range
    ) -> None:
        battlesuit_id = int(battlesuit_id)
        self.battlesuit_id = battlesuit_id
        self.expected_range = expected_range

        return super().__init__(
            f"Battlesuit ID {battlesuit_id!r} is out of range "
            f"from {expected_range.start!r} to {expected_range.stop!r}."
        )


class InvalidBattlesuitIDRangeError(BaseError):
    def __init__(
        self,
        valkyrie_id: str,
        start: int,
        end: int
    ) -> None:
        super().__init__(
            f"Valkyrie with ID {valkyrie_id!r} has invalid Battlesuit ID range: "
            f"start of the range {start} is not less than its end {end}"
        )


class NonNumericIDError(BaseError):
    def __init__(self, id: str, class_name: str) -> None:
        return super().__init__(
            f"ID {id!r} is not numeric: "
            f"it contains non-digit characters "
            f"and is invalid for class {class_name!r}."
        )


class TooLongIDError(BaseError):
    def __init__(self, id: str, max_length: int, class_name: str) -> None:
        self.id = id
        self.max_length = max_length
        self.class_name = class_name

        return super().__init__(
            f"ID {id!r} is too long: "
            f"its length {len(id)!r} exceeds the maximum "
            f"{max_length!r} for class {class_name!r}."
        )


class MissingFieldError(KeyError):
    def __init__(self, field_name: str, raw_avatar: dict[str, str | None] | Iterable[str | int]) -> None:
        self.raw_battlesuit = raw_avatar

        return super().__init__(f"Raw avatar is missing {field_name}: {raw_avatar!r}.")


class ModelNotFoundError(KeyError):
    def __init__(self, class_name: str, criteria: list[str] = []) -> None:
        self.class_name = class_name
        self.criteria = criteria

        message = f"No {class_name!r} entities were found"

        if criteria:
            criteria_str = "; ".join(criteria)
            message += f" by the following criteria: {criteria_str}"

        super().__init__(message.strip() + ".")


class InvalidChildNumberError(BaseError):
    def __init__(self, class_name: str, child_no: int) -> None:
        super().__init__(f"Child number {child_no} is not positive.")

class DuplicateChildNumberError(BaseError):
    def __init__(self, class_name: str, child_no: int) -> None:
        super().__init__(f"Child number {child_no} is already occupied.")

class UnknownIDError(BaseError):
    pass



__all__ = [
    "BaseError",
    "BattlesuitIDOutOfRangeError",
    "InvalidBattlesuitIDRangeError",
    "NonNumericIDError",
    "TooLongIDError"
]
