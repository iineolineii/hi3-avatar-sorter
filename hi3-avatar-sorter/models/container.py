from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass, field
from typing import ClassVar
from warnings import deprecated

from ..errors import EmptyReservationNoError, MissingChildrenAttributeError

from .base import BaseModel, NonUniqueIdModel
from ..utils import evaluate_type_argument


@dataclass(kw_only=True)
class Container[Child: "BaseModel"](BaseModel):
    _children_type: type["Child"]      = field(init=False)
    _children:      dict[str, "Child"] = field(init=False)

    __children_numbers: set[int] = field(init=False, default_factory=set)
    __current_mex:      int      = field(init=False, default=1)
    __children_attr:    ClassVar[str]

    def __post_init__(self):
        super().__post_init__() # pyright: ignore[reportAttributeAccessIssue]
        self._rename_children_attr()

    def __init_subclass__(cls, evaluate_children_type: bool = True):
        super().__init_subclass__()

        if evaluate_children_type:
            # Find attribute annotated with frozendict
            for name, annotation in cls.__annotations__.items():
                if str(annotation).startswith("frozendict"):
                    cls.__children_attr = name
                    break
            else:
                raise MissingChildrenAttributeError(cls.__name__)

            cls._children_type = evaluate_type_argument(cls, Container)

    def _rename_children_attr(self):
        # Copy named frozendict children to the mutable defaultdict
        self._children = defaultdict(getattr(self, self.__children_attr))
        setattr(self, self.__children_attr, self._children)

    def _add_child(self, child: "Child") -> "Child":
        mex = self._get_mex()
        child.no = mex
        self._children[child.id] = child
        return child

    def _get_mex(self) -> int:
        mex = self.__current_mex
        self.__children_numbers.add(mex)
        self._update_mex()
        return mex

    def _update_mex(self) -> None:
        while self.__current_mex in self.__children_numbers:
            self.__current_mex += 1

    def _reserve_child(self, child: "Child") -> "Child":
        if child.no is None:
            raise EmptyReservationNoError(type(child).__name__, child.id)

        self.__current_mex = child.no
        self._update_mex()
        self._children[child.id] = child
        return child

    def _get_or_create_child(self, child_id: str) -> "Child":
        try:
            return self._children[child_id]
        except KeyError:
            return self._children_type(id=child_id)


@dataclass(kw_only=True)
class NonUniqueIdContainer[Child: "NonUniqueIdModel"](Container[Child], evaluate_children_type=False):
    _children: defaultdict[str, list["Child"]] = field(init=False) # pyright: ignore[reportIncompatibleVariableOverride]

    def __init_subclass__(cls, evaluate_children_type: bool = True):
        super().__init_subclass__(evaluate_children_type=False)

        if evaluate_children_type:
            cls._children_type = evaluate_type_argument(cls, NonUniqueIdContainer)

    @deprecated(
        "Using _get_or_create_child is not available for non-unique ID containers. "
        "Use _get_child instead"
    )
    def _get_or_create_child(self, child_id: str) -> Child:
        raise NotImplementedError

    def _get_child(self, child_id: str, grandchild_id: str) -> "Child | None": # pyright: ignore[reportIncompatibleMethodOverride]
        with suppress(KeyError):
            found = self._children[child_id]

            for child in found:
                if int(grandchild_id) in child.children_id_range:
                    return child

    def _add_child(self, child: "Child") -> "Child":
        mex = self._get_mex()
        child.no = mex
        self._children[child.id].append(child)
        return child

    def _get_mex(self) -> int:
        mex = self.__current_mex
        self.__children_numbers.add(mex)
        self._update_mex()
        return mex

    def _update_mex(self) -> None:
        while self.__current_mex in self.__children_numbers:
            self.__current_mex += 1

    def _reserve_child(self, child: "Child") -> "Child":
        if child.no is None:
            raise EmptyReservationNoError(type(child).__name__, child.id)

        self.__current_mex = child.no
        self._update_mex()
        self._children[child.id].append(child)
        return child
