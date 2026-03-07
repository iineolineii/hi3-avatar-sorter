from .registry import ValkyrieRegistry


DATA_PART1 = [
    ( 1, "Kiana Kaslana",        50 ),
    ( 1, "Kallen Kaslana",          ),
    ( 2, "Raiden Mei",           10 ),
    ( 2, "Yae Sakura",              ),
    ( 3, "Bronya Zaychik",          ),
    ( 4, "Murata Himeko",        20 ),
    ( 4, "Liliya Olenyeva",      21 ),
    ( 4, "Rozaliya Olenyeva",       ),
    ( 5, "Theresa Apocalypse",      ),
    ( 6, "Fu Hua",                  ),
    ( 7, "Rita Rossweisse",      10 ),
    ( 7, "Seele Vollerei",          ),
    ( 8, "Durandal",                ),
    ( 9, "Asuka",                   ),
    (20, "Keqing",                  ),
    (21, "Fischl",                  ),
    (22, "Elysia",                  ),
    (23, "Mobius",                  ),
    (24, "Natasha Cioara",          ),
    (25, "Carole Pepper",           ),
    (26, "Pardofelis",              ),
    (27, "Aponia",                  ),
    (28, "Eden",                    ),
    (29, "Griseo",                  ),
    (30, "Vill-V",                  ),
    (31, "Li Sushang",              ),
    (32, "Ai Hyperion Λ",           ),
    (33, "Susannah Manatt",         ),
    (34, "Misteln Schariac",        ),
    (35, "PROMETHEUS",              ),
    (36, "Shigure Kira",            ),
    (37, "Sirin"                    )
]

DATA_PART2 = [
    (202, "Senadina",               ),
    (203, "Coralie 6626 Planck",    ),
    (204, "Erdős Helia",            ),
    (205, "Thelema Nutriscu",       ),
    (206, "«Lantern»",              ),
    (207, "Songque",                ),
    (208, "Vita",                   ),
    (209, "Sparkle"                 )
]

PART_CODE_LENGTH = 1
VALID_SKIN_RARITY_CODES = (2, 3, 4, 5)

valkyrie_db = ValkyrieRegistry(DATA_PART1, DATA_PART2)
