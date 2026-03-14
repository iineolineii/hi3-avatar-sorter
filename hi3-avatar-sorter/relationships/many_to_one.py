from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, Self, TypeVar

if TYPE_CHECKING:
    from .one_to_many import OneToMany


ParentT = TypeVar("ParentT", bound="OneToMany")

@dataclass(kw_only=True)
class ManyToOne(Generic[ParentT]):
    id: str = field(hash=True)
    no: int = field(default=None, hash=False) # pyright: ignore[reportAssignmentType]

    @classmethod
    def by_id(
        cls,
        child_id: str,
        parent: ParentT,
        /
    ) -> Self:
        if child_id in parent._children:
            return parent._children[child_id] # pyright: ignore[reportReturnType]

        return cls(id=child_id)

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"№{int(self)}"
