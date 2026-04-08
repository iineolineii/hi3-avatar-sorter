from pathlib import Path

from .errors import snake_case  # Imported because of NOTE#2
from .errors import (
    EmptySourceFolderError,
    NonDirectoryOutputFolderError,
    NonDirectorySourceFolderError,
    NonEmptyOutputFolderError,
)


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


__all__ = [
    "validate_paths",
    "snake_case"
]
