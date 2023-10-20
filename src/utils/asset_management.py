"""
Asset Management module.

This module contains functions related to asset management.
For example loading the information for an animation from a sprite sheet.
"""

import toml
from config.directories import ANIM_DIR


def get_anims_in_sprite_sheet(sprite_sheet_name: str) -> list[str]:
    """Retrieve names of animations in a sprite sheet."""
    path = ANIM_DIR / f"{sprite_sheet_name}.toml"
    with open(path, 'r', encoding="utf-8") as file:
        data = toml.load(file)
    return [key for key in data if key != "sheet_data"]

def get_hit_box_for_sprite(sprite_sheet_name: str):
    """Retrieve hitbox size in a give sprite sheet."""
    path = ANIM_DIR / f"{sprite_sheet_name}.toml"
    with open(path, 'r', encoding="utf-8") as file:
        data = toml.load(file)
    return (data["sheet_data"]["hit_box_w"],data["sheet_data"]["hit_box_h"])

def get_anim_data(sprite_sheet_name, anim_name):
    """Retrieve data for a specific animation within a sprite sheet.
    
    Args:
        sprite_sheet_name (str): Name of the sprite sheet containing the animation.
        anim_name (str): Name of the animation in the related toml file.

    Returns:
        dict with the following keys
        - "frame_w": width of the images in the sheet.
        - "frame_h": height of the images in the sheet.
        - "duration": how many ticks each frame is drawn.
        - "row" : which row of the sprite sheet the animation is on.
        - "seq" : sequence of columns that create the animation.
    """
    path = ANIM_DIR / f"{sprite_sheet_name}.toml"
    with open(path, 'r', encoding="utf-8") as file:
        data = toml.load(file)
    return {
        "frame_w" : data["sheet_data"]["tile_w"],
        "frame_h" : data["sheet_data"]["tile_h"],
        "duration": data[anim_name]["frame_duration"],
        "row" : data[anim_name]["row"],
        "seq" : data[anim_name]["seq"]
    }

def get_sprite_data(sprite_sheet_name):
    """Retrieve data from a .toml file for a given sprite sheet.
    
    Args:
        sprite_sheet_name (str): Name of the sprite sheet.

    Returns:
        dict containing the data in the .toml file.
    """
    path = ANIM_DIR / f"{sprite_sheet_name}.toml"
    with open(path, 'r', encoding="utf-8") as file:
        data = toml.load(file)
    return data
