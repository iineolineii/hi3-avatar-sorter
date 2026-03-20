from annotationlib import ForwardRef
from collections.abc import Hashable, Iterable
from pathlib import Path
from typing import Protocol, get_args, get_origin

from . import PART1_VALKYRIES, PART2_VALKYRIES
from .models import Part, Valkyrie
from .models.part import PART1, PART2

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
    orig_bases = cls.__orig_bases__
    if len(orig_bases) != 1:
        raise TypeError # TODO: Add custom exception class

    base = orig_bases[0]
    if get_origin(base) is not parent:
        raise TypeError # TODO: Add custom exception class

    type_arg: type | ForwardRef = get_args(base)[0]
    if isinstance(type_arg, type):
        return type_arg
    else:
        return type_arg.evaluate(owner=cls)


def build_valkyrie_db():
    # Store range start for each ID
    range_starts: dict[tuple[str, "Part"], int] = {}

    # Merge raw data preserving the order
    valkyries = [(PART1_VALKYRIES, PART1), (PART2_VALKYRIES, PART2)]

    for raw_valkyries, part in valkyries:
        for raw in raw_valkyries:
            id:   str = raw[0]
            name: str = raw[1]

            # Current start is the previous end
            # Or 0 if current valkyrie is the first one with current ID
            start = range_starts.get((id, part), 0)

            if len(raw) > 2:
                end = raw[2]

                valkyrie = Valkyrie(
                        id=id,
                        name=name,
                        children_id_range=range(start, end)
                    )
            else:
                valkyrie = Valkyrie(
                        id=id,
                        name=name
                    )
                end = valkyrie.children_id_range.stop

            part.add_valkyrie(valkyrie)

            # Current end is the next start
            range_starts[(id, part)] = end


__all__ = [
    "validate_paths",
    "build_valkyrie_db",
    "evaluate_type_argument",
    "HashableIterable"
]
