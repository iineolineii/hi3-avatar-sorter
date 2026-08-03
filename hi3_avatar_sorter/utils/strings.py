import re
import string
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import RawAvatar
    from ..fixers import AvatarFixer
    from ..registry import AvatarRegistry

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
    # Each input is allowed to pass through only one mechanism.
    # The first successful fix wins, so the same string is never rewritten twice.
    for fix_name, fixer in fixers.items():
        if fixed_string := fixer.fix(avatar_string):
            return fix_name, fixed_string


def build_fixers_map(registry: AvatarRegistry) -> dict[str, "AvatarFixer"]:
    """
    Build a dictionary mapping fix names to their :class:`AvatarFixer` instances.

    :param registry: Avatar registry passed to :class:`AvatarFixer`.
    :type registry: :class:`AvatarRegistry`

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
    fixers["empty Battlesuit ID"]     = AvatarFixer(registry, EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["empty Battlesuit ID"].replacement_map, cls=DataclassEncoder, indent=4))
    fixers["too short Battlesuit ID"] = AvatarFixer(registry, TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["too short Battlesuit ID"].replacement_map, cls=DataclassEncoder, indent=4))
    fixers["too short Valkyrie ID"]   = AvatarFixer(registry, TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["too short Valkyrie ID"].replacement_map, cls=DataclassEncoder, indent=4))
    fixers["misspelled note"]           = AvatarFixer(registry, WRONG_NOTE_REPLACEMENT_MAP)
    # print(json.dumps(fixers["misspelled note"].replacement_map, cls=DataclassEncoder, indent=4))

    # Prefix replacements
    fixers["wrong Battlesuit ID"] = PrefixFixer(registry, WRONG_BATTLESUIT_ID_REPLACEMENT_MAP)
    # print(json.dumps(fixers["wrong Battlesuit ID"].replacement_map, cls=DataclassEncoder, indent=4))

    return fixers


__all__ = ["title_case", "fix_avatar_string", "build_fixers_map"]
