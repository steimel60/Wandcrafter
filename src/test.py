from items.wand import Wand, WandWood, WandCore, WandLength

wand = Wand(
    wood=WandWood("Larch"),
    core=WandCore("Dragon Heartstring"),
    length=WandLength(13)
)

print(save := wand.save())

#print(vars("test")) # Err, must have __dict__