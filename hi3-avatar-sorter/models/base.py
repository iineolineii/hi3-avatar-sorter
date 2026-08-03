from dataclasses import Field, dataclass, field
from typing import Any, ClassVar, dataclass_transform

from ..errors import NonNumericIDError, TooLongIDError
from ..utils import capitalize

MISSING = 0


@dataclass_transform(
    eq_default=True,
    frozen_default=True,
    field_specifiers=(field,)
)
class _BaseModelMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any], /, **kwds: Any) -> type["BaseModel"]:
        klass: Any = super().__new__(cls, name, bases, namespace, **kwds)

        transform: dict[str, Any] = getattr(_BaseModelMeta, "__dataclass_transform__")
        eq:        bool = transform["eq_default"]
        order:     bool = transform["order_default"]
        kw_only:   bool = transform["kw_only_default"]
        frozen:    bool = transform["frozen_default"]
        kwargs:    dict = transform["kwargs"]

        return dataclass(klass, eq=eq, order=order, kw_only=kw_only, frozen=frozen, **kwargs)


class BaseModel(metaclass=_BaseModelMeta):
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
