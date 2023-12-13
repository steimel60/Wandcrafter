"""
PlayerCharacter Module

This module defines the `PlayerCharacter` class, which represents a player character in the game.
"""

import pygame as pg
from entities.characters import Character
from config.game_settings import TILESIZE
from gui.message_box import MessageBox

##### FOR TESTS
from items.cloak import Cloak
from config.directories import SPRITES_DIR

class PlayerCharacter(Character):
    """
    PlayerCharacter Class

    This class represents a player character in the game. It manages the player's 
    attributes, animations, movement, and interactions.

    Attributes:
        name (str): The name of the player character.
        wand (Wand, optional): The wand equipped by the player.
        interact_tile (pg.Rect): The rect used to see what objects the player is interacting with.

    Methods:
        handle_events(events): Handle player input events.
        update(): Update the player's position and animations.
        draw(screen): Draw the player character on the screen.
        get_save_data(): Retrieve the data necessary to re-initialize the player character.
        initialize_anim_dict(): Initialize animations for the player character.
    """
    def __init__(
            self,
            data
            ) -> None:
        """
        Initialize a player entity.

        Args:
            name (str): The name of the player.
            wand (Wand, optional): The wand equipped by the player. Defaults to None.
            x (int): The initial x coordinate of the player. Defaults to 0.
            y (int): The initial y coordinate of the player. Defaults to 0.
        """
        super().__init__(data)
        self.interact_tile = self.destination.copy()

    def update(self):
        super().update()
        if "idle" in self.appearance.current_anim:
            self.update_interaction_rect()

    def update_interaction_rect(self):
        """Figure out which tile interactions should be called from."""
        anim_name = self.appearance.current_anim
        if "up" in anim_name:
            self.interact_tile.x = self.destination.x
            self.interact_tile.y = self.destination.y - TILESIZE
        elif "down" in anim_name:
            self.interact_tile.x = self.destination.x
            self.interact_tile.y = self.destination.y + TILESIZE
        elif "left" in anim_name:
            self.interact_tile.x = self.destination.x - TILESIZE
            self.interact_tile.y = self.destination.y
        elif "right" in anim_name:
            self.interact_tile.x = self.destination.x + TILESIZE
            self.interact_tile.y = self.destination.y

    def interact(self, map_objects):
        """Interact with map obstacles or other sprites."""
        idx = self.interact_tile.collidelist(map_objects)
        if idx != -1:
            if hasattr(map_objects[idx], "interact"):
                return map_objects[idx].interact()
            return ["CHANGE_STATE", "message_box", MessageBox("You can't interact with that...")]
        return ["CHANGE_STATE", "message_box", MessageBox("There's nothing there...")]

    def draw(self, screen: pg.Surface, camera):
        super().draw(screen, camera)
        # Draw the tile that a player would interact with if called
        if "idle" in self.appearance.current_anim:
            pg.draw.rect(screen, (0,255,0), camera.apply_rect(self.interact_tile), 2)

    def get_save_data(self):
        """
        Retrieve the data necessary to re-initialize the player.

        Returns:
            dict: A dictionary containing player data for re-initialization.
        """
        return super().get_save_data()
