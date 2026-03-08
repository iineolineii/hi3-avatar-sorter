from collections import defaultdict

from .errors import ValkyrieNotFoundError
from .models import PART1, PART2, Part, Valkyrie


class ValkyrieDatabase:
    def __init__(self, part1_valkyries: list[tuple], part2_valkyries: list[tuple], default_max: int = 100) -> None:
        self._all_valkyries: list[Valkyrie] = []
        self._valkyrie_db: dict[tuple[int, Part], list[Valkyrie]] = defaultdict(list)

        # Store range start for each code
        range_starts: dict[tuple[int, Part], int] = {}

        # Merge raw data preserving the order
        valkyries = [(part1_valkyries, PART1), (part2_valkyries, PART2)]

        for raw_valkyries, part in valkyries:
            for raw in raw_valkyries:
                code: int = raw[0]
                name: str = raw[1]

                # Current start is the previous end
                # Or 0 if current valkyrie is the first one with current code
                start = range_starts.get((code, part), 0)
                end = raw[2] if len(raw) > 2 else default_max

                valkyrie = Valkyrie(
                    code=code,
                    name=name,
                    part=part,
                    battlesuit_code_range=range(start, end)
                )

                self._all_valkyries.append(valkyrie)
                valkyrie.no = len(self._all_valkyries)
                self._valkyrie_db[(code, part)].append(valkyrie)

                # Current end is the next start
                range_starts[(code, part)] = end


    def get(self, code: int, part: Part, battlesuit_code: int) -> Valkyrie:
        candidates = self._valkyrie_db.get((code, part), [])

        for valkyrie in candidates:
            if battlesuit_code in valkyrie.battlesuit_code_range:
                return valkyrie

        raise ValkyrieNotFoundError(code, part, battlesuit_code)

    def all(self) -> list[Valkyrie]:
        return self._all_valkyries
