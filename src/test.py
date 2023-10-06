from config.directories import ANIM_DIR

path = ANIM_DIR / "walk_forward"

print([f for f in path.iterdir()])