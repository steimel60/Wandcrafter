"""
Camera Module

This module defines the `Camera` class, which represents a camera used to manage
the view of a game world. The camera is responsible for keeping a specified target
entity (e.g., a player) centered on the screen and allowing for scrolling within the
game world. It can also apply its offset to entities and rectangles, ensuring that
they move with the camera's view and stay within the boundaries of the game world.
"""

import pygame as pg

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
    def __init__(self, width: int = 0, height: int = 0):
        """
        Initialize the Camera object.

        Args:
            width (int): The width of the current map.
            height (int): The height of the current map.
        """
        self.rect = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height
        info = pg.display.Info()
        self.screen_h = info.current_h
        self.screen_w = info.current_w

    def open_map(self, tile_map):
        """Set the camera width and height to match a given map."""
        self.width = tile_map.width
        self.height = tile_map.height
        self.rect = pg.Rect(0,0, self.width, self.height)

    def change_screen_size(self):
        """Get the new width and height of the screen. """
        info = pg.display.Info()
        self.screen_h = info.current_h
        self.screen_w = info.current_w

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
        return entity.rect.move(self.rect.topleft)

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
        return rect.move(self.rect.topleft)

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
        x = -target.rect.x + int(self.screen_w / 2)
        y = -target.rect.y + int(self.screen_h / 2)

        # limit scrolling to map size
        x = min(0,x) # left
        x = max(-(self.width - self.screen_w), x) # right
        y = min(0,y) # top
        y = max(-(self.height - self.screen_h), y) # bottom

        self.rect = pg.Rect(x, y, self.width, self.height)
