from dataclasses import dataclass
from typing import ClassVar, Generic

from .base import Child, Container
from ...errors import MissingChildrenAttributeError


@dataclass(kw_only=True)
class ClassContainer(
    Generic[Child],
    Container[Child],
    has_children_attribute=False
):
    _children: ClassVar[dict[str, "Child"]] # pyright: ignore[reportIncompatibleVariableOverride, reportGeneralTypeIssues]
    _children_numbers: ClassVar[set[int]]
    _current_mex: ClassVar[int] = 1 # pyright: ignore[reportIncompatibleVariableOverride]

    def __init_subclass__(cls, has_children_attribute: bool = True):
        if not hasattr(cls, "_children_numbers"):
            cls._children_numbers = set() # pyright: ignore[reportIncompatibleVariableOverride]

        super().__init_subclass__()

        if has_children_attribute:
            # Find attribute annotated with frozendict
            for name, annotation in cls.__annotations__.items():
                if str(annotation).startswith("ClassVar[frozendict"):
                    cls._children_accessor_name = name
                    break
            else:
                raise MissingChildrenAttributeError(cls.__name__)


    @classmethod
    def _add_children_attr(cls): # pyright: ignore[reportIncompatibleMethodOverride]
        return super()._add_children_attr(cls) # pyright: ignore[reportArgumentType]

    @classmethod
    def _add_child(cls, child: "Child") -> "Child": # pyright: ignore[reportIncompatibleMethodOverride]
        return super()._add_child(cls, child) # pyright: ignore[reportArgumentType]

    @classmethod
    def _get_child(cls, child_id: str) -> "Child | None": # pyright: ignore[reportIncompatibleMethodOverride]
        return super()._get_child(cls, child_id) # pyright: ignore[reportArgumentType]

    @classmethod
    def _get_mex(cls) -> int: # pyright: ignore[reportIncompatibleMethodOverride]
        return super()._get_mex(cls) # pyright: ignore[reportArgumentType]

    @classmethod
    def _update_mex(cls) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        return super()._update_mex(cls) # pyright: ignore[reportArgumentType]

    @classmethod
    def _reserve_child(cls, child: "Child") -> "Child": # pyright: ignore[reportIncompatibleMethodOverride]
        return super()._reserve_child(cls, child) # pyright: ignore[reportArgumentType]

    @classmethod
    def _get_or_add_child(cls, child: "Child") -> "Child": # pyright: ignore[reportIncompatibleMethodOverride]
        return super()._get_or_add_child(cls, child) # pyright: ignore[reportArgumentType]


__all__ = ["ClassContainer"]
