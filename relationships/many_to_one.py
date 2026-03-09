from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, TypeVar

from ..models import Battlesuit, Part, SkinRarity

if TYPE_CHECKING:
    from ..models import Valkyrie

ParentT = TypeVar("ParentT", bound="Part | Valkyrie | Battlesuit | SkinRarity")


@dataclass
class ManyToOne(Generic[ParentT]):
    code: int
    no: int = field(init=False)
