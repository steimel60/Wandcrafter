"""
TiledMap Module

This module defines the `TiledMap` class, which represents a Tiled map loaded from a TMX file.
It provides functionality to render and draw the map on a Pygame surface.
"""
from pprint import pprint
from maps.trees import Tree, MagicTree

import pygame as pg
import pytmx
from config.directories import MAP_DIR
from maps.obstacles import Obstacle, AnimatedObstacle
from maps.animated_tiles import AnimatedTile

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
        self.items = {
            'animated' : list(),
            'tiles' : list()
        }
        self.image = self.make_map()
        self.rect = self.image.get_rect()
        self.obstacles = self.get_obstacles()

    def render(self, surface):
        """Create the image for the map"""
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer): # If a tile layer (not an object layer)
                for x, y, gid in layer:
                    is_animated = False
                    map_x = x * self.tmxdata.tilewidth # x location of tile adjusted to map size
                    map_y = y * self.tmxdata.tileheight # y location of tile adjusted to map size
                    if self.tmxdata.get_tile_properties_by_gid(gid):
                        properties = self.tmxdata.get_tile_properties_by_gid(gid)
                        if "frames" in properties: # Check if tile is animated
                            is_animated = True
                            rect = pg.Rect(
                                map_x,
                                map_y,
                                properties['width'],
                                properties['height']
                            )
                            frames = self.load_animation_frames(properties["frames"])
                            self.items['tiles'].append(AnimatedTile(frames, rect))
                    image = self.tmxdata.get_tile_image_by_gid(gid)
                    if image and not is_animated:
                        surface.blit(image, (map_x, map_y))

    def make_map(self):
        """Creates a PyGame surface that can be Blit to the screen"""
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    def get_obstacles(self):
        """Get a list of static obstacles in the map."""
        obstacles = []
        for tile_object in self.tmxdata.objects:
            if "frames" in tile_object.properties:
                item = self.create_animated_object(tile_object)
            elif tile_object.name == "wall":
                rect = pg.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                item = Obstacle(rect)
            obstacles.append(item)
        return obstacles

    def draw(self, screen, camera):
        """Draw the map's image to the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        # Draw static image
        screen.blit(self.image, camera.apply(self))
        # Draw animated images
        for tile in self.items['tiles']:
            tile.draw(screen, camera)
        for item in self.items['animated']:
            item.draw(screen, camera)
        # Draw debug boxes
        for obstacle in self.obstacles:
            pg.draw.rect(screen, (255,255,255), camera.apply(obstacle), 2)

    def update(self):
        for tile in self.items['tiles']:
            tile.update()
        for item in self.items['animated']:
            item.update()

    def load_animation_frames(self, frames) -> list:
        """Create the pygame surface from the AnimationFrame objects passed in the init function.
        
        Returns: A list of tuples (image: pg.Surface, duration: int)
        """
        loaded_frames = []
        for frame in frames:
            gid = frame.gid
            image = self.tmxdata.get_tile_image_by_gid(gid)
            duration = frame.duration
            loaded_frames.append((image, duration))
        return loaded_frames

    def create_animated_object(self, tile_object) -> AnimatedObstacle:
        """Creates animated objects from the map and stores them in the map data to be updated later."""
        rect = pg.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        if tile_object.name == "MagicTree":
            item = MagicTree(
                    frames = self.load_animation_frames(tile_object.properties['frames']),
                    rect = rect
                )
        else:
            item = AnimatedObstacle(
                frames = self.load_animation_frames(tile_object.properties['frames']),
                rect = rect
            )
        self.items['animated'].append(item)
        return item
