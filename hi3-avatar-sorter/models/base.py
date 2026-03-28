from dataclasses import dataclass, field
from typing import ClassVar

from ..errors import TooLongIdError


@dataclass(kw_only=True)
class BaseModel:
    id: str

    no: int = field(default=None) # pyright: ignore[reportAssignmentType]
    id_length: ClassVar[int] = 2

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if getattr(cls, "__hash__", None) is None:
            cls.__hash__ = BaseModel.__hash__

    def __post_init__(self):
        self.id = self._validate_id(self.id)

    @classmethod
    def _validate_id(cls, id: str) -> str:
        id = id.rjust(cls.id_length, "0")

        if len(id) > cls.id_length:
            raise TooLongIdError(id, cls.id_length, cls.__name__)

        return id

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"№{int(self)}"

    def __hash__(self) -> int:
        return hash((self.id, self.no))


@dataclass(kw_only=True)
class NonUniqueIdModel(BaseModel):
    children_id_range: range = field(default=range(0, 100))


__all__ = ["BaseModel", "NonUniqueIdModel"]
