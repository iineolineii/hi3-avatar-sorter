from dataclasses import dataclass, field

from .base import BaseModel
from .battlesuit import Battlesuit
from ..containers import MutableContainer


@dataclass
class Valkyrie(BaseModel):
    name: str
    battlesuits: "MutableContainer[str, Battlesuit]" = field(default_factory=MutableContainer) # pyright: ignore[reportAssignmentType]
    battlesuit_id_range: range = field(default=range(0, 100))

    def add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        self.battlesuits[battlesuit.id] = battlesuit
        return battlesuit

    def get_or_add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self.battlesuits.get(battlesuit.id, battlesuit)

    def reserve_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self.battlesuits.reserve(battlesuit.id, battlesuit, int(battlesuit.id))

    def __str__(self) -> str:
        return self.name


__all__ = ["Valkyrie"]
