from collections.abc import Hashable, Iterable
from pathlib import Path
from typing import Protocol

from .errors import (
    SourceFolderIsNotDirectoryError,
    SourceFolderIsEmptyError,
    OutputFolderIsNotDirectoryError,
    OutputFolderIsNotEmptyError,
)

class HashableIterable[T](Hashable, Iterable[T], Protocol):
    pass


def validate_paths(source_folder: str | Path, output_folder: str | Path = "output"):
    source_folder = Path(source_folder)
    output_folder = Path(output_folder)

    if not output_folder.is_absolute():
        output_folder = source_folder / output_folder

    if source_folder.exists():
        if not source_folder.is_dir():
            raise SourceFolderIsNotDirectoryError(source_folder)

        if not source_folder.iterdir():
            raise SourceFolderIsEmptyError(source_folder)
    else:
        source_folder.mkdir()

    if output_folder.exists():
        if not output_folder.is_dir():
            raise OutputFolderIsNotDirectoryError(output_folder)

        if any(output_folder.iterdir()):
            raise OutputFolderIsNotEmptyError(output_folder)
    else:
        output_folder.mkdir()

    return source_folder, output_folder


__all__ = ["validate_paths", "HashableIterable"]
