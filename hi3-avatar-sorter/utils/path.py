from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING

from ..enums import PartIDFormat
from ..errors import (
    EmptySourceFolderError,
    NonDirectoryOutputFolderError,
    NonDirectorySourceFolderError,
    NonEmptyOutputFolderError,
    ParsingError,
    UnknownSourceFolderNameError
)
from ..fixers.avatar import RawAvatar

if TYPE_CHECKING:
    from ..maps import FORMAT_BY_FOLDER


def validate_paths(source_folder: str | Path, output_folder: str | Path = "output") -> tuple[Path, Path]:
    source_folder = Path(source_folder)
    output_folder = Path(output_folder)

    if not output_folder.is_absolute():
        output_folder = source_folder / output_folder

    if source_folder.exists():
        if not source_folder.is_dir():
            raise NonDirectorySourceFolderError(source_folder)

        if not source_folder.iterdir():
            raise EmptySourceFolderError(source_folder)
    else:
        source_folder.mkdir()

    if output_folder.exists():
        if not output_folder.is_dir():
            raise NonDirectoryOutputFolderError(output_folder)

        if any(output_folder.iterdir()):
            raise NonEmptyOutputFolderError(output_folder)
    else:
        output_folder.mkdir()

    return source_folder, output_folder


def validate_and_sort_files(folder: Path) -> Iterator[tuple[Path, "RawAvatar"]]:
    from ..models.avatar import RawAvatar
    items: dict[int, tuple[Path, RawAvatar]] = {}

    for file in folder.iterdir():
        try:
            raw_avatar = RawAvatar.from_string(file.stem)
            index = int(raw_avatar)

            if index in items:
                raise AssertionError("Duplicate index")

            items[index] = (file, raw_avatar)

        except ParsingError as e:
            print(f"\033[7m[SKIP]\033[0m {file.stem}: {e}")

    return (items[index] for index in sorted(items))


def get_format_by_folder(source_folder: Path) -> "PartIDFormat":
    try:
        part_id_format = FORMAT_BY_FOLDER[source_folder.name]

    except KeyError as e:
        known_folder_names = {
            repr(folder_name)
            for folder_names in FORMAT_BY_FOLDER.keys()
            for folder_name in folder_names
        }

        raise UnknownSourceFolderNameError(source_folder.name, known_folder_names) from e

    return part_id_format


__all__ = ["validate_paths", "validate_and_sort_files", "get_format_by_folder"]
