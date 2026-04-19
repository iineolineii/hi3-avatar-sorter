from abc import ABCMeta
from collections.abc import Hashable, Iterable
from pathlib import Path
from typing import Generic, TypeVar

from .errors import snake_case  # Imported because of NOTE#2
from .errors import (
    EmptySourceFolderError,
    NonDirectoryOutputFolderError,
    NonDirectorySourceFolderError,
    NonEmptyOutputFolderError,
    ParsingError
)
from .fixers import AvatarFixer
from .models.avatar import RawAvatar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


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


def fix_avatar_string(avatar_string: str, fixers: Iterable[AvatarFixer]) -> RawAvatar | None:
    avatar_string = avatar_string.lower()

    # Each input is allowed to pass through only one mechanism.
    # The first successful fix wins, so the same string is never rewritten twice.
    for fixer in fixers:
        if fixed_string := fixer.fix(avatar_string):
            return fixed_string


class MexContainer(Generic[K, V], dict["K", "V"], metaclass=ABCMeta):
    """
    Base container that stores values based on their MEX (minimal excluded number).
    """

    def __init__(
        self,
        map: dict["K", "V"] = {},
        mex_attr_name: str = "no"
    ) -> None:
        """
        Args:
            map (`dict["K", "V"]`):
                Initial container data. Defaults to an empty dictionary.
                All values passed here will be reserved via the `reserve()` method.
                Each of these values must have an attribute with the specified in `mex_attr_name` argument.

            mex_attr_name (`str`):
                Name of the values' attribute used as a MEX. Defaults to `"no"`.
        """
        super().__init__()

        self.mex_attr_name = mex_attr_name
        """
        mex_attr_name (`str`):
            Name of the values' attribute used as a MEX. Defaults to `"no"`.
        """
        self.map: dict["K", "V"] = map
        """
        map (`dict["K", "V"]`):
            Internal container.
        """
        self.update(self.map)
        self.consumed_mexes: set[int] = set()
        self.current_mex = 0

    def consume_mex(self) -> int:
        """
        Mark current MEX as consumed.

        Returns:
            `int`: The current MEX value.
        """
        mex = self.current_mex
        self.consumed_mexes.add(mex)
        self.update_mex()

        return mex

    def update_mex(self) -> None:
        """
        Increments `current_mex` until it is no longer present in `consumed_mexes`.
        """
        while self.current_mex in self.consumed_mexes:
            self.current_mex += 1

    def setdefault(self, key: "K", default: "V") -> "V": # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Get a value by key, or set it to `default` if missing.

        Args:
            key (`K`):
                The key to look up.

            default (`V`):
                The value to set and return if the key is missing.

        Returns:
            `V`: The existing or newly set value.
        """
        if key not in self:
            self[key] = default

        return self[key]

    def __setitem__(self, key: "K", value: "V") -> None:
        mex = self.consume_mex()
        object.__setattr__(value, self.mex_attr_name, mex)

        return super().__setitem__(key, value)

    def __hash__(self) -> int: # pyright: ignore[reportIncompatibleVariableOverride]
        return hash(frozenset(self.items()))


__all__ = [
    "fix_avatar_string",
    "MexContainer",
    "snake_case",
    "validate_paths",
    "validate_and_sort_files"
]
