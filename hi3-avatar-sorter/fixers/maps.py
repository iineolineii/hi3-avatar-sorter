from .constants import (
    BRONYA,
    ELYSIA_P1,
    ELYSIA_P2,
    HIMEKO,
    KALLEN,
    KIANA,
    MEI,
    RITA,
    SAKURA,
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
    (1, KIANA, "", 4, 1): (1, KIANA, 1, 4, 1),
    (1, MEI, "", 4, 1): (1, MEI, 1, 4, 1),
    (1, BRONYA, "", 4, 1): (1, BRONYA, 1, 4, 1),
    (1, THERESA, "", 4, 1): (1, THERESA, 1, 4, 1),
    (1, HIMEKO, "", 4, 1): (1, HIMEKO, 1, 4, 1)
}

WRONG_ID_REPLACEMENT_MAP: RawReplacementMap = {
    # 3rd Elysia is not a new character
    (2, ELYSIA_P2, 1): (1, ELYSIA_P1, 3),
    # HoV is 5th Kiana, not 3rd Kallen
    (1, KALLEN, 10 + 3): (1, KIANA, 5),
    # This avatar has wrong battlesuit ID
    (1, RITA, 1, "special"): (1, RITA, 3, "special"),
    # NOTE#1:
    # Because Kallen and Kiana are completely messed up,
    # Kallen's battlesuits were shifted to the 50s range to free room for future
    # Kiana battlesuits.
    #
    # IMPORTANT: For this fix to work, Kiana's max battlesuit ID must also be set
    # to 50 in the Valkyrie map.
    #
    # EDGE CASE: Unrealistically likely to happen, but if a new Kallen battlesuit
    # appears, extend this list accordingly.
    (1, KALLEN, 10 + 1): (1, KALLEN, 50 + 1),
    (1, KALLEN, 10 + 2): (1, KALLEN, 50 + 2),
    (1, KALLEN, 10 + 4): (1, KALLEN, 50 + 3)
}


__all__ = [
    "EMPTY_BATTLESUIT_ID_REPLACEMENT_MAP",
    "TOO_SHORT_BATTLESUIT_ID_REPLACEMENT_MAP",
    "TOO_SHORT_VALKYRIE_ID_REPLACEMENT_MAP",
    "WRONG_ID_REPLACEMENT_MAP",
]
