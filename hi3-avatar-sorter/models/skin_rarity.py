from typing import TYPE_CHECKING

from . import BaseModel
from ..mixins import HasChildren
from ..utils import capitalize

if TYPE_CHECKING:
    from . import Skin


class SkinRarity(BaseModel, HasChildren["Skin"]):
    valid_ids = {"02", "03", "04"}

    def __int__(self) -> int:
        return int(self.id)

    def __str__(self) -> str:
        return f"{capitalize(type(self).__name__)} {int(self)}★"


__all__ = ["SkinRarity"]
