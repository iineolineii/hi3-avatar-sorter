from collections.abc import Iterable
from typing import TYPE_CHECKING

from ..fixers import AvatarFixer
from ..fixers.maps import (
    EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP,
    TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP,
    TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP,
    WRONG_ID_REPLACEMENT_MAP
)

if TYPE_CHECKING:
    from ..enums import PartIDFormat
    from ..models.avatar import RawAvatar


def fix_avatar_string(avatar_string: str, fixers: Iterable["AvatarFixer"]) -> "RawAvatar | None":
    avatar_string = avatar_string.lower()

    # Each input is allowed to pass through only one mechanism.
    # The first successful fix wins, so the same string is never rewritten twice.
    for fixer in fixers:
        if fixed_string := fixer.fix(avatar_string):
            return fixed_string


def build_fixers(part_id_format: "PartIDFormat") -> dict[str, "AvatarFixer"]:
    """
    Build a dictionary mapping fix names to their :class:`AvatarFixer` instances.

    :param part_id_format: Part ID format passed to :class:`AvatarFixer`.
    :type part_id_format: :class:`PartIDFormat`

    :return: Dictionary mapping fix names to their :class:`AvatarFixer` instances.
    :rtype: dict[str, AvatarFixer]
    """
    fixers: dict[str, "AvatarFixer"] = {}

    # Exact replacements
    fixers["empty Battlesuit ID"]     = AvatarFixer(part_id_format, EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP)
    fixers["too short Battlesuit ID"] = AvatarFixer(part_id_format, TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP)
    fixers["too short Valkyrie ID"]   = AvatarFixer(part_id_format, TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP)

    # Prefix replacements
    fixers["wrong ID"] = AvatarFixer(part_id_format, WRONG_ID_REPLACEMENT_MAP)

    return fixers


__all__ = ["fix_avatar_string"]
