from abc import ABCMeta
from collections.abc import Hashable, Iterator, Mapping
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class MexContainer(Generic["K", "V"], Mapping["K", "V"], metaclass=ABCMeta):
    """
    Base container that stores values based on their MEX (minimal excluded number).
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
        super().__init__()

        self.mex_attr_name = mex_attr_name
        """
        mex_attr_name (`str`):
            Name of the values' attribute used as a MEX. Defaults to `"no"`.
        """
        self.map: dict["K", "V"] = map
        """
        map (`dict["K", "V"]`):
            Internal container.
        """
        self.reserve_map(self.map)
        self.consumed_mexes: set[int] = set()
        self.current_mex = 0

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

    def reserve_map(self, map: Mapping["K", "V"]) -> None:
        """
        Reserve all entries of a given mapping.
        """
        for key, value in map.items():
            mex = getattr(value, self.mex_attr_name)
            self.reserve(key, value, mex)

    def reserve(self, key: "K", value: "V", mex: int) -> "V": # pyright: ignore[reportArgumentType]
        """
        Reserve a value with a predefined MEX.

        Args:
            key (`K`):
                Key to insert.

            value (`V`):
                Value to store.

            mex (`int`):
                Predefined MEX.

        Returns:
            `V`: The inserted value.
        """
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

    def __setitem__(self, key: "K", value: "V") -> None:
        mex = self.consume_mex()
        setattr(value, self.mex_attr_name, mex)
        self.map[key] = value

    def __getitem__(self, key: "K") -> "V":
        return self.map[key]

    def __len__(self) -> int:
        return len(self.map)

    def __iter__(self) -> Iterator["K"]:
        return iter(self.map)


__all__ = ["MexContainer"]
