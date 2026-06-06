from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..errors import InvalidBattlesuitIDError

from .base import BaseModel
from ..utils import MexContainer, mex_field

if TYPE_CHECKING:
    from .battlesuit import Battlesuit


MAX_BATTLESUIT_ID = 100

@dataclass(frozen=True, slots=True)
class Valkyrie(BaseModel):
    name: str
    no: int = field(init=True)

    battlesuits: "MexContainer[str, Battlesuit]" = mex_field()
    battlesuit_id_range: range = range(0, MAX_BATTLESUIT_ID)

    def add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        self.battlesuits[battlesuit.id] = battlesuit
        return battlesuit

    def get_or_add_battlesuit(self, battlesuit: "Battlesuit") -> "Battlesuit":
        if int(battlesuit.id) not in self.battlesuit_id_range:
            raise InvalidBattlesuitIDError(battlesuit.id, self.name, self.battlesuit_id_range)

        return self.battlesuits.setdefault(battlesuit.id, battlesuit)

    def __str__(self) -> str:
        return self.name


__all__ = ["Valkyrie"]
