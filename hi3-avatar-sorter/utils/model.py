from dataclasses import asdict, is_dataclass
from json import JSONEncoder
from pathlib import Path
from typing import Any

from ..enums import PartIDFormat
from ..errors import DuplicateRawAvatarError
from ..fixers import AvatarFixer
from ..models.avatar import RawAvatar
from .path import _parse_raw_avatar_file

from ..__main__ import log
from ..errors import ParsingError
from ..models.avatar import Avatar, RawAvatar


# Source - https://stackoverflow.com/a/51286749
# Posted by miracle2k, License - CC BY-SA 4.0
class DataclassEncoder(JSONEncoder):
    def default(self, o: Any):
        if is_dataclass(o):
            return asdict(o) # pyright: ignore[reportArgumentType]

        return super().default(o)


__all__ = ["DataclassEncoder"]


def build_avatars_map(raw_avatar_map: dict[int, tuple[str, "RawAvatar"]]) -> dict[int, "Avatar"]:
    avatars_map: dict[int, "Avatar"] = {}

    for index, (file_name, raw_avatar) in sorted(raw_avatar_map.items()):
        try:
            avatars_map[index] = Avatar.from_raw(raw_avatar)
        except ParsingError as e:
            log.info(f"[SKIP] Invalid file name {file_name!r}: {e}")

    return avatars_map


def build_raw_avatars_map(
    source_folder: "Path",
    part_id_format: "PartIDFormat",
    fixers: dict[str, "AvatarFixer"]
) -> dict[int, tuple[str, "RawAvatar"]]:
    """
    Build a mapping of Avatar indices to their Raw avatar data and filenames.

    Iterates over files in the source folder,
    parses them into :class:`RawAvatar` instances,
    and validates that there are no duplicate indices.

    :param source_folder: Folder containing Raw avatar files.
    :type source_folder: Path

    :param part_id_format: Expected Part ID format for validation.
    :type part_id_format: :class:`PartIDFormat`

    :param fixers: Mapping of fix names to their :class:`AvatarFixer` instances.
    :type fixers: dict[str, :class:`AvatarFixer`]

    :return: Dictionary mapping Avatar indices to tuples containing file name and :class:`RawAvatar` instances).
    :rtype: dict[int, tuple[str, :class:`RawAvatar`]]

    :raises :class:`DuplicateRawAvatarError`: If two files result in the same Avatar index.
    :raises :class:`WrongPartIDFormat`: If a file's Part ID format does not match the expected given one.
    """
    raw_avatar_map: dict[int, tuple[str, "RawAvatar"]] = {}

    for file in source_folder.iterdir():
        if not file.is_file():
            continue

        parsed = _parse_raw_avatar_file(file, part_id_format, fixers)

        if not parsed:
            continue

        index, file_name, raw_avatar = parsed

        if (duplicate := raw_avatar_map.get(index)) is not None:
            raise DuplicateRawAvatarError(raw_avatar, file_name, duplicate[0])

        raw_avatar_map[index] = (file_name, raw_avatar)

    return raw_avatar_map
