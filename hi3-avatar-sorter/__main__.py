from pathlib import Path

from . import PART1_VALKYRIES, PART2_VALKYRIES
from .errors import ParsingError
from .models import Avatar
from .models.valkyrie import build_valkyrie_map
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

replacement_table: dict[AvatarTuple, AvatarTuple] = {
    # Beach avatars do not have battlesuit IDs
    (PART1, KIANA,   "", 4, 1): (PART1, KIANA,   1, 4, 1),
    (PART1, KIANA,   "", 4, 1): (PART1, KIANA,   1, 4, 1),
    (PART1, MEI,     "", 4, 1): (PART1, MEI,     1, 4, 1),
    (PART1, MEI,     "", 4, 1): (PART1, MEI,     1, 4, 1),
    (PART1, BRONYA,  "", 4, 1): (PART1, BRONYA,  1, 4, 1),
    (PART1, BRONYA,  "", 4, 1): (PART1, BRONYA,  1, 4, 1),
    (PART1, THERESA, "", 4, 1): (PART1, THERESA, 1, 4, 1),
    (PART1, THERESA, "", 4, 1): (PART1, THERESA, 1, 4, 1),
    (PART1, HIMEKO,  "", 4, 1): (PART1, HIMEKO,  1, 4, 1),
    (PART1, HIMEKO,  "", 4, 1): (PART1, HIMEKO,  1, 4, 1),

    # This avatar's battlesuit ID is 1 character long instead of 2
    (PART1, SAKURA, 1, 4, 1): (PART1, SAKURA, 1, 4, 1),

    # This avatar's Valkyrie ID is 1 character long instead of 2
    (PART1, KIANA, 15, 4, 1): (PART1, KIANA, 15, 4, 1),

    # HoV is 5th Kiana, not 3rd Kallen
    (PART1, KALLEN, 13): (PART1, KIANA, 5),

    # 3rd Elysia battlesuit is not a new character
    (PART2, ELYSIA_P2, 1): (PART1, ELYSIA_P1, 3),

    # This avatar has wrong battlesuit ID
    (PART1, RITA, 1, "Special"): (PART1, RITA, 3, "Special"),

    # NOTE#1:
    # Because Kallen and Kiana are completely messed up,
    # Kallen's battlesuits were shifted to the 50s range to
    # free some ID space for future Kiana battlesuits
    #
    # IMPORTANT: For this fix to work, Kiana's max
    # battlesuit ID must also be set to 50 in the Valkyrie DB
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
    output_folder: str | Path = "output"
):
    source_folder, output_folder = validate_paths(source_folder, output_folder)
    build_valkyrie_db(PART1_VALKYRIES, PART2_VALKYRIES)

    for file in sorted(source_folder.iterdir()):
        if not file.is_file():
            continue

        try:
            avatar = Avatar.from_string(file.stem)
        except ParsingError as e:
            print(f"\033[7m[SKIP]\033[0m {file.stem}: {str(e)}")
        else:
            print(f"{file.stem}:")
            print(avatar)


if __name__ == "__main__":
    main(input("Enter source folder path: "))
