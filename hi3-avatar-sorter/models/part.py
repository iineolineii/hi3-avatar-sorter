from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from functools import lru_cache
from typing import TYPE_CHECKING, Any, ClassVar

from multidict import MultiDict

from .base import BaseModel
from .battlesuit import Battlesuit
from .valkyrie import MAX_BATTLESUIT_ID, Valkyrie
from ..errors import UnknownPartIDError, UnknownValkyrieIDError
from ..maps import RAW_PARTS_MAP
from ..utils import FrozenMultiDict

if TYPE_CHECKING:
    from ..enums import PartIDFormat, PartNumber


@dataclass(frozen=True, slots=True)
class Part(BaseModel):
    id: str = field(compare=False)
    no: "PartNumber" = field(init=True)
    id_format: "PartIDFormat"

    valkyries: "FrozenMultiDict[Valkyrie]" = field(init=False, repr=False)
    id_length: ClassVar[int] = 3

    @classmethod
    def validate_id(cls, id: str) -> str:
        id = BaseModel.validate_id.__func__(cls, id)

        if id not in RAW_PARTS_MAP:
            raise UnknownPartIDError(id)

        return id

    @lru_cache # Add caching according to NOTE#2
    def get_valkyrie(self, valkyrie_id: str, battlesuit_id: str) -> "Valkyrie":
        numeric_battlesuit_id = int(Battlesuit.validate_id(battlesuit_id))

        try:
            valkyries = self.valkyries.getall(valkyrie_id)
        except KeyError as e:
            raise UnknownValkyrieIDError(valkyrie_id, battlesuit_id, self.no) from e

        for valkyrie in valkyries:
            if numeric_battlesuit_id in valkyrie.battlesuit_id_range:
                return valkyrie

        raise UnknownValkyrieIDError(valkyrie_id, battlesuit_id, self.no)


    def build_valkyries_map(self, raw_valkyries: Iterable[tuple[str, str, int] | tuple[str, str]]) -> "FrozenMultiDict[Valkyrie]":
        """
        Build a read-only multi-mapping of Valkyrie IDs
        to their :class:`Valkyrie` instances,
        allowing multiple valkyries to share the same ID.

        :param raw_valkyries: The raw Valkyrie data. \
        Iterable of tuples containing Valkyrie's ID, \
        name, and, optionally, maximum :class:`Battlesuit` ID.
        :type raw_valkyries: Iterable[tuple[str, str, int] | tuple[str, str]]

        :return: Read-only multi-mapping of Valkyrie IDs to their :class:`Valkyrie` instances.
        :rtype: :class:`FrozenMultiDict` [:class:`Valkyrie`]
        """
        valkyrie_map: "MultiDict[Valkyrie]" = MultiDict()

        # Group Valkyries with the same ID
        for valkyrie in self._parse_raw_valkyries(raw_valkyries):
            valkyrie_map.add(valkyrie.id, valkyrie)

        object.__setattr__(self, "valkyries", FrozenMultiDict(valkyrie_map))
        return self.valkyries

    def _parse_raw_valkyries(self, raw_valkyries: Iterable[tuple[str, str, int] | tuple[str, str]]) -> "Iterator[Valkyrie]":
        """
        Yields :class:`Valkyrie` instances parsed from the raw Valkyrie data.

        Automatically chains the :class:`Battlesuit` ID ranges,
        allowing multiple Valkyries to share the same ID.

        :param raw_valkyries: The raw Valkyrie data. \
        Iterable of tuples containing Valkyrie's ID, \
        name, and, optionally, maximum :class:`Battlesuit` ID.
        :type raw_valkyries: Iterable[tuple[str, str, int] | tuple[str, str]]

        :return: Iterator yielding parsed :class:`Valkyrie` instances.
        :rtype: Iterator[:class:`Valkyrie`]
        """
        # For the same ID, every next range start is the previous end
        range_starts: dict[str, int] = {}

        for no, (id, name, *rest) in enumerate(raw_valkyries, start=1):
            # Use the previous end for the current ID or start from 0
            start = range_starts.get(id, 0)

            # Use the specified end or limit to the max Battlesuit ID
            end = rest[0] if rest else MAX_BATTLESUIT_ID

            yield Valkyrie(
                id=id, no=no, name=name,
                battlesuit_id_range=range(start, end)
            )

            # Current end will be the next start for the current ID
            range_starts[id] = end


    def __getattribute__(self, name: str) -> Any:
        try:
            return BaseModel.__getattribute__(self, name)

        except AttributeError:
            class_name = type(self).__name__
            base_message = f"{class_name!r} object has no attribute '{name}'. "

            if name == "no":
                raise AttributeError(
                    base_message +
                    f"Perhaps it was created without using the "
                    f"'build_part_map' factory method?"
                )

            if name == "valkyries":
                raise AttributeError(
                    base_message +
                    f"Perhaps you forgot to call "
                    f"'build_valkyrie_map' method?"
                )

            raise


__all__ = ["Part"]
