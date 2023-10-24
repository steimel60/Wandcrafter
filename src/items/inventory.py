from items.item import Item
from items.equippable import Equippable

class CharacterInventory:
    def __init__(self) -> None:
        self.equipped = {
            "cloak" : None
        }
        self.unequipped = list()

    def unequip(self, item_type: str):
        if item_type in self.equipped:
            if self.equipped[item_type]:
                item = self.equipped[item_type]
                self.add_item(item)
                self.equipped[item_type] = None
            else: print(f"No {item_type} equipped")

    def equip(self, item):
        key = None
        # See if item can be equipped
        if isinstance(item, Equippable):
            key = item.equip_key
        else: print(f"{item} not equippable")
        if key:
            if self.equipped[key]:
                self.unequip(key)
            self.equipped[key] = item

    def add_item(self, item):
        if isinstance(item, Item):
            self.unequipped.append(item)
