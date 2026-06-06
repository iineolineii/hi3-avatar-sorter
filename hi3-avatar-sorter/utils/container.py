from abc import ABCMeta
from collections import UserDict
from collections.abc import Hashable
from dataclasses import field
from typing import Generic, TypeVar

from multidict import MultiDict, MultiDictProxy


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class FrozenMultiDict(Generic[V], MultiDictProxy[V]):
    def __init__(self, arg: MultiDict[V] | MultiDictProxy[V]):
        super().__init__(arg.copy())
        self._hash = hash(frozenset(self.items()))

    def __hash__(self) -> int:
        return self._hash


class MexContainer(Generic[K, V], UserDict["K", "V"], metaclass=ABCMeta):
    """
    Base container that stores values based on their MEX (minimal excluded number).
    """

    def __init__(
        self,
        map: dict["K", "V"] = {},
        attr_name: str = "no",
        start: int = 1
    ) -> None:
        """
        Args:
            map (`dict["K", "V"]`):
                Initial container data. Defaults to an empty dictionary.
                All values passed here will be reserved via the `reserve()` method.
                Each of these values must have an attribute with the specified in `attr_name` argument.

            attr_name (`str`):
                Name of the values' attribute used as a MEX. Defaults to `"no"`.
        """
        super().__init__()

        self.attr_name = attr_name
        """
        attr_name (`str`):
            Name of the values' attribute used as a MEX. Defaults to `"no"`.
        """
        self.map: dict["K", "V"] = map
        """
        map (`dict["K", "V"]`):
            Internal container.
        """
        self.update(self.map)
        self.consumed_mexes: set[int] = set()
        self.current_mex = start

    def consume_mex(self) -> int:
        """
        Mark current MEX as consumed.

        Returns:
            `int`: The current MEX value.
        """
        mex = self.current_mex
        self.consumed_mexes.add(mex)
        self.update_mex()

        return mex

    def update_mex(self) -> None:
        """
        Increments `current_mex` until it is no longer present in `consumed_mexes`.
        """
        while self.current_mex in self.consumed_mexes:
            self.current_mex += 1

    def setdefault(self, key: "K", default: "V") -> "V": # pyright: ignore[reportIncompatibleMethodOverride]
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

    def __setitem__(self, key: "K", value: "V") -> None:
        mex = self.consume_mex()
        object.__setattr__(value, self.attr_name, mex)

        return super().__setitem__(key, value)

mex_field = lambda *args, **kwargs: field(
    *args,
    **(kwargs | {
        "default_factory": MexContainer,
        "repr": False,
        "hash": False
    })
)


__all__ = ["FrozenMultiDict", "MexContainer", "mex_field"]
