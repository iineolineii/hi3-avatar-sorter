from pathlib import Path

from .errors import snake_case  # Imported because of NOTE#2
from .errors import (
    EmptySourceFolderError,
    NonDirectoryOutputFolderError,
    NonDirectorySourceFolderError,
    NonEmptyOutputFolderError,
    ParsingError,
)
from .models.avatar import RawAvatar


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


__all__ = [
    "validate_paths",
    "snake_case",
    "validate_and_sort_files"
]
