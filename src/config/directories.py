from pathlib import Path
from .game_settings import GAME_TITLE

# Main Game Folder and Sub-Modules
GAME_DIR = Path(__file__).parents[1]
SOURCE_DIR = GAME_DIR / "src"
ASSET_DIR = GAME_DIR / "assets"
CONFIG_DIR = GAME_DIR / "config"

# ASSET DIRS
IMAGE_DIR = ASSET_DIR / "images"
CLOTHES_DIR = IMAGE_DIR / "clothing"
FONT_DIR = ASSET_DIR / "fonts"
MUSIC_DIR = ASSET_DIR / "music"

# User Directories
USER_HOME_DIR = Path().home() # On windows C:/Users/user
USER_DOCS_DIR = USER_HOME_DIR / "Documents"
USER_GAME_DIR = USER_DOCS_DIR / GAME_TITLE

USER_GAME_DIR.mkdir(parents=True, exist_ok=True)