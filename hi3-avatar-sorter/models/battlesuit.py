from dataclasses import dataclass

from mixins import HasChildren

from . import SkinRarity
from .base import BaseModel


@dataclass(frozen=True, slots=True)
class Battlesuit(BaseModel, HasChildren["SkinRarity"]):
    pass


__all__ = ["Battlesuit"]
