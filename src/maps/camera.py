"""
Camera Module

This module defines the `Camera` class, which represents a camera used to manage
the view of a game world. The camera is responsible for keeping a specified target
entity (e.g., a player) centered on the screen and allowing for scrolling within the
game world. It can also apply its offset to entities and rectangles, ensuring that
they move with the camera's view and stay within the boundaries of the game world.
"""

import pygame as pg
from config.game_settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    """
    Camera Class

    This class represents a camera used to manage the view of a game world,
    keeping a specified target entity (e.g., a player) centered on the screen
    and allowing for scrolling within the game world.

    The camera can apply its offset to entities and rectangles, moving them with
    the camera's view. It also ensures that the camera doesn't move beyond the
    boundaries of the game world.
    """
    def __init__(self, width, height):
        """
        Initialize the Camera object.

        Args:
            width (int): The width of the camera.
            height (int): The height of the camera.
        """
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """
        Moves things with the camera.

        This method applies the camera's offset to an entity, effectively moving
        the entity along with the camera. It can be used, for example, to keep a
        mini-map in the top right corner of the screen.

        Args:
            entity: The entity to be moved with the camera.

        Returns:
            Rect: A new rectangle representing the entity's position adjusted
            for the camera's position.
        """
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """
        Move rectangles with the camera.

        This method applies the camera's offset to a rectangle, effectively moving
        the rectangle along with the camera.

        Args:
            rect (Rect): The rectangle to be moved with the camera.

        Returns:
            Rect: A new rectangle representing the original rectangle's position
            adjusted for the camera's position.
        """
        return rect.move(self.camera.topleft)

    def update(self, target):
        """
        Move the camera to keep the player centered on the screen.

        This method adjusts the camera's position based on the target's position
        to ensure that the target (e.g., a player character) remains centered on
        the screen. It also limits the scrolling to the size of the map to prevent
        the camera from moving beyond the map boundaries.

        Args:
            target: The target entity (e.g., the player character) to keep centered
            on the screen.
        """
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0,x) # left
        x = max(-(self.width - SCREEN_WIDTH), x) # right
        y = min(0,y) # top
        y = max(-(self.height - SCREEN_HEIGHT), y) # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)
