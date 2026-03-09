from .models import Part
from .valkyrie_db import ValkyrieDatabase

PART1_VALKYRIES = [
    ( 1, "Kiana Kaslana",      10 ),
    ( 1, "Kallen Kaslana",        ),
    ( 2, "Raiden Mei",         10 ),
    ( 2, "Yae Sakura",            ),
    ( 3, "Bronya Zaychik",        ),
    ( 4, "Murata Himeko",      20 ),
    ( 4, "Liliya Olenyeva",    21 ),
    ( 4, "Rozaliya Olenyeva",     ),
    ( 5, "Theresa Apocalypse",    ),
    ( 6, "Fu Hua",                ),
    ( 7, "Rita Rossweisse",    10 ),
    ( 7, "Seele Vollerei",        ),
    ( 8, "Durandal",              ),
    ( 9, "Asuka",                 ),
    (20, "Keqing",                ),
    (21, "Fischl",                ),
    (22, "Elysia",                ),
    (23, "Mobius",                ),
    (24, "Natasha Cioara",        ),
    (25, "Carole Pepper",         ),
    (26, "Pardofelis",            ),
    (27, "Aponia",                ),
    (28, "Eden",                  ),
    (29, "Griseo",                ),
    (30, "Vill-V",                ),
    (31, "Li Sushang",            ),
    (32, "Ai Hyperion Λ",         ),
    (33, "Susannah Manatt",       ),
    (34, "Misteln Schariac",      ),
    (35, "PROMETHEUS",            ),
    (36, "Shigure Kira",          ),
    (37, "Sirin"                  )
]

PART2_VALKYRIES: list[tuple[int, str] | tuple[int, str, int]] = [
    (2, "Senadina",               ),
    (3, "Coralie 6626 Planck",    ),
    (4, "Erdős Helia",            ),
    (5, "Thelema Nutriscu",       ),
    (6, "«Lantern»",              ),
    (7, "Songque",                ),
    (8, "Vita",                   ),
    (9, "Sparkle"                 )
]

PART_CODE_LENGTH = 1
VALID_SKIN_RARITY_CODES = (2, 3, 4, 5)

PART1 = Part("0", "6", 1)
PART2 = Part(("2", "62"), ("202", "302"), 2)
ALL_PARTS = PART2, PART1 # NOTE: DO NOT CHANGE THE ORDER!

VALKYRIE_DB = ValkyrieDatabase(PART1_VALKYRIES, PART2_VALKYRIES)
