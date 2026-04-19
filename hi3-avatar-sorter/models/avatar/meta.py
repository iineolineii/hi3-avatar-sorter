from abc import ABCMeta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Avatar


class AvatarMeta(ABCMeta):
    def __getattribute__(cls: "Avatar", name: str): # pyright: ignore[reportGeneralTypeIssues]
        try:
            return super().__getattribute__(name)

        except AttributeError:
            class_name = cls.__name__
            base_message = f"type object {class_name!r} has no attribute '{name!r}'."

            if name == "parts":
                raise AttributeError(
                    base_message +
                    f" Perhaps you forgot to call the "
                    f"{cls.build_part_map.__qualname__!r} method?"
                )

            raise


__all__ = ["AvatarMeta"]
