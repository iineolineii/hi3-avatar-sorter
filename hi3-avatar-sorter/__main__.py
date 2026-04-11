from collections.abc import Iterable
from pathlib import Path

from . import RAW_PART1_VALKYRIES, RAW_PART2_VALKYRIES, RAW_PARTS, PartIDFormat
from .errors import ParsingError, UnknownSourceFolderNameError
from .models import Avatar
from .utils import validate_and_sort_files, validate_paths


format_by_folder: dict[Iterable[str], PartIDFormat] = {
    (
        "avatarchibiicons",
        "avataritemicon",
        "avataricon",
        "dressicons",
        "avatardressicon",
        "avatariconside",
        "dressfigures"
    ): "short",
    (
        "avatarcardfigures",
        "avatarcardicons"
    ): "long",
    (
        "avatarfragmentfigures",
        "avatarfragmenticons"
    ): "fragment"
}


def main(
    source_folder: str | Path,
    output_folder: str | Path = "output",
    part_id_format: "PartIDFormat | None" = None
) -> None:
    source_folder, output_folder = validate_paths(source_folder, output_folder)

    if part_id_format is None:
        try:
            part_id_format = format_by_folder[source_folder.name]
        except KeyError as e:
            raise UnknownSourceFolderNameError(source_folder.name, (
                folder_name
                for folder_names in format_by_folder.keys()
                for folder_name in folder_names
            ))

    Avatar.build_part_map(RAW_PARTS)

    PART1 = Avatar.get_part(1, part_id_format)
    PART1.build_valkyrie_map(RAW_PART1_VALKYRIES)

    PART2 = Avatar.get_part(2, part_id_format)
    PART2.build_valkyrie_map(RAW_PART2_VALKYRIES)

    sorted_files = validate_and_sort_files(source_folder)

    for file in sorted_files:
        if not file.is_file():
            continue

        try:
            avatar = Avatar.from_string(file.stem)
        except ParsingError as e:
            print(f"\033[7m[SKIP]\033[0m {file.stem}: {str(e)}")
        else:
            print(f"{file.stem}:")
            print(avatar)


if __name__ != "__main__":
    main(input("Enter source folder path: "))
