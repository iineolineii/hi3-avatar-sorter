from ..relationships import ManyToOne
from .skin_rarity import SkinRarity


from dataclasses import dataclass, field


@dataclass
class Skin(ManyToOne["SkinRarity"]):
    code: int

    no: int = field(init=False)

    @classmethod
    def by_code(
        cls,
        code: int,
        skin_rarity: SkinRarity
    ):
        if code in skin_rarity.skins:
            return skin_rarity.skins[code]

        return cls(code)
