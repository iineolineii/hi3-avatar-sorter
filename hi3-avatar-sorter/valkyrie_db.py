from collections import defaultdict
from typing import TYPE_CHECKING

from .errors import ValkyrieNotFoundError
from .models.valkyrie import Valkyrie

if TYPE_CHECKING:
    from .models import Part


class ValkyrieDatabase:
    def __init__(
        self,
        part1_valkyries: list[tuple[int, str] | tuple[int, str, int]],
        part2_valkyries: list[tuple[int, str] | tuple[int, str, int]],
        default_max: int = 100,
    ) -> None:
        from . import PART1, PART2

        self._all_valkyries: list["Valkyrie"] = []
        self._valkyrie_db: dict[tuple[int, "Part"], list["Valkyrie"]] = defaultdict(list)

        # Store range start for each ID
        range_starts: dict[tuple[int, "Part"], int] = {}

        # Merge raw data preserving the order
        valkyries = [(part1_valkyries, PART1), (part2_valkyries, PART2)]

        for raw_valkyries, part in valkyries:
            for raw in raw_valkyries:
                id:   int = raw[0]
                name: str = raw[1]

                # Current start is the previous end
                # Or 0 if current valkyrie is the first one with current ID
                start = range_starts.get((id, part), 0)
                end = raw[2] if len(raw) > 2 else default_max

                valkyrie = Valkyrie(
                    id=id,
                    name=name,
                    part=part,
                    battlesuit_id_range=range(start, end)
                )

                self._all_valkyries.append(valkyrie)
                valkyrie.no = len(self._all_valkyries)
                self._valkyrie_db[(id, part)].append(valkyrie)

                # Current end is the next start
                range_starts[(id, part)] = end

    def get(self, id: int, battlesuit_id: int, part: "Part") -> "Valkyrie":
        candidates = self._valkyrie_db.get((id, part), [])

        for valkyrie in candidates:
            if battlesuit_id in valkyrie.battlesuit_id_range:
                return valkyrie

        raise ValkyrieNotFoundError(id, part, battlesuit_id)

    def all(self) -> list["Valkyrie"]:
        return self._all_valkyries
