from .constants import (
    BRONYA,
    ELYSIA_P1,
    ELYSIA_P2,
    HIMEKO,
    KALLEN,
    KIANA,
    LANTERN,
    MEI,
    RITA,
    SAKURA,
    THELEMA,
    THERESA,
    RawReplacementMap
)


# These avatars' battlesuit IDs are 1 character long instead of 2
TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP: RawReplacementMap = {
    (1, SAKURA, "1", 4, 1): (1, SAKURA, 10 + 1, 4, 1)
}

# These avatars' Valkyrie IDs are 1 character long instead of 2
TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP: RawReplacementMap = {
    (1, str(KIANA), 15, 4, 1): (1, KIANA, 15, 4, 1)
}

# These avatars do not have their battlesuit IDs
EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP: RawReplacementMap = {
    (1, KIANA,   "", 4, 1): (1, KIANA,   1, 4, 1),
    (1, MEI,     "", 4, 1): (1, MEI,     1, 4, 1),
    (1, BRONYA,  "", 4, 1): (1, BRONYA,  1, 4, 1),
    (1, HIMEKO,  "", 4, 1): (1, HIMEKO,  1, 4, 1),
    (1, THERESA, "", 4, 1): (1, THERESA, 1, 4, 1)
}

# These avatars battlesuit IDs are mixed up
WRONG_BATTLESUIT_ID_REPLACEMENT_MAP: RawReplacementMap = {
    # 3rd Rita's special avatar is not her 1st battlesuit
    (1, RITA, 1, "special"): (1, RITA, 3, "special"),

    # 3rd Elysia is not a new character
    (2, ELYSIA_P2, 1): (1, ELYSIA_P1, 3),

    # HoV is 5th Kiana, not 3rd Kallen
    (1, KALLEN, 10+3): (1, KIANA, 5),

    # Skip duplicates by letting them overwrite originals
    (1, 10+MEI,    3 ): (1, MEI,    3 ),
    (1, 10+BRONYA, 3 ): (1, BRONYA, 3 ),
    (1, 10+HIMEKO, 11): (1, HIMEKO, 11),

    # NOTE#1:
    # Because Kallen and Kiana are completely messed up,
    # Kallen's battlesuits were shifted to the 50s range to free room for future
    # Kiana battlesuits.
    #
    # IMPORTANT: For this fix to work, Kiana's max battlesuit ID must also be set
    # to 50 in the Valkyrie map.
    #
    # EDGE CASE: Unrealistically likely to happen, but if a new Kallen battlesuit
    # appears, this list must be extended accordingly.
    (1, KALLEN, 10+1): (1, KALLEN, 50+1),
    (1, KALLEN, 10+2): (1, KALLEN, 50+2),
    (1, KALLEN, 10+4): (1, KALLEN, 50+3)
}

# These avatars' notes are misspelled
WRONG_NOTE_REPLACEMENT_MAP: RawReplacementMap = {
    (1, ELYSIA_P1, 2, 4, 1, "ShadownIcon"): (1, ELYSIA_P1, 2, 4, 1, "ShadowIcon"),

    # These avatars do not have an underscore before the note
    (2, THELEMA, 1, 4, "02ShadowIcon"): (2, THELEMA, 1, 4, 2, "ShadowIcon"),
    (2, LANTERN, 1, 4, "01ShadowIcon"): (2, LANTERN, 1, 4, 1, "ShadowIcon")
}


__all__ = [
    "EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP",
    "TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP",
    "TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP",
    "WRONG_BATTLESUIT_ID_REPLACEMENT_MAP",
    "WRONG_NOTE_REPLACEMENT_MAP"
]
