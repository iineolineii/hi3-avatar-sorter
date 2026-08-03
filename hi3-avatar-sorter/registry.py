from collections.abc import Iterable
from itertools import pairwise
from pathlib import Path
from typing import Any, overload

from .enums import PartIDFormat
from .errors import ModelNotFoundError
from .models import Avatar, Battlesuit, Part, Skin, SkinRarity, Valkyrie
from .models.base import MAX_MODEL_ID
from .utils import RawAvatar


class _AvatarRegistryMeta(type):
    _FORMAT_BY_FOLDER = {
        "avatarchibiicons":      PartIDFormat.ICON,
        "avataritemicon":        PartIDFormat.ICON,
        "avataricon":            PartIDFormat.ICON,
        "dressicons":            PartIDFormat.ICON,
        "avatardressicon":       PartIDFormat.ICON,
        "avatariconside":        PartIDFormat.ICON,
        "dressfigures":          PartIDFormat.ICON,
        "avatarcardfigures":     PartIDFormat.SPLASH,
        "avatarcardicons":       PartIDFormat.SPLASH,
        "avatarfragmentfigures": PartIDFormat.FRAGMENT,
        "avatarfragmenticons":   PartIDFormat.FRAGMENT
    }

    _ALL_PARTS = (
        Part(1, "000", PartIDFormat.ICON    ),
        Part(2, "002", PartIDFormat.ICON    ),
        Part(1, "006", PartIDFormat.SPLASH  ),
        Part(2, "302", PartIDFormat.SPLASH  ),
        Part(2, "062", PartIDFormat.SPLASH  ), # Second splash Part 2 ID is for skins found in folders avatarcardfigures and avatarcardicons
        Part(1, "001", PartIDFormat.FRAGMENT),
        Part(2, "202", PartIDFormat.FRAGMENT)
    )


    _VALKYRIES_BY_PART_NO = {
        1: (
            Valkyrie("01", "Kiana Kaslana",   50), # Changed from most common 10 because of NOTE#1
            Valkyrie("01", "Kallen Kaslana"     ),
            Valkyrie("02", "Raiden Mei",      10),
            Valkyrie("02", "Yae Sakura"         ),
            Valkyrie("03", "Bronya Zaychik"     ),
            Valkyrie("04", "Murata Himeko",   10),
            Valkyrie("04", "Liliya Olenyeva"    ),
            Valkyrie("04", "Rozaliya Olenyeva"  ),
            Valkyrie("05", "Theresa Apocalypse" ),
            Valkyrie("06", "Fu Hua"             ),
            Valkyrie("07", "Rita Rossweisse", 10),
            Valkyrie("07", "Seele Vollerei"     ),
            Valkyrie("08", "Durandal"           ),
            Valkyrie("09", "Asuka"              ),
            Valkyrie("20", "Keqing"             ),
            Valkyrie("21", "Fischl"             ),
            Valkyrie("22", "Elysia"             ),
            Valkyrie("23", "Mobius"             ),
            Valkyrie("24", "Natasha Cioara"     ),
            Valkyrie("25", "Carole Pepper"      ),
            Valkyrie("26", "Pardofelis"         ),
            Valkyrie("27", "Aponia"             ),
            Valkyrie("28", "Eden"               ),
            Valkyrie("29", "Griseo"             ),
            Valkyrie("30", "Vill-V"             ),
            Valkyrie("31", "Li Sushang"         ),
            Valkyrie("32", "Ai Hyperion Λ"      ),
            Valkyrie("33", "Susannah Manatt"    ),
            Valkyrie("34", "Misteln Schariac"   ),
            Valkyrie("35", "PROMETHEUS"         ),
            Valkyrie("36", "Shigure Kira"       ),
            Valkyrie("37", "Sirin"              )
        ),
        2: (
            Valkyrie("02", "Senadina"           ),
            Valkyrie("03", "Coralie 6626 Planck"),
            Valkyrie("04", "Erdős Helia"        ),
            Valkyrie("05", "Thelema Nutriscu"   ),
            Valkyrie("06", "«Lantern»"          ),
            Valkyrie("07", "Songque"            ),
            Valkyrie("08", "Vita"               ),
            Valkyrie("09", "Sparkle"            )
        )
    }


    def __init__(cls, name: str, bases: tuple[type, ...], dict: dict[str, Any], /, **kwds: Any) -> None:
        super().__init__(name, bases, dict, **kwds)
        cls._build_part_maps()


    def _build_part_maps(cls):
        # TODO: Threadsafe
        by_id: dict[str, Part] = {}
        by_format: dict[PartIDFormat, dict[int, tuple[Part, ...]]] = {}

        for part in cls._ALL_PARTS:
            cls._update_part_by_id_map(part, by_id)
            cls._update_parts_by_format_map(part, by_format)

        cls._PART_BY_ID = by_id
        cls._PARTS_BY_FORMAT = by_format


    def _update_part_by_id_map(cls, part: Part, map: dict[str, Part]):
        if part.id in map:
            raise ValueError(f"Duplicate part ID {part.id}")

        map[part.id] = part


    def _update_parts_by_format_map(cls, part: Part, map: dict[PartIDFormat, dict[int, tuple[Part, ...]]]):
        if part.id_format not in map:
            map[part.id_format] = {}

        by_no = map[part.id_format]

        if part.no not in by_no:
            by_no[part.no] = ()

        parts = by_no[part.no]
        parts += (part,)


