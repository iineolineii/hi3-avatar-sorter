from pathlib import Path
from typing import TYPE_CHECKING

from . import fix_avatar_string
from .. import log
from ..enums import PartIDFormat
from ..errors import (
    EmptySourceFolderError,
    NonDirectoryOutputFolderError,
    NonDirectorySourceFolderError,
    NonEmptyOutputFolderError,
    NonNumericIDError,
    ParsingError,
    UnknownSourceFolderNameError,
    WrongPartIDFormat
)
from ..fixers import AvatarFixer
from ..maps import FORMAT_BY_FOLDER, RAW_PARTS_MAP
from ..models.avatar import RawAvatar


if TYPE_CHECKING:
    from ..fixers.avatar import RawAvatar


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
        source_folder.mkdir(parents=True)

    if output_folder.exists():
        if not output_folder.is_dir():
            raise NonDirectoryOutputFolderError(output_folder)

        if any(output_folder.iterdir()):
            raise NonEmptyOutputFolderError(output_folder)
    else:
        output_folder.mkdir(parents=True)

    return source_folder, output_folder


def get_format_by_folder(source_folder: Path) -> "PartIDFormat":
    known_folder_names: set[str] = set()

    for folder_names, part_id_format in FORMAT_BY_FOLDER.items():
        for folder_name in folder_names:
            if source_folder.name in folder_names:
                return part_id_format

            known_folder_names.add(repr(folder_name))

    raise UnknownSourceFolderNameError(source_folder.name, known_folder_names)


def _parse_raw_avatar_file(
    file: "Path",
    part_id_format: "PartIDFormat",
    fixers: dict[str, "AvatarFixer"]
) -> tuple[int, str, "RawAvatar"] | None:
    """
    Parse a single file into a :class:`RawAvatar` instance and compute its index.

    Attempts to apply fixers first. If that fails, parses the filename directly
    and validates the Part ID format.

    :param file: Path to the avatar file.
    :type file: Path

    :param part_id_format: Expected Part ID format for validation.
    :type part_id_format: :class:`PartIDFormat`

    :param fixers: Mapping of fix names to their :class:`AvatarFixer` instances.
    :type fixers: dict[str, :class:`AvatarFixer`]

    :return: If the file has been parsed correctly, returns a tuple containing \
    index, file name, and a :class:`RawAvatar` instance. \
    Otherwise returns `None`.
    :rtype: tuple[int, str :class:`RawAvatar`] | None

    :raises WrongPartIDFormat: If the file's Part ID format does not match the expected format.
    """
    file_name = file.stem

    if file_name == "1303":
        pass

    fixed = fix_avatar_string(file_name, fixers)

    if fixed:
        fix_name, raw_avatar = fixed
        object.__setattr__(raw_avatar, "fixed", True)
        index = int(raw_avatar)
        log.debug(f"[FIX] Fixed {fix_name} in {file_name!r}: {str(raw_avatar)!r}")
        return index, file_name, raw_avatar

    try:
        raw_avatar = RawAvatar.from_string(file_name)
        raw_part_id = raw_avatar.part_id
        raw_part_id_format, _ = RAW_PARTS_MAP[raw_part_id]

        if raw_part_id_format != part_id_format:
            raise WrongPartIDFormat(raw_part_id_format, part_id_format)

        index = int(raw_avatar)
        return index, file_name, raw_avatar

    except NonNumericIDError:
        return None

    except ParsingError as e:
        log.info(f"[SKIP] Invalid file name {file_name!r}: {e}")
        return None


__all__ = [
    "validate_paths",
    "get_format_by_folder",
    "_parse_raw_avatar_file"
]
