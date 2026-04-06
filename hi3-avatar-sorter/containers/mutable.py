from collections.abc import Mapping
from typing import TYPE_CHECKING, Generic

from .mex import MexContainer
from ..errors import MissingReservationAttributeError

if TYPE_CHECKING:
   from . import K, V


class MutableContainer(Generic["K", "V"], MexContainer["K", "V"], dict["K", "V"]):
    """
    A mutable implementation of the MEX container allowing value assignment.
    """

    def __init__(
        self,
        map: dict["K", "V"] = {},
        mex_attr_name: str = "no"
    ) -> None:
        """
        Args:
            map (`dict["K", "V"]`):
                Initial container data. Defaults to an empty dictionary.
                All values passed here will be reserved via the `reserve()` method.
                Each of these values must have an attribute with the specified in `mex_attr_name` argument.

            mex_attr_name (`str`):
                Name of the values' attribute used as a MEX. Defaults to `"no"`.
        """
        super().__init__(map, mex_attr_name)
        self.reserve_map(self.map)

    def reserve_map(self, map: Mapping["K", "V"]) -> None:
        """
        Reserve all entries of a given mapping.
        """
        for key, value in map.items():
            mex = getattr(value, self.mex_attr_name)
            self.reserve(key, value, mex)

    def reserve(self, key: "K", value: "V", mex: int = ...) -> "V": # pyright: ignore[reportArgumentType]
        """
        Reserve a value with a predefined MEX.

        Args:
            key (`K`):
                Key to insert.

            value (`V`):
                Value to store.

            mex (`int`):
                Predefined MEX. Defaults to `getattr(value, self.mex_attr_name)` (which defaults to `value.no`)

        Returns:
            `V`: The inserted value.
        """
        if mex is ...:
            if getattr(value, self.mex_attr_name, None) is None:
                raise MissingReservationAttributeError(key, type(value).__name__)

            mex = getattr(value, self.mex_attr_name)

        self.current_mex = mex
        self.update_mex()
        self[key] = value

        return value

    def get(self, key: "K", default: "V") -> "V":  # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Get a value by key, or set it to `default` if missing.

        Args:
            key (`K`):
                The key to look up.

            default (`V`):
                The value to set and return if the key is missing.

        Returns:
            `V`: The existing or newly set value.
        """
        if key not in self:
            self[key] = default

        return self[key]

    def __setitem__(self, key: "K", value: "V") -> "V":
        mex = self.consume_mex()
        setattr(value, self.mex_attr_name, mex)
        self.map[key] = value

        return value


__all__ = ["MutableContainer"]
