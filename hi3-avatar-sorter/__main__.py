from pathlib import Path

from models.avatar import RawAvatar

from . import RAW_PARTS, PartIDFormat
from .errors import ParsingError
from .models import Avatar
from .utils import validate_paths


folder_name_by_format: dict[PartIDFormat, list[str]] = {
    "short": [
        "avatarchibiicons",
        "avataritemicon",
        "avataricon",
        "dressicons",
        "avatardressicon",
        "avatariconside",
        "dressfigures"
    ],
    "long": [
        "avatarcardfigures",
        "avatarcardicons"
    ],
    "skin_long": [
        "avatarcardfigures",
        "avatarcardicons"
    ],
    "fragment": [
        "avatarfragmentfigures",
        "avatarfragmenticons"
    ]
}


def validate_and_sort_files(folder: Path):
    index_by_file: dict[Path, int] = {}

    for file in folder.iterdir():
        try:
            index = int(RawAvatar.from_string(file.stem))
            assert index not in index_by_file.values(), "Duplicate index"
            index_by_file[file] = index
        except ParsingError as e:
            print(f"\033[7m[SKIP]\033[0m {file.stem}: {str(e)}")

    return sorted(index_by_file.keys(), key=lambda file: index_by_file[file])


def main(
    source_folder: str | Path,
    output_folder: str | Path = "output",
    part_id_format: PartIDFormat | None = None
) -> None:
    source_folder, output_folder = validate_paths(source_folder, output_folder)

    if part_id_format is None:
        raise NotImplementedError(folder_name_by_format)

    Avatar.build_part_map(RAW_PARTS)
    PART1 = Avatar.get_part(1, part_id_format)
    PART2 = Avatar.get_part(2, part_id_format)

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
