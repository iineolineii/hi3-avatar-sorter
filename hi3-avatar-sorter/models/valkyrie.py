from dataclasses import dataclass, field

from .base import BaseModel
from .battlesuit import Battlesuit
from ..mex_container import MexContainer


@dataclass
class Valkyrie(BaseModel):
    name: str
    battlesuits: "MexContainer[str, Battlesuit]" = field(default_factory=MexContainer) # pyright: ignore[reportAssignmentType]
    battlesuit_id_range: range = field(default=range(0, 100))

    def add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        self.battlesuits[battlesuit.id] = battlesuit
        return battlesuit

    def get_or_add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        return self.battlesuits.setdefault(battlesuit.id, battlesuit)

    def __str__(self) -> str:
        return self.name


__all__ = ["Valkyrie"]
