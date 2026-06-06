from dataclasses import dataclass

from .base import BaseModel


@dataclass(frozen=True, slots=True)
class Skin(BaseModel):
    pass


__all__ = ["Skin"]
