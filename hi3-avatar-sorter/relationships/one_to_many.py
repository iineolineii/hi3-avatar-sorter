from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

if TYPE_CHECKING:
    from .many_to_one import ManyToOne


ChildT = TypeVar("ChildT", bound="ManyToOne")

@dataclass(kw_only=True)
class OneToMany(Generic[ChildT]):
    _children:   dict[str, ChildT] = field(init=False, default_factory=dict, hash=False)
    __children_attr: ClassVar[str] = field(init=False, hash=False)

    __children_numbers: set[int] = field(init=False, default_factory=set, hash=False)
    __mex_child_number:      int = field(init=False, default=1, hash=False)
    __max_reserved_number:   int = field(init=False, default=0, hash=False)

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # Find attribute annotated with frozendict
        for name, annotation in cls.__annotations__.items():
            if str(annotation).startswith("frozendict"):
                cls.__children_attr = name
                break
        else:
            raise TypeError(f"Class {cls.__name__!r} must have a frozendict field for storing children")

    def __post_init__(self) -> None:
        # Copy named frozendict children to the common mutable dict
        self._children = dict(getattr(self, self.__children_attr))
        setattr(self, self.__children_attr, self._children)

        # Make initial child numbers reserved
        if self._children:
            for child in self._children.values():
                self.__children_numbers.add(child.no)
                self._update_mex(child.no)

            self.__max_reserved_number = max(self.__children_numbers)

    def _add_child(self, child: ChildT) -> ChildT:
        # Switch method to lazy if no spaces between child numbers are left
        if len(self._children) >= self.__max_reserved_number:
            self._add_child = self._add_child_lazy
            return self._add_child_lazy(child)

        return self._add_child_mex(child)

    def _add_child_mex(self, child: ChildT) -> ChildT:
        child.no = getattr(child, "no", self.__mex_child_number)
        self.__children_numbers.add(child.no)
        self._update_mex(child.no)
        self._children[child.id] = child
        return child

    def _add_child_lazy(self, child: ChildT) -> ChildT:
        child.no = getattr(child, "no", len(self._children) + 1)
        self._children[child.id] = child
        return child

    def _update_mex(self, child_no: int) -> None:
        if child_no == self.__mex_child_number:
            while self.__mex_child_number in self.__children_numbers:
                self.__mex_child_number += 1
