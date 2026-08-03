from typing import TYPE_CHECKING, ClassVar

from . import BaseModel
from ..enums import PartIDFormat
from ..mixins import HasChildren

if TYPE_CHECKING:
    from . import Valkyrie


class Part(BaseModel, HasChildren["Valkyrie"]):
    no: int
    id_format: "PartIDFormat"

    id_length: ClassVar[int] = 3
    valid_ids: ClassVar[set[str]] = {"000", "002", "006", "302", "062", "001", "202"}

    def __hash__(self) -> int:
        return hash(self.id)


__all__ = ["Part"]
