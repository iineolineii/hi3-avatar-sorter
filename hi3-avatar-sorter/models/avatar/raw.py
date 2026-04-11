from collections.abc import Iterable
from dataclasses import asdict, dataclass, replace
from typing import Self

from ..base import BaseModel
from ..battlesuit import Battlesuit
from ..part import Part
from ..skin import Skin
from ..skin_rarity import SkinRarity
from ..valkyrie import Valkyrie
from ...errors import (
    MissingAvatarIDError,
    MissingBattlesuitIDError,
    MissingPartIDError,
    MissingSkinIDError,
    MissingSkinRarityIDError,
    MissingValkyrieIDError,
    TooLongSuffixError
)


@dataclass(frozen=True, slots=True)
class RawAvatar:
    """
    An immutable raw representation of an avatar.

    Represents parsed input data in a normalized,
    low-level form before it is transformed
    into the `Avatar` model.
    """
    part_id:        str
    valkyrie_id:    str
    battlesuit_id:  str
    skin_rarity_id: str | None = None
    skin_id:        str | None = None
    note:           str | None = None

    @property
    def id(self) -> str:
        """
        Normalized Avatar ID as a concatenation of `part_id`,
        `valkyrie_id`, and `battlesuit_id`.
        """
        return f"{self.part_id}{self.valkyrie_id}{self.battlesuit_id}"


    @classmethod
    def validate_id(cls, id: str) -> str:
        """
        Validate and normalize given Avatar ID.

        Args:
            id (`str`): ID to validate.

        Returns:
            `str`: The validated and normalized ID.
        """
        return object.__getattribute__(BaseModel, "validate_id").__wrapped__(cls, id)

    def validated(self) -> Self:
        """
        Return a copy of this instance with all of its fields validated and normalized.

        Raises:
            `MissingSkinIDError`:
                If `skin_rarity_id` is provided but `skin_id` is missing.

            `MissingSkinRarityIDError`:
                If `skin_id` is provided without `skin_rarity_id`.

        Returns:
            `Self`: The validated and normalized model instance.
        """
        validated_fields: dict[str, str] = {}

        validated_fields["part_id"] = Part.validate_id(self.part_id)
        validated_fields["valkyrie_id"] = Valkyrie.validate_id(self.valkyrie_id)
        validated_fields["battlesuit_id"] = Battlesuit.validate_id(self.battlesuit_id)

        match (self.skin_rarity_id, self.skin_id):
            case (_, None):
                raise MissingSkinIDError(asdict(self))

            case (None, _):
                raise MissingSkinRarityIDError(asdict(self))

            case _:
                validated_fields["skin_rarity_id"] = SkinRarity.validate_id(self.skin_rarity_id)
                validated_fields["skin_id"] = Skin.validate_id(self.skin_id)

        return type(self)(**validated_fields)


    @classmethod
    def from_string(cls, string: str, validate: bool = True) -> Self:
        """
        Parse a raw avatar from a string representation.

        Args:
            string (`str`):
                Source string in one of the supported raw avatar formats.

            validate (`bool`, *optional*):
                Whether to validate the parsed result.
                Defaults to `True`.

        Raises:
            `MissingAvatarIDError`:
                If the string does not contain an avatar identifier.

        Returns:
            `Self`: Parsed raw avatar.
        """
        parts = string.split("_", maxsplit=3)

        if not parts:
            raise MissingAvatarIDError(string)

        avatar_id, *suffix = parts
        part_id, valkyrie_id, battlesuit_id = cls.parse_id(avatar_id)
        skin_rarity_id, skin_id, note = cls.parse_suffix(suffix)

        raw = cls(part_id, valkyrie_id, battlesuit_id, skin_rarity_id, skin_id, note)

        if validate:
            return raw.validated()

        return raw

    @classmethod
    def from_iterable(
        cls,
        iterable: Iterable[int | str],
        validate: bool = True,
        validate_string_ids: bool = True
    ) -> Self:
        items = list(iterable)

        match items:
            case [part_id, valkyrie_id, battlesuit_id, *suffix]:
                pass

            case [part_id, valkyrie_id]:
                raise MissingBattlesuitIDError(iterable)

            case [part_id]:
                raise MissingValkyrieIDError(iterable)

            case _:
                raise MissingPartIDError(iterable)

        string_fields: dict[str, str] = {}

        def coerce(name: str, value: int | str | None) -> str: # pyright: ignore[reportReturnType]
            if value is not None:
                if validate_string_ids and isinstance(value, str):
                    string_fields[name] = value

                return str(value)

        skin_rarity_id, skin_id, note = cls.parse_suffix(suffix) # pyright: ignore[reportArgumentType]

        raw = cls(
            coerce("part_id", part_id),
            coerce("valkyrie_id", valkyrie_id),
            coerce("battlesuit_id", battlesuit_id),
            coerce("skin_rarity_id", skin_rarity_id),
            coerce("skin_id", skin_id),
            note
        )

        if not validate:
            return raw

        validated = raw.validated()

        if not validate_string_ids:
            return validated

        return replace(validated, **string_fields)


    @classmethod
    def parse_id(cls, id: str) -> tuple[str, str, str]:
        """
        Parse `part_id`, `valkyrie_id`, and `battlesuit_id` from given Avatar ID.

        Args:
            id (`str`):
                The ID to parse.

        Returns:
            `tuple[str, str, str]`: `part_id`, `valkyrie_id`, and `battlesuit_id`.
        """
        id = cls.validate_id(id)

        # Part ID, Valkyrie ID, and Battlesuit ID appear next to each other in the Avatar ID
        pos = 0
        part_id       = id[pos:pos+Part.id_length]

        pos += Part.id_length
        valkyrie_id   = id[pos:pos+Valkyrie.id_length]

        pos += Valkyrie.id_length
        battlesuit_id = id[pos:pos+Battlesuit.id_length]

        return part_id, valkyrie_id, battlesuit_id

    @classmethod
    def parse_suffix(cls, suffix: Iterable[str]) -> (
        tuple[None, None, None] |
        tuple[None, None, str ] |
        tuple[str,  str,  None] |
        tuple[str,  str,  str ]
    ):
        """
        Parse `skin_rarity_id`, `skin_id`, and `note` from the optional suffix of a raw input data.

        Args:
            suffix (`Iterable[str]`):
                Remaining input data components after the Avatar ID.

        Raises:
            `TooLongSuffixError`:
                If the suffix contains more than three elements.

        Returns:
            - `tuple[None, None, None]`: If the suffix is empty.

            - `tuple[None, None, str ]`: If the suffix contains only `note`.

            - `tuple[str, str, None]`: If the suffix contains `skin_rarity_id` and `skin_id` without `note`.

            - `tuple[str, str, str ]`: If the suffix contains `skin_rarity_id`, `skin_id`, and `note`.
        """
        skin_rarity_id: str | None = None
        skin_id:        str | None = None
        note:           str | None = None

        suffix = list(suffix)

        match suffix:
            case [skin_rarity_id, skin_id, note]:
                pass

            case [skin_rarity_id, skin_id]:
                pass

            case [note]:
                pass

            case []:
                pass

            case _:
                raise TooLongSuffixError(suffix)

        return skin_rarity_id, skin_id, note # pyright: ignore[reportReturnType]


    def __str__(self) -> str:
        # Example: 60203_04_05_Special
        result = self.id

        if self.skin_rarity_id is not None and self.skin_id is not None:
            result += f"_{self.skin_rarity_id}_{self.skin_id}"

        if self.note:
            result += f"_{self.note}"

        return result


    def __int__(self):
        result = self.id

        if self.skin_rarity_id is not None and self.skin_id is not None:
            result += self.skin_rarity_id
            result += self.skin_id
        else:
            result += "0000"

        return int(result)


__all__ = ["RawAvatar"]
