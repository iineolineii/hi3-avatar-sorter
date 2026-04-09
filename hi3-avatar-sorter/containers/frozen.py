from typing import TYPE_CHECKING, Generic

from .mex import MexContainer
from .mutable import MutableContainer

if TYPE_CHECKING:
   from . import K, V


class FrozenContainer(Generic["K", "V"], MexContainer["K", "V"]):
    """
    An immutable implementation of the MEX container that locks its state after initialization.

    Warning:
        - `__mutable_attrs`, `__unfreeze`, and `__freeze` are internal hacks.
          They are used only to temporarily enable mutation during initialization
          for reserving predefined values. Their direct use is strongly discouraged.
        - `__freeze` does NOT check whether attributes from `__mutable_attrs`
          exist on the object. It must only be used after `__unfreeze`, an equivalent
          mechanism, or an external guarantee that those attributes are present.

    Note:
        All values passed during initialization via `map` are reserved using `.reserve()`.
    """

    def __init__(
        self,
        map: dict["K", "V"],
        mex_attr_name: str = "no"
    ) -> None:
        """
        Args:
            map (`dict["K", "V"]`):
                Initial container data.
                All values passed here will be reserved via the `reserve()` method.
                Each of these values must have an attribute with the specified in `mex_attr_name` argument.

            mex_attr_name (`str`, *optional*):
                Name of the values' attribute used as a MEX. Defaults to `"no"`.
        """
        super().__init__(map, mex_attr_name)

        self.__unfreeze()
        MutableContainer.reserve_map(self, map)  # pyright: ignore[reportArgumentType]
        self.__freeze()

    __mutable_attrs = ["reserve", "__setitem__"]

    def __unfreeze(self) -> None:
        """
        Temporarily enable mutation methods for initialization.

        Warning:
            This is an **internal hack** used only for reserving pre-defined values \
            during initialization; it's direct **usage is not recommended**.
        """
        for attr in self.__mutable_attrs:
            setattr(type(self), attr, getattr(MutableContainer, attr))

    def __freeze(self) -> None:
        """
        Remove mutation methods to enforce immutability.

        Warning:
            This is an **internal hack** used only for reserving pre-defined values \
            during initialization; it's direct **usage is not recommended**. \
            This method does NOT check for the presence of attributes \
            from `__mutable_attrs` and must be used only after `__unfreeze`, \
            its counterpart, or an external check.
        """
        for attr in self.__mutable_attrs:
            delattr(type(self), attr)


__all__ = ["FrozenContainer"]
