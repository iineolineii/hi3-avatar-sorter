from collections.abc import Iterable
from enum import Enum

from .enums import PartIDFormat
from .models import Part, Valkyrie


FORMAT_BY_FOLDER: dict[Iterable[str], PartIDFormat] = {
    (
        "avatarchibiicons",
        "avataritemicon",
        "avataricon",
        "dressicons",
        "avatardressicon",
        "avatariconside",
        "dressfigures"
    ): PartIDFormat.ICON,
    (
        "avatarcardfigures",
        "avatarcardicons"
    ): PartIDFormat.SPLASH,
    (
        "avatarfragmentfigures",
        "avatarfragmenticons"
    ): PartIDFormat.FRAGMENT
}
