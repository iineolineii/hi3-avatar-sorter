from dataclasses import dataclass, field

from . import AvatarFixer
from ..errors import MissingFieldError
from ..models import RawAvatar


@dataclass(frozen=True)
class PrefixFixer(AvatarFixer):
    _replacement_items: list[tuple[str, RawAvatar]] = field(init=False, repr=False, default_factory=list)

    def __post_init__(self) -> None:
        AvatarFixer.__post_init__(self)
        replacement_items = sorted(
            self.replacement_map.items(),
            key=lambda malformed_prefix: len(malformed_prefix[0]),
            reverse=True
        )
        object.__setattr__(self, "_replacement_items", replacement_items)

    def fix(self, avatar_string: str) -> RawAvatar | None:
        for malformed_prefix, fixed_dto in self._replacement_items:
            if avatar_string.startswith(malformed_prefix):
                valid_suffix = avatar_string[len(malformed_prefix):]
                fixed_string = str(fixed_dto) + valid_suffix

                return RawAvatar.from_string(fixed_string)

        return None


__all__ = ["PrefixFixer"]
