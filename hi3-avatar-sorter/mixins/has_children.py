from collections.abc import Collection, Iterator
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from ..errors import DuplicateChildNumberError, InvalidChildNumberError
from ..models.base import MISSING, BaseModel

ChildT = TypeVar("ChildT", bound="BaseModel")


@dataclass(frozen=True)
class HasChildren(Generic[ChildT], Collection[ChildT]):
    """
    Mutable collection of child models indexed by their numbers (`child.no` attribute).
    """

    _children_map: dict[int, ChildT] = field(
        init=False,
        default_factory=dict,
        repr=False,
        compare=False
    )

    def add_child(self, child: ChildT, exists_ok: bool = False) -> ChildT:
        """
        Updates the child's number (`child.no` attribute)
        and stores it in the collection under the assigned value.

        - If `child.no is MISSING`, sets it to the minimal unused number.
        - If `child.no <= 0` or `child.no` is not an integer, raises :class:`InvalidChildNumberError`.
        - If `child.no` is already occupied and `exists_ok` is not `True`, raises :class:`DuplicateChildNumberError`.
        - Otherwise, leaves `child.no` unchanged.

        :param child: The child to update and store.
        :type child: :class:`ChildT`

        :return: The updated and stored children.
        :rtype: :class:`ChildT`

        :raises :class:`InvalidChildNumberError`: If `child.no` is not positive.

        :raises :class:`DuplicateChildNumberError`: If `child.no` is already occupied.
        """
        if child.no is MISSING:
            object.__setattr__(child, "no", self._get_mex())

        try:
            self[child.no] = child

        except DuplicateChildNumberError:
            if not exists_ok:
                raise

        return child

    def _get_mex(self) -> int:
        """
        Return the minimal unused child number starting from 1.
        """
        child_no = 1
        while child_no in self._children_map:
            child_no += 1

        return child_no

    def __setitem__(self, child_no: int, child: ChildT, /) -> None:
        """
        Validate the provided `child_no` and store the `child` under it.

        :param child_no: The number to store under.
        :type child_no: int

        :param child: The child to store.
        :type child: :class:`ChildT`

        :raises :class:`InvalidChildNumberError`: If `child_no` is not positive.

        :raises :class:`DuplicateChildNumberError`: If `child_no` is already occupied.
        """
        class_name = type(self).__name__

        if not isinstance(child_no, int) and child_no <= 0:
            raise InvalidChildNumberError(class_name, child_no)

        if child_no in self._children_map:
            raise DuplicateChildNumberError(class_name, child_no)

        child._update_no(child_no)
        self._children_map[child_no] = child

    def __iter__(self) -> Iterator[ChildT]:
        """
        Iterate over stored children following the insertion order.
        """
        yield from self._children_map.values()

    def __len__(self) -> int:
        """
        Return the number of the currently stored children.
        """
        return len(self._children_map)

    def __contains__(self, child: ChildT, /) -> bool:
        """
        Check if a child with the same `no` is stored already.
        """
        if not isinstance(child, BaseModel):
            return False

        return child.no in self._children_map


__all__ = ["HasChildren"]
