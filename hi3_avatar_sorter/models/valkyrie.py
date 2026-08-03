from dataclasses import InitVar, field
from typing import TYPE_CHECKING

from . import BaseModel
from .base import MAX_MODEL_ID
from ..mixins import HasChildren

if TYPE_CHECKING:
    from .battlesuit import Battlesuit


class Valkyrie(BaseModel, HasChildren["Battlesuit"]):
    name: str
    max_child_id: InitVar[int] = MAX_MODEL_ID
    children_id_range: range = field(init=False)

    def __post_init__(self, max_child_id: int) -> None:
        super().__post_init__()
        self._update_children_id_range(end=max_child_id)

    def _update_children_id_range(self, *, start: int = 0, end: int = MAX_MODEL_ID) -> None:
        children_id_range = range(start, end)
        object.__setattr__(self, "children_ID_range", children_id_range)

    def __str__(self) -> str:
        return self.name


__all__ = ["Valkyrie"]
