from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import ClassVar

from .base import BaseModel
from .skin import Skin
from ..errors import UnknownSkinRarityIDError
from ..utils import MexContainer, capitalize, mex_field


@dataclass(frozen=True, slots=True)
class SkinRarity(BaseModel):
    skins: "MexContainer[str, Skin]" = mex_field()
    valid_ids: ClassVar[Iterable[str]] = ("02", "03", "04", "05")

    def add_skin(self, skin: "Skin") -> "Skin":
        self.skins[skin.id] = skin
        return skin

    def get_or_add_skin(self, skin: "Skin") -> "Skin":
        return self.skins.setdefault(skin.id, skin)


    @classmethod
    def validate_id(cls, id: str) -> str:
        id = BaseModel.validate_id.__func__(cls, id)

        if id not in cls.valid_ids:
            raise UnknownSkinRarityIDError(id)

        return id

    def __int__(self) -> int:
        return int(self.id)

    def __str__(self) -> str:
        return f"{capitalize(type(self).__name__)} {int(self)}★"


__all__ = ["SkinRarity"]
