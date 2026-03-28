import sys
from dataclasses import dataclass, field

from .container import Container
from .skin import Skin
from ..errors import UnknownSkinRarityIdError

if sys.version_info <= (3, 15):
    from frozendict import frozendict


@dataclass(kw_only=True)
class SkinRarity(Container[Skin]):
    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__post_init__
    skins: "frozendict[str, Skin]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_skin` method
    """

    @classmethod
    def _validate_id(cls, id: str) -> str:
        if id not in VALID_IDS:
            raise UnknownSkinRarityIdError(id)

        return id

    def add_skin(self, skin: "Skin") -> "Skin":
        return self._add_child(skin)

    def reserve_skin(self, skin: "Skin") -> "Skin":
        return self._reserve_child(skin)

    def get_or_create_skin(self, skin_id: str) -> "Skin":
        return self._get_or_create_child(skin_id)

    def __int__(self) -> int:
        return int(self.id)

    def __str__(self) -> str:
        return f"{int(self)}★"


VALID_IDS = ("02", "03", "04", "05")
