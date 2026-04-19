from dataclasses import dataclass, field
from typing import Any, ClassVar

from ..errors import NonNumericIDError, TooLongIDError


@dataclass(frozen=True, slots=True)
class BaseModel:
    id: str

    no: int = field(init=False)
    id_length: ClassVar[int] = 2

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if getattr(cls, "__hash__", None) is None:
            cls.__hash__ = BaseModel.__hash__

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", self.validate_id(self.id))

    @classmethod
    def validate_id(cls, id: str) -> str:
        id = id.rjust(cls.id_length, "0")

        if len(id) > cls.id_length:
            raise TooLongIDError(id, cls.id_length, cls.__name__)

        if not id.isnumeric():
            raise NonNumericIDError(id, cls.__name__)

        return id

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)

        except AttributeError:
            class_name = type(self).__name__
            base_message = f"{class_name!r} object has no attribute {name!r}."

            if name == "no":
                raise AttributeError(
                    base_message +
                    f" Perhaps it was created without using the "
                    f"'get_or_add_{class_name}' method?"
                )

            raise

    def __int__(self) -> int:
        return self.no + 1

    def __str__(self) -> str:
        return f"№{int(self)}"

    def __hash__(self) -> int:
        return hash((self.id, self.no))


__all__ = ["BaseModel"]
