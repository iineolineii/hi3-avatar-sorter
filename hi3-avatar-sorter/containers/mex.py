from abc import ABCMeta
from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING, Generic

if TYPE_CHECKING:
   from . import K, V


class MexContainer(Generic["K", "V"], Mapping["K", "V"], metaclass=ABCMeta):
    """
    Base container that stores values based on their MEX (minimal excluded number).
    """

    def __init__(self, map: dict["K", "V"] = {}, mex_attr_name: str = "no") -> None:
        """
        Args:
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

    def __getitem__(self, key: "K") -> "V":
        return self.map[key]

    def __len__(self) -> int:
        return len(self.map)

    def __iter__(self) -> Iterator["K"]:
        return iter(self.map)


__all__ = ["MexContainer"]
