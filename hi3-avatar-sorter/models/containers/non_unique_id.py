from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from typing_extensions import deprecated

from .base import Container
from ..base import NonUniqueIdModel
from ...errors import EmptyReservationNoError

NonUniqueIdChild = TypeVar("NonUniqueIdChild", bound="NonUniqueIdModel")


@dataclass(kw_only=True)
class NonUniqueIdContainer(
    Generic[NonUniqueIdChild],
    Container[NonUniqueIdChild],
    has_children_attribute=False
):
    _children: defaultdict[str, list["NonUniqueIdChild"]] = field(init=False)

    def __init_subclass__(cls):
        super().__init_subclass__(has_children_attribute=True)

    def _add_children_attr(self):
        # Get the name of the attribute used by subclasses for storage
        target_attr_name = self._children_accessor_name

        # Extract the initial data
        initial_children = getattr(self, target_attr_name)

        # Initialize the unified mutable container
        # for multiple children with the same ID
        self._children = defaultdict(list, initial_children)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Replace the target attribute with the new unified container
        setattr(self, target_attr_name, self._children)

    @deprecated(
        "Using _get_or_add_child is not available for non-unique ID containers. "
        "Use _get_child instead"
    )
    def _get_or_add_child(self, child: "NonUniqueIdChild") -> NonUniqueIdChild:
        raise NotImplementedError

    def _get_child( # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        child_id: str,
        grandchild_id: str
    ) -> "NonUniqueIdChild | None":
        with suppress(KeyError):
            found = self._children[child_id]

            for child in found:
                if int(grandchild_id) in child.children_id_range:
                    return child

    def _add_child(self, child: "NonUniqueIdChild") -> "NonUniqueIdChild":
        mex = self._get_mex()
        child.no = mex
        self._children[child.id].append(child)
        return child

    def _get_mex(self) -> int:
        mex = self._current_mex
        self._children_numbers.add(mex)
        self._update_mex()
        return mex

    def _update_mex(self) -> None:
        while self._current_mex in self._children_numbers:
            self._current_mex += 1

    def _reserve_child(self, child: "NonUniqueIdChild") -> "NonUniqueIdChild":
        if child.no is None:
            raise EmptyReservationNoError(type(child).__name__, child.id)

        self._current_mex = child.no
        self._update_mex()
        self._children[child.id].append(child)
        return child


__all__ = ["NonUniqueIdContainer"]
