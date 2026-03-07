from collections import defaultdict

from .errors import ValkyrieNotFoundError

from .models import PART1, PART2, Valkyrie


class ValkyrieRegistry:
    def __init__(self, part1_valkyries: list[tuple], part2_valkyries: list[tuple], default_max: int = 100) -> None:
        self._valkyries: list[Valkyrie] = []
        self._valkyries_by_code: dict[int, list[Valkyrie]] = defaultdict(list)

        # Store range start for each code
        range_starts: dict[int, int] = {}

        # Merge raw data preserving the order
        valkyries = [(part1_valkyries, PART1), (part2_valkyries, PART2)]

        for raw_valkyries, part in valkyries:
            for raw in raw_valkyries:
                code, name = raw[0], raw[1]

                # Current start is the previous end
                # Or 0 if current valkyrie is the first one with current code
                start = range_starts.get(code, 0)
                end = raw[2] if len(raw) > 2 else default_max

                valkyrie = Valkyrie(
                    code=code,
                    name=name,
                    part=part,
                    battlesuit_code_range=range(start, end)
                )

                self._valkyries.append(valkyrie)
                valkyrie.no = len(self._valkyries)
                self._valkyries_by_code[code].append(valkyrie)

                # Current end is the next start
                range_starts[code] = end


    def get(self, code: int, battlesuit_code: int) -> Valkyrie:
        candidates = self._valkyries_by_code.get(code, [])

        for valkyrie in candidates:
            if battlesuit_code in valkyrie.battlesuit_code_range:
                return valkyrie

        raise ValkyrieNotFoundError(code, battlesuit_code)

    def all(self) -> list[Valkyrie]:
        return self._valkyries
