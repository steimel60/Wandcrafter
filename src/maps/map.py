"""
TiledMap Module

This module defines the `TiledMap` class, which represents a Tiled map loaded from a TMX file.
It provides functionality to render and draw the map on a Pygame surface.
"""

import pygame as pg
import pytmx
from config.directories import MAP_DIR
from entities.obstacles import Obstacle

class TiledMap:
    """
    TiledMap Class

    This class represents a Tiled map loaded from a TMX file.
    It provides methods to render and draw the map on a Pygame surface.

    Args:
        map_name (str): The name of the Tiled map.

    Attributes:
        name (str): The name of the Tiled map.
        width (int): The width of the map in pixels.
        height (int): The height of the map in pixels.
        tmxdata (pytmx.TiledMapData): The loaded Tiled map data.
        image (pygame.Surface): The Pygame surface representing the map's image.

    Methods:
        render(surface): Create the image for the map.
        make_map(): Create a Pygame surface that can be Blit to the screen.
        draw(screen): Draw the map's image to the screen.

    """
    def __init__(self, map_name):
        """
        Initialize a TiledMap object.

        Args:
            map_name (str): The name of the Tiled map.
        """
        self.name = map_name
        tm = pytmx.load_pygame(MAP_DIR / f"{map_name}.tmx", pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height =tm.height * tm.tileheight
        self.tmxdata = tm
        self.image = self.make_map()
        self.rect = self.image.get_rect()
        self.obstacles = self.get_obstacles()

    def render(self, surface):
        """Create the image for the map"""
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(
                            tile,
                            (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight)
                            )

    def make_map(self):
        """Creates a PyGame surface that can be Blit to the screen"""
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    def get_obstacles(self):
        """Get a list of static obstacles in the map."""
        obstacles = []
        for tile_object in self.tmxdata.objects:
            if tile_object.name == "wall":
                obstacles.append(
                    Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                )
        return obstacles

    def draw(self, screen, camera):
        """Draw the map's image to the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        screen.blit(self.image, camera.apply(self))
        for obstacle in self.obstacles:
            pg.draw.rect(screen, (255,255,255), camera.apply(obstacle), 2)
