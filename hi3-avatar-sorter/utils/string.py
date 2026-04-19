from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fixers import AvatarFixer
    from ..models.avatar import RawAvatar


def fix_avatar_string(avatar_string: str, fixers: Iterable["AvatarFixer"]) -> "RawAvatar | None":
    avatar_string = avatar_string.lower()

    # Each input is allowed to pass through only one mechanism.
    # The first successful fix wins, so the same string is never rewritten twice.
    for fixer in fixers:
        if fixed_string := fixer.fix(avatar_string):
            return fixed_string


__all__ = ["fix_avatar_string"]
