from items.wand import Wand, WandWood, WandCore, WandLength
from items.cloak import Cloak

wand = Wand(
    wood=WandWood("Larch"),
    core=WandCore("Dragon Heartstring"),
    length=WandLength(13)
)

print(save := wand.save())

wand2 = Wand.from_json(save) # has from_json method
for key in (d := vars(wand2)):
    print(key, ":", d[key])
cloak = Cloak.from_json(save) # No from_json method