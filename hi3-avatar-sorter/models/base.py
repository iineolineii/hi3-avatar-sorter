from dataclasses import dataclass, field
from typing import ClassVar

from ..errors import NonNumericIDError, TooLongIDError


@dataclass
class BaseModel:
    id: str

    no: int = field(init=False)
    id_length: ClassVar[int] = 2

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if getattr(cls, "__hash__", None) is None:
            cls.__hash__ = BaseModel.__hash__

    def __post_init__(self) -> None:
        self.id = self.validate_id(self.id)

    @classmethod
    def validate_id(cls, id: str) -> str:
        id = id.rjust(cls.id_length, "0")

        if len(id) > cls.id_length:
            raise TooLongIDError(id, cls.id_length, cls.__name__)

        if not id.isnumeric():
            raise NonNumericIDError(id, cls.__name__)

        return id

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"№{int(self)}"

    def __hash__(self) -> int:
        return hash((self.id, self.no))


__all__ = ["BaseModel"]
