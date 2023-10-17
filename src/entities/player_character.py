"""
PlayerCharacter Module

This module defines the `PlayerCharacter` class, which represents a player character in the game.
"""

import pygame as pg
from entities.characters import Character
from items.wand import Wand
from config.player_settings import WALK_SPEED

class PlayerCharacter(Character):
    """
    PlayerCharacter Class

    This class represents a player character in the game. It manages the player's 
    attributes, animations, movement, and interactions.

    Attributes:
        name (str): The name of the player character.
        wand (Wand, optional): The wand equipped by the player.
        coord (list): The initial coordinates [x, y] of the player character.

    Methods:
        handle_events(events): Handle player input events.
        update(): Update the player's position and animations.
        draw(screen): Draw the player character on the screen.
        get_save_data(): Retrieve the data necessary to re-initialize the player character.
        initialize_anim_dict(): Initialize animations for the player character.
    """
    def __init__(
            self,
            name : str,
            wand : Wand = None,
            x : int = 0,
            y : int = 0
            ) -> None:
        """
        Initialize a player entity.

        Args:
            name (str): The name of the player.
            wand (Wand, optional): The wand equipped by the player. Defaults to None.
            x (int): The initial x coordinate of the player. Defaults to 0.
            y (int): The initial y coordinate of the player. Defaults to 0.
        """
        super().__init__(name, x, y)
        self.wand = wand

    def handle_events(self, events):
        """
        Handle player input events.

        Args:
            events (list): A list of pygame events to process.
        """
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_UP | pg.K_w:
                        self.set_animation("walk_up")
                        self.y -= WALK_SPEED
                    case pg.K_DOWN | pg.K_s:
                        self.set_animation("walk_down")
                        self.y += WALK_SPEED
                    case pg.K_LEFT | pg.K_a:
                        self.set_animation("walk_left")
                        self.x -= WALK_SPEED
                    case pg.K_RIGHT | pg.K_d:
                        self.set_animation("walk_right")
                        self.x += WALK_SPEED
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

    def get_save_data(self):
        """
        Retrieve the data necessary to re-initialize the player.

        Returns:
            dict: A dictionary containing player data for re-initialization.
        """
        return {
            "name" : self.name,
            "wand" : self.wand,
            "x" : self.x,
            "y" : self.y
        }
