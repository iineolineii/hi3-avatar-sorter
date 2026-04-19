from collections.abc import Iterable

from .enums import PartIDFormats, PartNumbers


FORMAT_BY_FOLDER: dict[Iterable[str], PartIDFormats] = {
    (
        "avatarchibiicons",
        "avataritemicon",
        "avataricon",
        "dressicons",
        "avatardressicon",
        "avatariconside",
        "dressfigures"
    ): PartIDFormats.SHORT,
    (
        "avatarcardfigures",
        "avatarcardicons"
    ): PartIDFormats.LONG,
    (
        "avatarfragmentfigures",
        "avatarfragmenticons"
    ): PartIDFormats.FRAGMENT
}

RAW_PARTS: dict[str, tuple["PartIDFormats", "PartNumbers"]] = {
    "000": (PartIDFormats.SHORT,    PartNumbers.PART1),
    "002": (PartIDFormats.SHORT,    PartNumbers.PART2),
    "006": (PartIDFormats.LONG,     PartNumbers.PART1),
    "302": (PartIDFormats.LONG,     PartNumbers.PART2),
    "062": (PartIDFormats.LONG,     PartNumbers.PART2), # Second long Part 2 ID is for skins found in folders avatarcardfigures and avatarcardicons
    "001": (PartIDFormats.FRAGMENT, PartNumbers.PART1),
    "202": (PartIDFormats.FRAGMENT, PartNumbers.PART2),
}


RAW_PART1_VALKYRIES: list[tuple[str, str, int] | tuple[str, str]] = [
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
]

RAW_PART2_VALKYRIES: list[tuple[str, str, int] | tuple[str, str]] = [
    ("02", "Senadina",             ),
    ("03", "Coralie 6626 Planck",  ),
    ("04", "Erdős Helia",          ),
    ("05", "Thelema Nutriscu",     ),
    ("06", "«Lantern»",            ),
    ("07", "Songque",              ),
    ("08", "Vita",                 ),
    ("09", "Sparkle",              )
]


__vesrion__ = (0, 0, 1)

__all__ = [
    "FORMAT_BY_FOLDER",
    "RAW_PARTS",
    "RAW_PART1_VALKYRIES",
    "RAW_PART2_VALKYRIES",
    "__vesrion__",
]
