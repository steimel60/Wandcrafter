"""
PlayerCharacter Module

This module defines the `PlayerCharacter` class, which represents a player character in the game.
"""

import pygame as pg
from entities.characters import Character
from config.game_settings import TILESIZE

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
            *args,
            **kwargs
            ) -> None:
        """
        Initialize a player entity.

        Args:
            name (str): The name of the player.
            wand (Wand, optional): The wand equipped by the player. Defaults to None.
            x (int): The initial x coordinate of the player. Defaults to 0.
            y (int): The initial y coordinate of the player. Defaults to 0.
        """
        super().__init__(*args, **kwargs)
        self.interact_tile = self.destination.copy()

    def handle_events(self, events):
        """
        Handle player input events.

        Args:
            events (list): A list of pygame events to process.
        """
        # Triggered Events
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        if "idle" in self.appearance.current_anim:
                            print("INTERACT EVENT")
                    ########## TEST EVENTS #############
                    case pg.K_u:
                        if "idle" in self.appearance.current_anim:
                            print("EQUIP EVENT")
                            self.inventory.equip(
                            Cloak(
                                sprite_sheet=SPRITES_DIR / self.species / "cloak" / "school_cloak"
                                )
                            )
                            self.update_appearance()
                    case pg.K_i:
                        if "idle" in self.appearance.current_anim:
                            print("UNEQUIP EVENT")
                            self.inventory.unequip("cloak")
                            self.update_appearance()
                    ################# END TEST ############
            if event.type == pg.KEYUP:
                match event.key:
                    case pg.K_UP | pg.K_w:
                        self.set_animation("idle_up")
                    case pg.K_DOWN | pg.K_s:
                        self.set_animation("idle_down")
                    case pg.K_LEFT | pg.K_a:
                        self.set_animation("idle_left")
                    case pg.K_RIGHT | pg.K_d:
                        self.set_animation("idle_right")
        # Continuous Events
        keys = pg.key.get_pressed()
        if (keys[pg.K_UP] or keys[pg.K_w]):
            self.set_animation("walk_up")
            self.change_destination(0, -TILESIZE)
        elif (keys[pg.K_DOWN] or keys[pg.K_s]):
            self.set_animation("walk_down")
            self.change_destination(0, TILESIZE)
        elif (keys[pg.K_LEFT] or keys[pg.K_a]):
            self.set_animation("walk_left")
            self.change_destination(-TILESIZE, 0)
        elif (keys[pg.K_RIGHT] or keys[pg.K_d]):
            self.set_animation("walk_right")
            self.change_destination(TILESIZE, 0)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
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
