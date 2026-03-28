from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from typing_extensions import deprecated

from .base import BaseModel
from ..errors import EmptyReservationNoError, MissingChildrenAttributeError

if TYPE_CHECKING:
    from .base import NonUniqueIdModel

Child = TypeVar("Child", bound="BaseModel")


@dataclass(kw_only=True)
class Container(Generic[Child], BaseModel):
    _children:      dict[str, "Child"] = field(init=False)

    _children_accessor_name: set[int] = field(init=False, default_factory=set)
    _current_mex:            int      = field(init=False, default=1)
    _children_attr_name:     ClassVar[str]

    def __post_init__(self):
        super().__post_init__()
        self._add_children_attr()

    def __init_subclass__(cls, has_children_attribute: bool = True):
        super().__init_subclass__()

        if has_children_attribute:
            # Find attribute annotated with frozendict
            for name, annotation in cls.__annotations__.items():
                if str(annotation).startswith("frozendict"):
                    cls._children_attr_name = name
                    break
            else:
                raise MissingChildrenAttributeError(cls.__name__)

    def _add_children_attr(self):
        # Get the name of the attribute used by subclasses for storage
        target_attr_name = self._children_attr_name

        # Extract the initial data
        initial_children = getattr(self, target_attr_name)

        # Initialize the unified mutable container
        self._children = dict(initial_children)

        # Replace the target attribute with the new unified container
        setattr(self, target_attr_name, self._children)

    def _add_child(self, child: "Child") -> "Child":
        mex = self._get_mex()
        child.no = mex
        self._children[child.id] = child
        return child

    def _get_child(self, child_id: str) -> "Child | None":
        try:
            return self._children[child_id]
        except KeyError:
            return None

    def _get_mex(self) -> int:
        mex = self._current_mex
        self._children_accessor_name.add(mex)
        self._update_mex()
        return mex

    def _update_mex(self) -> None:
        while self._current_mex in self._children_accessor_name:
            self._current_mex += 1

    def _reserve_child(self, child: "Child") -> "Child":
        if child.no is None:
            raise EmptyReservationNoError(type(child).__name__, child.id)

        self._current_mex = child.no
        self._update_mex()
        self._children[child.id] = child
        return child

    def _get_or_add_child(self, child: "Child") -> "Child":
        return self._get_child(child.id) or self._add_child(child)


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
        target_attr_name = self._children_attr_name

        # Extract the initial data
        initial_children = getattr(self, target_attr_name)

        # Initialize the unified mutable container
        # for multiple children with the same ID
        self._children = defaultdict(list, initial_children) # pyright: ignore[reportIncompatibleVariableOverride]

        # Replace the target attribute with the new unified container
        setattr(self, target_attr_name, self._children)

    @deprecated(
        "Using _get_or_add_child is not available for non-unique ID containers. "
        "Use _get_child instead"
    )
    def _get_or_add_child(self, child: "NonUniqueIdChild") -> NonUniqueIdChild:
        raise NotImplementedError

    def _get_child(self, child_id: str, grandchild_id: str) -> "NonUniqueIdChild | None": # pyright: ignore[reportIncompatibleMethodOverride]
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
        self._children_accessor_name.add(mex)
        self._update_mex()
        return mex

    def _update_mex(self) -> None:
        while self._current_mex in self._children_accessor_name:
            self._current_mex += 1

    def _reserve_child(self, child: "NonUniqueIdChild") -> "NonUniqueIdChild":
        if child.no is None:
            raise EmptyReservationNoError(type(child).__name__, child.id)

        self._current_mex = child.no
        self._update_mex()
        self._children[child.id].append(child)
        return child


__all__ = ["Container", "NonUniqueIdContainer"]
