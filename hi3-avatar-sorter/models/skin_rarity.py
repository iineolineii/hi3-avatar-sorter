from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import ClassVar

from .base import BaseModel
from .skin import Skin
from ..mex_container import MexContainer
from ..errors import UnknownSkinRarityIDError


@dataclass
class SkinRarity(BaseModel):
    skins: "MexContainer[str, Skin]" = field(default_factory=MexContainer) # pyright: ignore[reportAssignmentType]
    valid_ids: ClassVar[Iterable[str]] = ("02", "03", "04", "05")

    def add_skin(self, skin: "Skin") -> "Skin":
        self.skins[skin.id] = skin
        return skin

    def get_or_add_skin(self, skin: "Skin") -> "Skin":
        return self.skins.get(skin.id, skin)

    def reserve_skin(self, skin: "Skin") -> "Skin":
        return self.skins.reserve(skin.id, skin, int(skin.id))


    @classmethod
    def validate_id(cls, id: str) -> str:
        id = super().validate_id(id)

        if id not in cls.valid_ids:
            raise UnknownSkinRarityIDError(id)

        return id

    def __int__(self) -> int:
        return int(self.id)

    def __str__(self) -> str:
        return f"{int(self)}★"


__all__ = ["SkinRarity"]
