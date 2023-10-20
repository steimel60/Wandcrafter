"""NPC Module.

Contains NPC specific logic.
"""
from entities.characters import Character

class NPC(Character):
    """NPC Class.
    
    Entity's that can move around and be interacted with. May
    or may not have dialog or be involved in quests.
    """
    def __init__(self, *args, **kwargs) -> None: 
        # pylint: disable=useless-super-delegation
        super().__init__(*args, **kwargs)
