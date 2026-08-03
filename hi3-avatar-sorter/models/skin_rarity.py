from collections.abc import Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from .base import BaseModel
from ..errors import UnknownSkinRarityIDError
from ..mixins import HasChildren
from ..utils import capitalize

if TYPE_CHECKING:
    from . import Skin


@dataclass(frozen=True, slots=True)
class SkinRarity(BaseModel, HasChildren["Skin"]):
    valid_ids: ClassVar[Iterable[str]] = ("02", "03", "04", "05")

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
