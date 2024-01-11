import items
from items.item import Item
from items.equippable import Equippable

class CharacterInventory:
    def __init__(self) -> None:
        self.equipped = {}
        self.bag = list()

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
            key = item.__class__.__name__
        else: print(f"{item} not equippable") # Turn into message box later
        if key:
            if key in self.equipped:
                self.unequip(key)
            self.equipped[key] = item

    def add_item(self, item):
        if isinstance(item, Item):
            self.bag.append(item)

    def save(self):
        equipped = {}
        for key, item in self.equipped.items():
            equipped[key] = item.save()
        return {
            "equipped" : equipped,
            "bag" : [item.save() for item in self.bag]
        }

    @classmethod
    def from_json(cls, data):
        instance = cls()
        for key in data["equipped"]:
            load_data = data["equipped"][key]
            item = instance.get_item_from_json(load_data)
            instance.equip(item)
        for load_data in data["bag"]:
            instance.add_item(
                instance.get_item_from_json(load_data)
            )
        return instance

    def get_item_from_json(self, data):
        match data:
            case {"type" : "Wand"}:
                return items.wand.Wand.from_json(data)
            case {"type" : "Cloak"}:
                return items.cloak.Cloak.from_json(data)
            case _:
                # raise ValueError(f'Tried to load unknown item: {data["type"]}') # UNCOMMENT EVENUALLY
                print(f'Tried to load unknown item: {data["type"]}')
