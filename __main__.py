# from typing import Any

# from . import PART1, PART2
# from .models import Avatar, Valkyrie


# KIANA = KALLEN = 1
# MEI = SAKURA = 2
# BRONYA = 3
# THERESA = 4
# HIMEKO = 5
# RITA = 7
# ELYSIA_P2 = 10
# ELYSIA_P1 = 22


# renaming_table: dict[str | Avatar, Avatar] = {
#     "601_04_01":
# }


# renaming_table = {
#     (PART1, RITA, 1, "Special"): Avatar(PART1, RITA, 3, note="Special", reserve=True),

#     # 3rd Elysia battlesuit is not a new character
#     (PART2, ELYSIA_P2, 1): Avatar(PART1, ELYSIA_P1, 3, reserve=True),

#     # Beach skins
#     "601_04_01": Avatar(PART1, KIANA, 1, 4, 1, reserve=True),

#     "602_04_01": Avatar(PART1, MEI, 1, 4, 1, reserve=True),

#     # (PART1, BRONYA, 1, 4, 1): Avatar(PART1, BRONYA, 1, 4, 2, reserve=True),
#     "603_04_01": Avatar(PART1, BRONYA, 1, 4, 1, reserve=True),

#     # (PART1, THERESA, 1, 4, 1): Avatar(PART1, THERESA, 1, 4, 2, reserve=True),
#     "604_04_01": Avatar(PART1, THERESA, 1, 4, 1, reserve=True),

#     # (PART1, HIMEKO, 1, 4, 2): Avatar(PART1, HIMEKO, 1, 4, 3, reserve=True),
#     # (PART1, HIMEKO, 1, 4, 1): Avatar(PART1, HIMEKO, 1, 4, 2, reserve=True),
#     "605_04_01": Avatar(PART1, HIMEKO, 1, 4, 1, reserve=True),

#     "6021_04_01": Avatar(PART1, SAKURA, 1, 4, 1, reserve=True),

#     "6115_04_01": Avatar(PART1, KIANA, 15, 4, 1, reserve=True),

#     # Kiana can sometimes be Kallen yk
#     # (PART1, KIANA, 6) : Avatar(PART1, KIANA, 7, reserve=True),
#     # (PART1, KIANA, 5) : Avatar(PART1, KIANA, 6, reserve=True),
#     (PART1, KALLEN, 13): Avatar(PART1, KIANA, 5, reserve=True),
#     (PART1, KALLEN, 15): Avatar(PART1, KIANA, 8)
# }

# a = Avatar.from_file("60106")
# print("Avatar(PART" + ", ".join(map(str, tuple(a))) + ")")
# # print(black.format_str(pformat(vars(a, reserve=True), indent=4, reserve=True), mode=black.Mode()))

# TODO: переделать таблицу замен (как-то надо матчить либо текст к аватару, либо аватар к аватару и всегда резервировать аватар справа через Avatar.reserve())
# TODO: проверить цепляются ли скины к зарезервированным сьютам
# TODO: __main__
# TODO: придумать как отображать аватар в ошибках вида ReserveMissing...No
# TODO: придумать алгоритм обратного поиска файла по наследникам класса OneToMany путём создания некой регулярки и поиска файлов, соответствующей ей (вероятно, можно будет прописать ещё целевые папки)
