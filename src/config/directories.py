"""
Configuration file for game directories.

This file defines various directories and paths used by your game. These directories
are organized to store assets, such as images, animations, maps, fonts, and music, and
also to manage user-specific directories.
"""

from pathlib import Path
from config.game_settings import GAME_TITLE

# Main Game Folder and Sub-Modules
GAME_DIR = Path(__file__).parents[2]
SOURCE_DIR = GAME_DIR / "src"
ASSET_DIR = GAME_DIR / "assets"
DATA_DIR = GAME_DIR / "data"
CONFIG_DIR = SOURCE_DIR / "config"

# ASSET DIRS
SPRITES_DIR = ASSET_DIR / "sprites"
MAP_DIR = ASSET_DIR / "maps"
FONT_DIR = ASSET_DIR / "fonts"
MUSIC_DIR = ASSET_DIR / "music"
GUI_DIR = ASSET_DIR / "gui"

# User Directories
USER_HOME_DIR = Path().home() # On windows C:/Users/user
USER_DOCS_DIR = USER_HOME_DIR / "Documents"
USER_GAME_DIR = USER_DOCS_DIR / GAME_TITLE

USER_GAME_DIR.mkdir(parents=True, exist_ok=True)
