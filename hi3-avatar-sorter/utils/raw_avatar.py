from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Any, ClassVar, final

from ..errors import EmptyNoteError, MissingFieldError, TooLongSuffixError
from ..models import BaseModel, Battlesuit, Part, Skin, SkinRarity, Valkyrie

if TYPE_CHECKING:
    from typing_extensions import Self

    from ..fixers.types import AvatarComponents
    from ..registry import AvatarRegistry


# TODO: Improve validation documentation
@final
@dataclass(frozen=True)
class RawAvatar:
    part_id:        str
    valkyrie_id:    str
    battlesuit_id:  str
    skin_rarity_id: str | None = None
    skin_id:        str | None = None
    note:           str | None = None

    fixed: bool = False
    known_notes: ClassVar[dict[str, int]] = {}
    id_length: ClassVar[int] = Part.id_length + Valkyrie.id_length + Battlesuit.id_length

    @property
    def id(self) -> str:
        """
        Normalized Avatar ID as a concatenation of `part_ID`,
        `valkyrie_ID`, and `battlesuit_ID`.
        """
        return f"{self.part_id}{self.valkyrie_id}{self.battlesuit_id}"


    @classmethod
    def from_components(
        cls,
        components: "AvatarComponents",
        registry: "AvatarRegistry",
        *,
        preserve_strings: bool = False
    ) -> Iterator["RawAvatar"]:
        part_no, valkyrie_id, battlesuit_id, *suffix = components
        skin_rarity_id, skin_id, note = cls._parse_suffix(suffix, preserve_strings)

        parts = registry.parts_by_no[part_no]
        valkyrie_id   = cls._validate_id(valkyrie_id,   preserve_strings=preserve_strings, model=Valkyrie  )
        battlesuit_id = cls._validate_id(battlesuit_id, preserve_strings=preserve_strings, model=Battlesuit)

        for part in parts:
            yield RawAvatar(
                part_id        = part.id,
                valkyrie_id    = valkyrie_id,
                battlesuit_id  = battlesuit_id,
                skin_rarity_id = skin_rarity_id,
                skin_id        = skin_id,
                note           = note
            )


    @classmethod
    def from_string(cls, string: str) -> "Self":
        components = string.split("_", maxsplit=3)

        if not components or not components[0]:
            raise MissingFieldError("Avatar ID", string)

        avatar_id, *suffix = components
        part_id, valkyrie_id, battlesuit_id = cls._parse_id(avatar_id)
        skin_rarity_id, skin_id, note = cls._parse_suffix(suffix, preserve_strings=False)

        return cls(
            part_id,
            valkyrie_id,
            battlesuit_id,
            skin_rarity_id,
            skin_id,
            note
        )


    @classmethod
    def _parse_id(cls, id: str) -> tuple[str, str, str]:
        """
        Parse `part_ID`, `valkyrie_ID`, and `battlesuit_ID` from given Avatar ID.

        :param ID: The ID to parse.
        :type ID: str

        :return: A tuple containing `part_ID`, `valkyrie_ID`, and `battlesuit_ID`.
        :rtype: tuple[str, str, str]
        """
        id = cls._validate_id(id)

        # Part ID, Valkyrie ID, and Battlesuit ID appear next to each other in the Avatar ID
        pos = 0
        part_id       = str(id[pos:pos+Part.id_length])

        pos += Part.id_length
        valkyrie_id   = id[pos:pos+Valkyrie.id_length]

        pos += Valkyrie.id_length
        battlesuit_id = id[pos:pos+Battlesuit.id_length]

        return part_id, valkyrie_id, battlesuit_id


    @classmethod
    def _parse_suffix(
        cls,
        suffix: Sequence[int | str],
        preserve_strings: bool
    ) -> (
        tuple[None, None, None] |
        tuple[None, None, str ] |
        tuple[str,  str,  None] |
        tuple[str,  str,  str ]
    ):
        """
        Parse `skin_rarity_ID`, `skin_ID`, and `note` from the optional suffix of a raw input data.

        :param suffix: Remaining input data components following the Avatar ID.
        :type suffix: Sequence[int | str]

        :return:
            A tuple depending on the contents of the suffix:

            - (`None`, `None`, `None`):
                If the suffix is empty.

            - (`None`, `None`, `str`):
                If the suffix contains only `note`.

            - (`str`, `str`, `None`):
                If the suffix contains `skin_rarity_ID` and `skin_ID` without `note`.

            - (`str`, `str`, `str`):
                If the suffix contains `skin_rarity_ID`, `skin_ID`, and `note`.

        :rtype:
            tuple[None, None, None] |
            tuple[None, None, str ] |
            tuple[str,  str,  None] |
            tuple[str,  str,  str ]
        """
        skin_rarity_id: int | str | None = None
        skin_id:        int | str | None = None
        note:           int | str | None = None

        match suffix:
            case [skin_rarity_id, skin_id, note]:
                skin_rarity_id = cls._validate_id(skin_rarity_id, preserve_strings=preserve_strings, model=SkinRarity)
                skin_id = cls._validate_id(skin_id, preserve_strings=preserve_strings, model=Skin)
                note = cls._validate_note(note)

                return (skin_rarity_id, skin_id, note)

            case [skin_rarity_id, skin_id]:
                skin_rarity_id = cls._validate_id(skin_rarity_id, preserve_strings=preserve_strings, model=SkinRarity)
                skin_id = cls._validate_id(skin_id, preserve_strings=preserve_strings, model=Skin)

                return (skin_rarity_id, skin_id, note)

            case [note]:
                note = cls._validate_note(note)

                return (skin_rarity_id, skin_id, note)

            case []:
                return (skin_rarity_id, skin_id, note)

            case _:
                raise TooLongSuffixError(suffix)


    @classmethod
    def _validate_id(
        cls,
        id: int | str,
        *,
        preserve_strings: bool = False,
        model: type["BaseModel"] | None = None
    ) -> str:
        if model is None:
            validator = partial(BaseModel._validate_id.__func__, cls)
        else:
            validator = model._validate_id

        if isinstance(id, str) and preserve_strings:
            return str(id)

        return validator(id)


    @classmethod
    def _validate_note(cls, note: Any) -> str:
        if not isinstance(note, str):
            raise TypeError # TODO: Custom exception class

        if not note:
            raise EmptyNoteError(note)

        if note not in cls.known_notes:
            cls.known_notes[note] = len(cls.known_notes)

        return note


    def __repr__(self) -> str:
        # Example: 60203_04_05_Special
        result = self.id

        if self.skin_rarity_id is not None and self.skin_id is not None:
            result += f"_{self.skin_rarity_id}_{self.skin_id}"

        if self.note:
            result += f"_{self.note}"

        return result.lstrip("0")


    def __int__(self):
        result = self.id

        if self.skin_rarity_id is not None and self.skin_id is not None:
            result += str(self.skin_rarity_id)
            result += str(self.skin_id)
        else:
            result += "0" * SkinRarity.id_length
            result += "0" * Skin.id_length

        if self.note is not None:
            note_index = self.known_notes[self.note]
            result += str(note_index+1)
        else:
            result += "0"

        if self.fixed:
            result += "1"
        else:
            result += "0"

        return int(result)
