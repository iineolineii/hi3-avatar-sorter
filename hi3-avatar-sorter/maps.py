from collections.abc import Iterable

from .enums import PartIDFormat, PartNumber


FORMAT_BY_FOLDER: dict[Iterable[str], PartIDFormat] = {
    (
        "avatarchibiicons",
        "avataritemicon",
        "avataricon",
        "dressicons",
        "avatardressicon",
        "avatariconside",
        "dressfigures"
    ): PartIDFormat.ICON,
    (
        "avatarcardfigures",
        "avatarcardicons"
    ): PartIDFormat.SPLASH,
    (
        "avatarfragmentfigures",
        "avatarfragmenticons"
    ): PartIDFormat.FRAGMENT
}

RAW_PARTS_MAP: dict[str, tuple["PartIDFormat", "PartNumber"]] = {
    "000": (PartIDFormat.ICON,     PartNumber.PART1),
    "002": (PartIDFormat.ICON,     PartNumber.PART2),
    "006": (PartIDFormat.SPLASH,   PartNumber.PART1),
    "302": (PartIDFormat.SPLASH,   PartNumber.PART2),
    "062": (PartIDFormat.SPLASH,   PartNumber.PART2), # Second splash Part 2 ID is for skins found in folders avatarcardfigures and avatarcardicons
    "001": (PartIDFormat.FRAGMENT, PartNumber.PART1),
    "202": (PartIDFormat.FRAGMENT, PartNumber.PART2)
}


RAW_VALKYRIES_MAP: dict[PartNumber, list[tuple[str, str, int] | tuple[str, str]]] = {
    PartNumber.PART1: [
        ("01", "Kiana Kaslana",      50), # Changed from 10 because of NOTE#1
        ("01", "Kallen Kaslana",       ),
        ("02", "Raiden Mei",         10),
        ("02", "Yae Sakura",           ),
        ("03", "Bronya Zaychik",       ),
        ("04", "Murata Himeko",      20),
        ("04", "Liliya Olenyeva",    21),
        ("04", "Rozaliya Olenyeva",    ),
        ("05", "Theresa Apocalypse",   ),
        ("06", "Fu Hua",               ),
        ("07", "Rita Rossweisse",    10),
        ("07", "Seele Vollerei",       ),
        ("08", "Durandal",             ),
        ("09", "Asuka",                ),
        ("20", "Keqing",               ),
        ("21", "Fischl",               ),
        ("22", "Elysia",               ),
        ("23", "Mobius",               ),
        ("24", "Natasha Cioara",       ),
        ("25", "Carole Pepper",        ),
        ("26", "Pardofelis",           ),
        ("27", "Aponia",               ),
        ("28", "Eden",                 ),
        ("29", "Griseo",               ),
        ("30", "Vill-V",               ),
        ("31", "Li Sushang",           ),
        ("32", "Ai Hyperion Λ",        ),
        ("33", "Susannah Manatt",      ),
        ("34", "Misteln Schariac",     ),
        ("35", "PROMETHEUS",           ),
        ("36", "Shigure Kira",         ),
        ("37", "Sirin",                )
    ],
    PartNumber.PART2: [
        ("02", "Senadina",             ),
        ("03", "Coralie 6626 Planck",  ),
        ("04", "Erdős Helia",          ),
        ("05", "Thelema Nutriscu",     ),
        ("06", "«Lantern»",            ),
        ("07", "Songque",              ),
        ("08", "Vita",                 ),
        ("09", "Sparkle",              )
    ]
}
