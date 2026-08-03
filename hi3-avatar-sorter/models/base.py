from dataclasses import dataclass, field
from typing import ClassVar

from ..errors import NonNumericIDError, TooLongIDError
from ..utils import capitalize

MISSING = 0

@dataclass(frozen=True, slots=True)
class BaseModel:
    id: str

    no: int = field(init=False, default=MISSING)
    id_length: ClassVar[int] = 2

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", self.validate_id(self.id))

    @classmethod
    def validate_id(cls, id: str) -> str:
        id = id.strip().rjust(cls.id_length, "0")

        if not id.isnumeric():
            raise NonNumericIDError(id, cls.__name__)

        if len(id) > cls.id_length:
            raise TooLongIDError(id, cls.id_length, cls.__name__)

        return id

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"{capitalize(type(self).__name__)} №{int(self)}"

    def __hash__(self) -> int:
        return hash((self.id, self.no))


__all__ = ["BaseModel"]
