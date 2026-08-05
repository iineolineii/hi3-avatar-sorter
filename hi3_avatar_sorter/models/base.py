from dataclasses import Field, dataclass, field
from typing import Any, ClassVar, dataclass_transform

from ..errors import NonNumericIDError, TooLongIDError, UnknownIDError
from ..utils import title_case

MISSING = 0
MAX_MODEL_ID = 99
DEFAULT_VALID_IDS = set(map(str, range(MAX_MODEL_ID)))

@dataclass_transform(
    eq_default=True,
    frozen_default=True,
    field_specifiers=(field,)
)
class _BaseModelMeta(type):
    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwds: Any
    ) -> type["_BaseModelMeta"]:
        cls = super().__new__(cls, name, bases, namespace, **kwds)

        transform: dict[str, Any] = getattr(_BaseModelMeta, "__dataclass_transform__")
        eq:        bool = transform["eq_default"]
        order:     bool = transform["order_default"]
        kw_only:   bool = transform["kw_only_default"]
        frozen:    bool = transform["frozen_default"]
        kwargs:    dict = transform["kwargs"]

        return dataclass(eq=eq, order=order, kw_only=kw_only, frozen=frozen, **kwargs)(cls)


class BaseModel(metaclass=_BaseModelMeta):
    no: int = field(init=False, default=MISSING)
    id: str

    id_length: ClassVar[int] = 2
    valid_ids: ClassVar[set[str]] = DEFAULT_VALID_IDS
    __dataclass_fields__: ClassVar[dict[str, Field]] = {}

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.valid_ids = cls.valid_ids or set()
        cls.__dataclass_fields__ = cls.__dataclass_fields__ or {}

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", self._validate_id(self.id))

    @classmethod
    def _validate_id(cls, id: int | str) -> str:
        id = str(id).strip().rjust(cls.id_length, "0")

        if not id.isnumeric():
            raise NonNumericIDError(id, cls.__name__)

        if len(id) > cls.id_length:
            raise TooLongIDError(id, cls.id_length, cls.__name__)

        if cls.valid_ids and id not in cls.valid_ids:
            raise UnknownIDError(id, cls.valid_ids, cls.__name__)

        return id

    def _update_no(self, value: int) -> None:
        object.__setattr__(self, "no", value)

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"{title_case(type(self).__name__)} №{int(self)}"

    def __hash__(self) -> int:
        return hash((self.id, self.no))


__all__ = ["BaseModel"]
