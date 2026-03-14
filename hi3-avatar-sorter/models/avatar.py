from annotationlib import ForwardRef
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Self, TypedDict, get_args, get_origin

from frozendict import frozendict


def _evaluate_type_argument(cls: type, parent: type) -> type:
    orig_bases = cls.__orig_bases__
    if len(orig_bases) != 1:
        raise TypeError

    base = orig_bases[0]
    if get_origin(base) is not parent:
        raise TypeError

    type_arg: type | ForwardRef = get_args(base)[0]
    if isinstance(type_arg, type):
        return type_arg
    else:
        return type_arg.evaluate(owner=cls)


@dataclass(kw_only=True)
class BaseModel:
    id: str
    no: int = field(default=None) # pyright: ignore[reportAssignmentType]

    id_length: ClassVar[int]

    @classmethod
    def _validate_id(cls, id: str) -> None:
        pass

    def __int__(self) -> int:
        return self.no

    def __str__(self) -> str:
        return f"№{int(self)}"


class Container[Child: "BaseModel"](BaseModel):
    _children_type: type["Child"]
    _children: dict[str, "Child"]

    def __init_subclass__(cls, evaluate_children_type: bool = True):
        super().__init_subclass__()

        if evaluate_children_type:
            cls._children_type = _evaluate_type_argument(cls, Container)

    def _add_child(self, child: "Child") -> None:
        ...

    def _reserve_child(self, child: "Child") -> None:
        ...

    def _get_or_create_child(self, child_id: str) -> "Child":
        try:
            return self._children[child_id]
        except KeyError:
            return self._children_type(id=child_id)


class ClassContainer[Child: "BaseModel"](Container[Child], evaluate_children_type=False):
    _children_type: ClassVar[type["Child"]] # pyright: ignore[reportIncompatibleVariableOverride, reportGeneralTypeIssues]
    _children: ClassVar[dict[str, "Child"]] # pyright: ignore[reportIncompatibleVariableOverride, reportGeneralTypeIssues]

    def __init_subclass__(cls, evaluate_children_type: bool = True):
        super().__init_subclass__(evaluate_children_type=False)

        if evaluate_children_type:
            cls._children_type = _evaluate_type_argument(cls, Container) # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def _add_child(cls, child: "Child") -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        ...

    @classmethod
    def _reserve_child(cls, child: "Child") -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        ...

    @classmethod
    def _get_or_create_child(cls, child_id: str) -> "Child": # pyright: ignore[reportIncompatibleMethodOverride]
        try:
            return cls._children[child_id]
        except KeyError:
            return cls._children_type(id=child_id)


class Skin(BaseModel):
    pass


@dataclass(kw_only=True)
class SkinRarity(Container[Skin]):
    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__init_subclass__
    skins: "frozendict[int, Skin]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_skin` method
    """

    def add_skin(self, skin: "Skin") -> None:
        return self._add_child(skin)

    def reserve_skin(self, skin: "Skin") -> None:
        return self._reserve_child(skin)

    def get_or_create_skin(self, skin_id: str) -> "Skin":
        return self._get_or_create_child(skin_id)

@dataclass(kw_only=True)
class Battlesuit(Container[SkinRarity]):
    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__init_subclass__
    skin_rarities: "frozendict[int, SkinRarity]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_skin_rarity` method
    """

    def add_skin_rarity(self, skin_rarity: "SkinRarity") -> None:
        return self._add_child(skin_rarity)

    def reserve_skin_rarity(self, skin_rarity: "SkinRarity") -> None:
        return self._reserve_child(skin_rarity)

    def get_or_create_skin_rarity(self, skin_rarity_id: str) -> "SkinRarity":
        return self._get_or_create_child(skin_rarity_id)

@dataclass(kw_only=True)
class Valkyrie(Container[Battlesuit]):
    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__init_subclass__
    battlesuits: "frozendict[int, Battlesuit]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_battlesuit` method
    """

    def add_battlesuit(self, battlesuit: "Battlesuit") -> None:
        return self._add_child(battlesuit)

    def reserve_battlesuit(self, battlesuit: "Battlesuit") -> None:
        return self._reserve_child(battlesuit)

    def get_or_create_battlesuit(self, battlesuit_id: str) -> "Battlesuit":
        return self._get_or_create_child(battlesuit_id)

@dataclass(kw_only=True)
class Part(Container[Valkyrie]):
    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__init_subclass__
    valkyries: "frozendict[int, Valkyrie]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_valkyrie` method
    """

    def add_valkyrie(self, valkyrie: "Valkyrie") -> None:
        return self._add_child(valkyrie)

    def reserve_valkyrie(self, valkyrie: "Valkyrie") -> None:
        return self._reserve_child(valkyrie)

    def get_or_create_valkyrie(self, valkyrie_id: str) -> "Valkyrie":
        return self._get_or_create_child(valkyrie_id)


class RawAvatar(TypedDict):
    part_id:        str
    valkyrie_id:    str
    battlesuit_id:  str
    skin_rarity_id: str | None
    skin_id:        str | None
    note:           str | None


