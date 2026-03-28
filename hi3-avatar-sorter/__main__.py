from pathlib import Path
from typing import Literal

from . import PART1_VALKYRIES, PART2_VALKYRIES
from .models import Avatar
from .models.part import build_valkyrie_db
from .utils import validate_paths


PART1 = 1
PART2 = 2

KIANA = KALLEN = 1
MEI = SAKURA = 2
BRONYA = 3
THERESA = 4
HIMEKO = 5
RITA = 7
ELYSIA_P2 = 10
ELYSIA_P1 = 22

RawAvatarWithNote = tuple[int | str, int | str, int | str, str]
RawAvatarWithSkinAndNote = tuple[int | str, int | str, int | str, int | str, int | str, str]
RawAvatarWithSkin = tuple[int | str, int | str, int | str, int | str, int | str]
RawAvatar = tuple[int | str, int | str, int | str]

AvatarTuple = RawAvatar | RawAvatarWithNote | RawAvatarWithSkin | RawAvatarWithSkinAndNote

replacement_table: dict[str | AvatarTuple | Avatar, str | AvatarTuple | Avatar] = {
    # 3rd Elysia battlesuit is not a new character
    (PART2, ELYSIA_P2, 1): (PART1, ELYSIA_P1, 3),

    #
    (PART1, RITA, 1, "Special"): (PART1, RITA, 3, "Special"),

    # Beach skins
    "601_04_01": (PART1, KIANA, 1, 4, 1),

    "602_04_01": (PART1, MEI, 1, 4, 1),

    # (PART1, BRONYA, 1, 4, 1): (PART1, BRONYA, 1, 4, 2),
    "603_04_01": (PART1, BRONYA, 1, 4, 1),

    # (PART1, THERESA, 1, 4, 1): (PART1, THERESA, 1, 4, 2),
    "604_04_01": (PART1, THERESA, 1, 4, 1),

    # (PART1, HIMEKO, 1, 4, 2): (PART1, HIMEKO, 1, 4, 3),
    # (PART1, HIMEKO, 1, 4, 1): (PART1, HIMEKO, 1, 4, 2),
    "605_04_01": (PART1, HIMEKO, 1, 4, 1),

    "6021_04_01": (PART1, SAKURA, 1, 4, 1),

    "6115_04_01": (PART1, KIANA, 15, 4, 1),

    # HoV is 5th Kiana, not 3rd Kallen
    # (PART1, KIANA, 6) : (PART1, KIANA, 7),
    # (PART1, KIANA, 5) : (PART1, KIANA, 6),
    (PART1, KALLEN, 13): (PART1, KIANA, 5),

    # NOTE#1:
    # Kallen battlesuits were shifted to the 50s range to
    # free some ID space for future Kiana battlesuits
    #
    # IMPORTANT: Kiana's max battlesuit ID must also be
    # set to 50 in the Valkyrie DB
    #
    # EDGE CASE: Unrealistically to happen, but in case of
    # a new Kallen battlesuit, the below list should be
    # extended accordingly
    (PART1, KALLEN, 11): (PART1, KALLEN, 40+11),
    (PART1, KALLEN, 12): (PART1, KALLEN, 40+12),
    (PART1, KALLEN, 14): (PART1, KALLEN, 40+14)
}


def main(
    source_folder: str | Path,
    output_folder: str | Path = "output",
    format: Literal["short", "long"] = "long"
):
    source_folder, output_folder = validate_paths(source_folder, output_folder)
    build_valkyrie_db(PART1_VALKYRIES, PART2_VALKYRIES)

    for file in source_folder.iterdir():
        # _, avatar_raw = Avatar._raw_from_file(file, format)
        avatar = Avatar.from_file(file)
