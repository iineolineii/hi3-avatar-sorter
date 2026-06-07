from pathlib import Path

from .enums import PartIDFormat
from .maps import RAW_PARTS_MAP, RAW_VALKYRIES_MAP
from .models.avatar import Avatar
from .utils import (
    build_avatars_map,
    build_fixers_map,
    build_raw_avatars_map,
    get_format_by_folder,
    validate_paths
)


def main(
    source_folder: str | Path,
    output_folder: str | Path = "output",
    part_id_format: "PartIDFormat | None" = None
) -> None:
    source_folder, output_folder = validate_paths(source_folder, output_folder)

    if part_id_format is None:
        part_id_format = get_format_by_folder(source_folder)

    Avatar.build_parts_map(RAW_PARTS_MAP)
    for part_no, raw_valkyries in RAW_VALKYRIES_MAP.items():
        for part in Avatar.get_part_by_no(part_no, part_id_format):
            part.build_valkyries_map(raw_valkyries)

    fixers_map = build_fixers_map(part_id_format)

    raw_avatars_map = build_raw_avatars_map(source_folder, part_id_format, fixers_map)
    avatars_map = build_avatars_map(raw_avatars_map)


if __name__ == "__main__":
    main(input("Enter source folder path: "))
