from dataclasses import field
from typing import TYPE_CHECKING

from mixins import HasChildren

from .base import BaseModel

if TYPE_CHECKING:
    from .battlesuit import Battlesuit


MAX_BATTLESUIT_ID = 100

class Valkyrie(BaseModel, HasChildren["Battlesuit"]):
    name: str
    no: int = field(init=True)

    children_id_range: range = range(0, MAX_BATTLESUIT_ID)

    def __str__(self) -> str:
        return self.name


__all__ = ["Valkyrie"]