class AvatarRegistry(metaclass=_AvatarRegistryMeta):
    @overload
    def __init__(self, *, folder: Path) -> None: ...

    @overload
    def __init__(self, *, part_id_format: "PartIDFormat") -> None: ...

    def __init__(
        self,
        folder: Path | None = None,
        part_id_format: "PartIDFormat | None" = None
    ) -> None:
        self.part_id_format = self._get_part_id_format(folder, part_id_format)
        self.parts_by_no = self._get_parts_by_no(self.part_id_format)
        self.part_by_id = type(self)._PART_BY_ID

        self._register_valkyries(self.parts_by_no)


    def register_avatar(self, raw: "RawAvatar") -> "Avatar":
        no   = int(raw)
        id = raw.id

        part       = self.part_by_id[raw.part_id]
        valkyrie   = self._get_valkyrie_by_ids(part, raw.valkyrie_id, raw.battlesuit_id)
        battlesuit = valkyrie.add_child(Battlesuit(raw.battlesuit_id), exists_ok=True)

        if raw.skin_rarity_id is not None and raw.skin_id is not None:
            skin_rarity = battlesuit.add_child(SkinRarity(raw.skin_rarity_id), exists_ok=True)
            skin        = skin_rarity.add_child(Skin(raw.skin_id), exists_ok=True)
        else:
            skin_rarity = skin = None

        note = raw.note

        return Avatar(
            no, id, raw,
            part, valkyrie, battlesuit,
            skin_rarity, skin, note
        )


    @classmethod
    def _get_part_id_format(
        cls,
        folder: Path | None,
        part_id_format: PartIDFormat | None
    ) -> PartIDFormat:
        match (folder, part_id_format):
            case (None, None):
                raise ValueError("Either specify folder or part_ID_format")

            case (folder, None):
                if folder.name not in cls._FORMAT_BY_FOLDER:
                    raise KeyError("Unknown folder name. Check it or provide part ID format")

                part_id_format = cls._FORMAT_BY_FOLDER[folder.name]

            case (None, part_id_format):
                pass

            case _:
                raise ValueError("Either specify folder or part_ID_format")

        return part_id_format


    @classmethod
    def _get_parts_by_no(cls, part_id_format: PartIDFormat):
        map = cls._PARTS_BY_FORMAT

        if part_id_format not in map:
            raise KeyError(f"Unknown part ID format: {part_id_format}")

        return map[part_id_format]


    @classmethod
    def _register_valkyries(
        cls,
        parts_by_no: dict[int, tuple[Part, ...]],
    ) -> None:
        """Add Valkyries to every matching Part."""

        for part_no, valkyries in cls._VALKYRIES_BY_PART_NO.items():
            # Look up all parts that belong to the current part number
            parts = parts_by_no.get(part_no)
            if parts is None:
                raise KeyError(f"Unknown part number: {part_no}")

            # A known part number must still have at least one part
            if not parts:
                raise ValueError(f"No parts found with number: {part_no}")

            cls._link_children_id_ranges(valkyries)

            for part in parts:
                for valkyrie in valkyries:
                    part.add_child(valkyrie)

    @classmethod
    def _link_children_id_ranges(
        cls,
        valkyries: Iterable[Valkyrie],
    ) -> None:
        """Chain children ID ranges of Valkyries with the same ID."""

        for previous, current in pairwise(valkyries):
            if previous.children_id_range.stop != MAX_MODEL_ID:
                if previous.id != current.id:
                    raise ValueError(
                        f"Cannot chain children ID ranges "
                        f"for Valkyries with different IDs: "
                        f"{previous.id!r} and {current.id!r}"
                    )

                current._update_children_id_range(
                    start=previous.children_id_range.stop + 1
                )

    @classmethod
    def _get_valkyrie_by_ids(cls, part: Part, valkyrie_id: str, battlesuit_id: int | str) -> Valkyrie:
        numeric_battlesuit_id = int(battlesuit_id)

        for valkyrie in part:
            if (
                valkyrie.id == valkyrie_id and
                numeric_battlesuit_id in valkyrie.children_id_range
            ):
                return valkyrie

        raise ModelNotFoundError(
            Valkyrie.__name__, [
                f"part.no == {part.no}",
                f"id == {valkyrie_id!r}",
                f"children_id_range contains {numeric_battlesuit_id}"
            ]
        )


__all__ = ["AvatarRegistry"]
