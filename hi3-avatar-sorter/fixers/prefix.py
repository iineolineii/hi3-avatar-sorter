from dataclasses import dataclass, field

from .avatar import AvatarFixer
from ..models.avatar import RawAvatar


@dataclass(frozen=True, slots=True)
class PrefixFixer(AvatarFixer):
    _replacement_items: list[tuple[str, RawAvatar]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        prefix_items = sorted(
            self.replacement_map.items(),
            key=lambda item: len(item[0]),
            reverse=True
        )
        object.__setattr__(self, "_prefix_items", prefix_items)

    def fix(self, avatar_string: str) -> RawAvatar | None:
        for malformed_prefix, fixed_dto in self._replacement_items:
            if avatar_string.startswith(malformed_prefix):
                fixed_string = str(fixed_dto) + avatar_string[len(malformed_prefix) :]
                return RawAvatar.from_string(fixed_string)

        return None


__all__ = ["PrefixFixer"]
