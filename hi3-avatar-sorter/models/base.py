from dataclasses import dataclass, field
from typing import ClassVar

from ..errors import TooShortIdError


@dataclass(kw_only=True)
class BaseModel:
    id: str

    no: int = field(default=None) # pyright: ignore[reportAssignmentType]
    id_length: ClassVar[int] = 2

    @classmethod
    def _validate_id(cls, id: str) -> str:
        id = id.rjust(cls.id_length, "0")

        if len(id) < cls.id_length:
            raise TooShortIdError(id, cls.id_length, cls.__name__)

        return id

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"№{int(self)}"


@dataclass(kw_only=True)
class NonUniqueIdModel(BaseModel):
    children_id_range: range = field(default=range(0, 100))
