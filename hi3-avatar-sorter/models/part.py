from collections.abc import Iterable, Iterator
from dataclasses import field
from typing import TYPE_CHECKING, ClassVar

from .base import BaseModel
from .valkyrie import MAX_BATTLESUIT_ID, Valkyrie
from ..errors import UnknownPartIDError
from ..maps import RAW_PARTS_MAP
from ..mixins import HasChildren

if TYPE_CHECKING:
    from ..enums import PartIDFormat, PartNumber


class Part(BaseModel, HasChildren["Valkyrie"]):
    id: str = field(compare=False)
    no: "PartNumber" = field(init=True)
    id_format: "PartIDFormat"

    id_length: ClassVar[int] = 3

    @classmethod
    def validate_id(cls, id: str) -> str:
        id = BaseModel.validate_id.__func__(cls, id)

        if id not in RAW_PARTS_MAP:
            raise UnknownPartIDError(id)

        return id

    def build_valkyries_map(self, raw_valkyries: Iterable[tuple[str, str, int] | tuple[str, str]]):
        """
        Add all children parsed from the raw Valkyrie data.

        :param raw_valkyries: The raw Valkyrie data. \
        Iterable of tuples containing Valkyrie's ID, \
        name, and, optionally, maximum :class:`Battlesuit` ID.
        :type raw_valkyries: Iterable[tuple[str, str, int] | tuple[str, str]]
        """
        for valkyrie in self._parse_raw_valkyries(raw_valkyries):
            self.add_child(valkyrie)

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
                children_id_range=range(start, end)
            )

            # Current end will be the next start for the current ID
            range_starts[id] = end


__all__ = ["Part"]
