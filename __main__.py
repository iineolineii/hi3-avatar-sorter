from . import PART1, PART2
from .models import Avatar, Part


KIANA = KALLEN = 1
MEI = SAKURA = 2
BRONYA = 3
THERESA = 4
HIMEKO = 5
RITA = 7
ELYSIA_P2 = 10
ELYSIA_P1 = 22


RawAvatarWithNote = tuple[Part, int, int, str]
RawAvatarWithSkinAndNote = tuple[Part, int, int, int, int, str]
RawAvatarWithSkin = tuple[Part, int, int, int, int]
RawAvatar = tuple[Part, int, int]

AvatarTuple = RawAvatar | RawAvatarWithNote | RawAvatarWithSkin | RawAvatarWithSkinAndNote

renaming_table: dict[str | AvatarTuple | Avatar, str | AvatarTuple | Avatar] = {
    (PART1, RITA, 1, "Special"): (PART1, RITA, 3, "Special"),

    # 3rd Elysia battlesuit is not a new character
    (PART2, ELYSIA_P2, 1): (PART1, ELYSIA_P1, 3),

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
    (PART1, KALLEN, 11): (PART1, KALLEN, 11+40),
    (PART1, KALLEN, 12): (PART1, KALLEN, 12+40),
    (PART1, KALLEN, 14): (PART1, KALLEN, 14+40)
}


# avatar = Avatar.from_file("60106")
# print("Avatar(PART" + ", ".join(map(str, tuple(avatar))) + ")")
# # print(black.format_str(pformat(vars(avatar, reserve=True), indent=4, reserve=True), mode=black.Mode()))

# TODO: __main__
# TODO: научиться парсить таблицу замен (детей аватара справа нужно инициализировать сразу с номерами, а потом вызывать Avatar.reserve())
# TODO: проверить сдвиг по mex (безопасно ли убирать закомментированные строки в таблице замен?)
# TODO: придумать алгоритм обратного поиска файла по наследникам класса OneToMany путём создания некой регулярки и поиска файлов, соответствующей ей (вероятно, можно будет прописать ещё целевые папки)
