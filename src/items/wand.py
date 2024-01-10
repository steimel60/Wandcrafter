"""
Wand Module

This module defines the classes related to wand components, including WandWood, 
WandCore, WandLength, and Wand, which represents a wizard's wand and its attributes.

Wand components such as wood, core, and length can be customized to create unique wands.
"""

from items.item import Item

# pylint: disable=R0903
# disables "too few public methods" warning
class WandWood:
    """Wood component of a wand."""
    def __init__(self, name : str) -> None:
        self.name = name

class WandCore:
    """Core component of a wand"""
    def __init__(self, name : str) -> None:
        self.name = name

class WandLength:
    """Length component of a wand."""
    def __init__(self, length : int) -> None:
        self.length = length

class Wand(Item):
    """
    Represents a magical wand, a type of item that can be used within the game world.

    This class extends the Item class and adds attributes specific to wands, such as
    the type of wood, the magical core, and the length of the wand.

    Attributes:
        wood (WandWood): The type of wood used in the wand.
        core (WandCore): The magical core of the wand.
        length (WandLength): The length of the wand in inches.
    """
    def __init__(
            self,
            wood : WandWood,
            core : WandCore,
            length : WandLength
            ) -> None:
        """
        Initialize a Wand instance.

        Args:
            wood (WandWood): The wand's wood type.
            core (WandCore): The wand's core type.
            length (WandLength): The length of the wand.
        """
        super().__init__()
        self.wood = wood
        self.core = core
        self.length = length

    @classmethod
    def from_json(cls, data):
        wood = WandWood(**data["wood"])
        core = WandCore(**data["core"])
        length = WandLength(**data["length"])
        instance = cls(
            wood = wood,
            core = core,
            length = length
        )
        return instance
