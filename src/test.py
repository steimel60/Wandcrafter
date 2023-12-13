import json
from pathlib import Path
from config.directories import DATA_DIR, SPRITES_DIR

with open(DATA_DIR / "npc_data.json", encoding="utf-8") as f:
    npc_data = json.load(f)
npc_data = npc_data["npcs"]
for npc in npc_data:
    print(npc)
    print(npc_data[npc]["location"])
