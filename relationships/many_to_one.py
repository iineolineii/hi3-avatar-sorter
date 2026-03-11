from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, Self, TypeVar

if TYPE_CHECKING:
    from .one_to_many import OneToMany

ParentT = TypeVar("ParentT", bound="OneToMany")


@dataclass(kw_only=True)
class ManyToOne(Generic[ParentT]):
    id: int
    no: int = field(default=None) # pyright: ignore[reportAssignmentType]

    @classmethod
    def by_id(
        cls,
        child_id: int,
        parent: ParentT,
        /
    ) -> Self:
        if child_id in parent._children:
            return parent._children[child_id] # pyright: ignore[reportReturnType]

        return cls(id=child_id)
