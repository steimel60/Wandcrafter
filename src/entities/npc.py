"""NPC Module.

Contains NPC specific logic.
"""

import json
from entities.characters import Character
from config.directories import DATA_DIR

class NPC(Character):
    """NPC Class.
    
    Entity's that can move around and be interacted with. May
    or may not have dialog or be involved in quests.
    """
    def __init__(self, name, *args, **kwargs) -> None:
        # pylint: disable=useless-super-delegation
        self.data = self.get_npc_data(name)
        super().__init__(self.data, *args, **kwargs)

    def get_npc_data(self, name: str) -> dict:
        """Retrieves specific npc data from json file."""
        with open(DATA_DIR / "npc_data.json", encoding="utf-8") as f:
            npc_data = json.load(f)
        if name not in npc_data["npcs"]:
            raise KeyError(f"No NPC named {name} found in {DATA_DIR / 'npc_data.json'}")
        return npc_data["npcs"][name.lower()]
