from .item import Item

class WandWood:
    def __init__(self, name : str) -> None:
        self.name = name

class WandCore:
    def __init__(self, name : str) -> None:
        self.name = name

class WandLength:
    def __init__(self, length : int) -> None:
        self.length = length

class Wand(Item):
    def __init__(
            self,
            wood : WandWood = None,
            core : WandCore = None,
            length : WandLength = None
            ) -> None:
        super().__init__()
        self.wood = wood
        self.core = core
        self.length = length