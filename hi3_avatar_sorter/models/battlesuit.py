from typing import TYPE_CHECKING

from . import BaseModel
from ..mixins import HasChildren

if TYPE_CHECKING:
    from .skin_rarity import SkinRarity


class Battlesuit(BaseModel, HasChildren["SkinRarity"]):
    pass


__all__ = ["Battlesuit"]
