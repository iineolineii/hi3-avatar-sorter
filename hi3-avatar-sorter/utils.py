from annotationlib import ForwardRef
from collections.abc import Hashable, Iterable, Sequence
from pathlib import Path
from typing import Protocol, get_args, get_origin

from .errors import (
    NonDirectorySourceFolderError,
    EmptySourceFolderError,
    NonDirectoryOutputFolderError,
    NonEmptyOutputFolderError
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


def evaluate_type_argument(cls: type, parent: type) -> type:
    orig_bases: Sequence[type] = cls.__orig_bases__

    for base in orig_bases:
        origin = get_origin(base)
        if origin is not parent:
            continue

        type_arg: type | ForwardRef = get_args(base)[0]

        if not isinstance(type_arg, type):
            raise TypeError

        return type_arg

    raise TypeError(f"Class {cls.__name__!r} does not inherit {parent.__name__!r}") # TODO: Add custom exception class


__all__ = [
    "validate_paths",
    "evaluate_type_argument",
    "HashableIterable"
]
