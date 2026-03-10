from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, Self, TypeVar

if TYPE_CHECKING:
    from .one_to_many import OneToMany

ParentT = TypeVar("ParentT", bound="OneToMany")


@dataclass(kw_only=True)
class ManyToOne(Generic[ParentT]):
    code: int
    no: int = field(default=None) # pyright: ignore[reportAssignmentType]

    @classmethod
    def by_code(
        cls,
        code: int,
        parent: ParentT,
        /
    ) -> Self:
        if code in parent._children:
            return parent._children[code] # pyright: ignore[reportReturnType]

        return cls(code)
