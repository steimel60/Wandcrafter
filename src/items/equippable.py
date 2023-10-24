from pathlib import Path
from items.item import Item

class Equippable(Item):
    """Base class for items that can be equipped by characters."""
    def __init__(
            self,
            equip_key: str,
            sprite_sheet: Path = None
            ) -> None:
        super().__init__()
        self.equip_key = equip_key
        self.sprite_sheet = sprite_sheet
