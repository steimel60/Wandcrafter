from config.directories import SPRITES_DIR
from items.equippable import Equippable

class Cloak(Equippable):
    def __init__(self, species: str, style: str, color = None) -> None:
        sprite_sheet = SPRITES_DIR / species / "cloak" / style
        super().__init__(sprite_sheet=sprite_sheet)
        self.style = style
        self.species = species
        self.color = color

    @classmethod
    def from_json(cls, data):
        instance = cls(
            style = data["style"],
            species = data["species"],
            color = data["color"]
        )
        return instance