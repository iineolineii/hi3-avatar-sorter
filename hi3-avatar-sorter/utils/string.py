import re
import string
from collections.abc import Collection, Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..enums import PartIDFormat
    from ..fixers import AvatarFixer
    from ..models.avatar import RawAvatar


DELIMITERS = " -_"
PUNCTUATION = "".join(
    character
    for character in string.punctuation
    if character not in DELIMITERS
)


def title_case(string: str):
    """
    Convert a string to title case.

    Example:
        Hello world => Hello World
        hello-world => Hello World
        helloWorld => Hello World

    Note:
        - This function was adapted from `caseconverter.titlecase`

        - Source: https://github.com/chrisdoherty4/python-case-converter/blob/master/caseconverter/title.py

        - Copyright (c) Chris Doherty and Contributors

        - Licensed under the MIT License.
    """

    string = string.strip(DELIMITERS)

    # Strip punctuation
    string = re.sub("[{}]+".format(re.escape(PUNCTUATION)), "", string)

    # Change recurring delimiters into single delimiters.
    string = re.sub("[{}]+".format(re.escape(DELIMITERS)), DELIMITERS[0], string)

    if not string:
        return ""

    if string.isupper():
        string = string.lower()

    chars = iter(string)
    result = next(chars).upper()

    # Previous character and current character
    previous = None
    character = next(chars)

    while character:
        # On delimiters, write the space and make the next character uppercase
        if character in DELIMITERS:
            result += " "
            result += next(chars).upper()

        # Handle camelCase -> Title Case
        elif (
            previous is not None
            and previous.isalpha()
            and previous.islower()
            and character.isupper()
        ):
            result += " "
            result += character

        else:
            result += character.lower()

        previous = character
        character = next(chars, "")

    return result


def fix_avatar_string(avatar_string: str, fixers: dict[str, "AvatarFixer"]) -> "tuple[str, RawAvatar] | None":
    avatar_string = avatar_string.lower()

    # Each input is allowed to pass through only one mechanism.
    # The first successful fix wins, so the same string is never rewritten twice.
    for fix_name, fixer in fixers.items():
        if fixed_string := fixer.fix(avatar_string):
            return fix_name, fixed_string


def build_fixers_map(part_id_format: "PartIDFormat") -> dict[str, "AvatarFixer"]:
    """
    Build a dictionary mapping fix names to their :class:`AvatarFixer` instances.

    :param part_id_format: Part ID format passed to :class:`AvatarFixer`.
    :type part_id_format: :class:`PartIDFormat`

    :return: Dictionary mapping fix names to their :class:`AvatarFixer` instances.
    :rtype: dict[str, :class:`AvatarFixer`]
    """
    from ..fixers import AvatarFixer, PrefixFixer
    from ..fixers.maps import (
        EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP,
        TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP,
        TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP,
        WRONG_BATTLESUIT_ID_REPLACEMENT_MAP,
        WRONG_NOTE_REPLACEMENT_MAP
    )

    fixers: dict[str, "AvatarFixer"] = {}

    # Exact replacements
    fixers["empty Battlesuit ID"]     = AvatarFixer(part_id_format, EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["empty Battlesuit ID"].replacement_map, cls=DataclassEncoder, indent=4))
    fixers["too short Battlesuit ID"] = AvatarFixer(part_id_format, TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["too short Battlesuit ID"].replacement_map, cls=DataclassEncoder, indent=4))
    fixers["too short Valkyrie ID"]   = AvatarFixer(part_id_format, TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["too short Valkyrie ID"].replacement_map, cls=DataclassEncoder, indent=4))
    fixers["misspelled note"]         = AvatarFixer(part_id_format, WRONG_NOTE_REPLACEMENT_MAP)
    # print(json.dumps(fixers["misspelled note"].replacement_map, cls=DataclassEncoder, indent=4))

    # Prefix replacements
    fixers["wrong Battlesuit ID"] = PrefixFixer(part_id_format, WRONG_BATTLESUIT_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["wrong Battlesuit ID"].replacement_map, cls=DataclassEncoder, indent=4))

    return fixers


def _compute_stats(
    values: Collection,
    names: Sequence[str],
    stats_map: dict[int, dict[str, int]],
) -> None:
    if not names or not values:
        return

    children_name = names[0]

    for value in values:
        children = list(getattr(value, children_name, {}).values())

        if children:
            _compute_stats(children, names[1:], stats_map)

        stats: dict[str, int] = {}
        if children:
            stats[children_name] = len(children)
            for child in children:
                for k, v in stats_map.get(id(child), {}).items():
                    stats[k] = stats.get(k, 0) + v

        stats_map[id(value)] = stats


def print_node(
    values: Collection,
    names: Sequence[str],
    stats_map: dict[int, dict[str, int]],
    prefix: str = "",
    skip_empty: bool = False,
):
    if skip_empty and names:
        values = [v for v in values if hasattr(v, names[0])]

    total = len(values)

    for index, value in enumerate(values):
        is_last = index == (total - 1)
        branch = "└─ " if is_last else "├─ "
        bar = "   " if is_last else "│  "

        stats = stats_map.get(id(value), {})
        stats_parts = []
        for name in names:
            count = stats.get(name)
            if count:
                stats_parts.append(f"{capitalize(name)}: {count}")

        stats_str = f", {', '.join(stats_parts)}" if stats_parts else ""

        has_children = bool(names and getattr(value, names[0], {}))
        id_branch = "│  " if has_children else "└─ "

        text = (
            f"{prefix}{branch}{value}\n"
            f"{prefix}{bar}{id_branch}(ID: {value.id}{stats_str})"
        )
        print(text)

        if names:
            children = list(getattr(value, names[0], {}).values())
            print_node(
                children,
                names[1:],
                stats_map=stats_map,
                prefix=prefix + bar,
                skip_empty=skip_empty,
            )


def tree():
    from ..models.avatar import Avatar

    values = list(Avatar.parts.values())
    names = ["valkyries", "battlesuits", "skin_rarities", "skins"]

    stats_map: dict[int, dict[str, int]] = {}
    _compute_stats(values, names, stats_map)

    print_node(values, names, stats_map=stats_map, skip_empty=True)


__all__ = [
    "snake_case",
    "fix_avatar_string",
    "build_fixers_map",
    "capitalize",
    "_compute_stats",
    "print_node",
    "tree"
]
