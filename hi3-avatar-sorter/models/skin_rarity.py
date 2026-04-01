import sys
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import ClassVar

from .containers import Container
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

    valid_ids: ClassVar[Iterable[str]] = ("02", "03", "04", "05")

    @classmethod
    def validate_id(cls, id: str) -> str:
        id = super().validate_id(id)

        if id not in cls.valid_ids:
            raise UnknownSkinRarityIdError(id)

        return id

    def reserve_skin(self, skin: "Skin") -> "Skin":
        return self._reserve_child(skin)

    def get_or_add_skin(self, skin: "Skin") -> "Skin":
        return self._get_or_add_child(skin)

    def __int__(self) -> int:
        return int(self.id)

    def __str__(self) -> str:
        return f"{int(self)}★"


__all__ = ["SkinRarity"]
