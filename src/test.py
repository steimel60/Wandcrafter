from items.wand import Wand, WandWood, WandCore, WandLength
from items.cloak import Cloak
from entities.inventory import CharacterInventory

wand = Wand(
    wood=WandWood("Larch"),
    core=WandCore("Dragon Heartstring"),
    length=WandLength(13)
)

inventory = CharacterInventory()
inventory.add_item(wand)
inventory.add_item(wand)
inventory.add_item(wand)


print(save := wand.save())

wand2 = Wand.from_json(save) # has from_json method
for key in (d := vars(wand2)):
    print(key, ":", d[key])

print(inventory.bag)
print(inv_save := inventory.save())

inv2 = CharacterInventory.from_json(inv_save)
print("INV 2 BAG: ", inv2.bag)
print("IV 2 SAVE:", inv2.save())

cloak = Cloak.from_json(save) # No from_json method