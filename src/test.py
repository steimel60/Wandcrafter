import json
from pathlib import Path
from config.directories import DATA_DIR, SPRITES_DIR

with open(DATA_DIR / "npc_data.json", encoding="utf-8") as f:
    npc_data = json.load(f)
print(type(npc_data))
print(npc_data["npcs"]["dylan"]["inventory"]["equipped"])
sprite = npc_data["npcs"]["dylan"]["sprite"]
race = npc_data["npcs"]["dylan"]["race"]
print(SPRITES_DIR / race / sprite)