@dataclass(kw_only=True)
class Avatar(ClassContainer[Part]):
    id: str = field(init=False)

    part:        "Part"
    valkyrie:    "Valkyrie"
    battlesuit:  "Battlesuit"
    skin_rarity: "SkinRarity | None" = None
    skin:        "Skin       | None" = None
    note:        "str        | None" = None


    def reserve(self):
        # self.reserve_part(self.part)
        # self.part.reserve_valkyrie(self.valkyrie)
        self.valkyrie.reserve_battlesuit(self.battlesuit)

        if self.skin_rarity is not None and self.skin is not None:
            self.battlesuit.reserve_skin_rarity(self.skin_rarity)
            self.skin_rarity.reserve_skin(self.skin)

    def register(self):
        # self.add_part(self.part)
        # self.part.add_valkyrie(self.valkyrie)
        self.valkyrie.add_battlesuit(self.battlesuit)

        if self.skin_rarity is not None and self.skin is not None:
            self.battlesuit.add_skin_rarity(self.skin_rarity)
            self.skin_rarity.add_skin(self.skin)


    @classmethod
    def from_file(
        cls,
        file: str | Path
    ) -> Self:
        raw_avatar = cls._raw_from_file(file)
        self = cls.from_raw(**raw_avatar)
        self.register()

        return self

    @classmethod
    def from_raw(
        cls,
        part_id:        str,
        valkyrie_id:    str,
        battlesuit_id:  str,
        skin_rarity_id: str | None,
        skin_id:        str | None,
        note:           str | None
    ):
        part = cls.get_or_create_part(part_id)
        valkyrie = part.get_or_create_valkyrie(valkyrie_id)
        battlesuit = valkyrie.get_or_create_battlesuit(battlesuit_id)

        if skin_rarity_id is not None and skin_id is not None:
            skin_rarity = battlesuit.get_or_create_skin_rarity(skin_rarity_id)
            skin = skin_rarity.get_or_create_skin(skin_id)
        else:
            skin_rarity = skin = None

        if note is not None:
            note = cls.format_note(note)
        # else:
        #     note = None

        return cls(
            part=part,
            valkyrie=valkyrie,
            battlesuit=battlesuit,
            skin_rarity=skin_rarity,
            skin=skin,
            note=note
        )


    @classmethod
    def format_note(
        cls,
        note: str | None
    ) -> str:
        if not note:
            raise EmptyNoteError(note)

        if note.lower() == "b":
            note = "Veliona"

        return note.capitalize()


    @classmethod
    def get_or_create_part(cls, part_id: str) -> "Part":
        return cls._get_or_create_child(part_id)

    # We don't use default_factory here because this field
    # will be replaced by _children in Container.__init_subclass__
    parts: "frozendict[int, Part]" = field(default=frozendict())
    """
    This field should not be updated from outside.
    Instead, use the `add_part` method
    """
    @classmethod
    def add_part(cls, part: "Part") -> None:
        return cls._add_child(part)


    @classmethod
    def _raw_from_file(
        cls,
        file: str | Path
    ) -> RawAvatar:
        file_name = Path(file).name

        if not file_name:
            raise EmptyFileNameError(file_name)

        name_parts = file_name.split("_", maxsplit=3)

        skin_rarity_id: str | None = None
        skin_id:        str | None = None
        note:           str | None = None

        match name_parts:
            # Length is 0: Invalid file name (empty string or "_")
            case []:
                raise MissingAvatarIdError(file_name)

            # Length is 1: Only avatar ID
            case [avatar_id]:
                pass

            # Length is 2: Avatar ID with a note
            case [avatar_id, note]:
                pass

            # Length is 3: Avatar ID with a skin
            case [avatar_id, skin_rarity_id, skin_id]:
                pass

            # Length is 4: Avatar ID with a skin and a note
            case [avatar_id, skin_rarity_id, skin_id, note]:
                pass

            # Length is 5: Unreachable because max length here is 4 (maxsplit+1)
            case _:
                raise AssertionError("This code should be unreachable")

        avatar_id = avatar_id.rjust(cls.id_length, "0")

        # The same as len(avatar_id) != cls.id_length:
        if len(avatar_id) >= cls.id_length:
            raise AvatarIdTooLongError(avatar_id, file_name)

        # part_id, valkyrie_id, and battlesuit_id appear next to each other in avatar_id
        pos = 0

        part_id = avatar_id[pos:pos + Part.id_length]
        pos += Part.id_length

        valkyrie_id = avatar_id[pos:pos + Valkyrie.id_length]
        pos += Valkyrie.id_length

        battlesuit_id = avatar_id[pos:pos + Battlesuit.id_length]

        return {
            "part_id":        part_id,
            "valkyrie_id":    valkyrie_id,
            "battlesuit_id":  battlesuit_id,
            "skin_rarity_id": skin_rarity_id,
            "skin_id":        skin_id,
            "note":           note
        }


    def __iter__(self) -> Iterator[int | str]:
        result = (self.part.no, self.valkyrie.id, self.battlesuit.id)

        if self.skin_rarity is not None and self.skin is not None:
            result += (self.skin_rarity.id, self.skin.id)

        if self.note:
            result += (self.note,)

        return iter(result)

    def __int__(self) -> int:
        # Example: 010203_04_05_Special
        result = f"{int(self.part):02}{int(self.valkyrie):02}{self.battlesuit:02}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f", {self.skin_rarity} {self.skin}"

        if self.note:
            result += f", {self.note}"

        return int(result)

    def __str__(self) -> str:
        # Example: Raiden Mei №3, Skin 4★ №5, Special
        result = f"{self.valkyrie} {self.battlesuit}"

        if self.skin_rarity is not None and self.skin is not None:
            result += f", {self.skin_rarity} {self.skin}"

        if self.note:
            result += f", {self.note}"

        return result
