"""
Character Module

This module contains the base classes for character entities in the game. 
It provides a `Character` class that represents a character entity with a name,
position, hitbox, and appearance. Additionally, it defines the `CharacterAppearance`
class for handling character appearances and animations.

Classes:
    - Character: Base class for character entities.
    - CharacterAppearance: Manages appearance and animations of a character entity.
"""

import pygame as pg
from entities.entity import Entity
from config.player_settings import WALK_SPEED
from config.directories import SPRITES_DIR
from items.inventory import CharacterInventory

class Character(Entity):
    """Base class for character entities in the game.

    Attributes:
        name (str): The name of the character.
    """
    def __init__(self, data: dict, *args, **kwargs) -> None:
        sprite_sheet = SPRITES_DIR / data["race"] / data["sprite"]
        super().__init__(sprite_sheet=sprite_sheet, *args, **kwargs)
        self.data = data
        self.inventory = data["inventory"]
        self.speed = WALK_SPEED
        self.destination = self.hitbox.rect.copy()

    def change_destination(self, x, y):
        """Change the character's target destination."""
        if self.hitbox.rect == self.destination:
            self.destination.x += x
            self.destination.y += y

    def move(self, speed):
        """Move towards the character's target destination.
        
        Used to make characer slide across the screen as opposed to snap
        from position to position.
        """
        if self.hitbox.rect.y > self.destination.y:
            self.change_position(0, -speed)
        if self.hitbox.rect.y < self.destination.y:
            self.change_position(0, speed)
        if self.hitbox.rect.x > self.destination.x:
            self.change_position(-speed, 0)
        if self.hitbox.rect.x < self.destination.x:
            self.change_position(speed, 0)
        self.hitbox.move(self.x, self.y)

    def update(self, **kwargs):
        """Update the character's position and appearance."""
        super().update()
        if self.hitbox.rect != self.destination: # If attempting to move
            tile_map = kwargs.get("tile_map") # Get static objects
            sprite_group = kwargs.get("sprite_group") # Get dynamic objects
            other_sprites = [sprite.hitbox for sprite in sprite_group if sprite != self]
            # Check for collision with static objects
            if self.destination.collidelist(tile_map.obstacles) != -1:
                self.destination = self.hitbox.rect.copy()
            # Check for collision with dynamic objects
            elif self.destination.collidelist(other_sprites) != -1:
                self.destination = self.hitbox.rect.copy()
            else: self.move(self.speed)

    def update_appearance(self):
        """Update the character's sprite based on their current inventory."""
        #base_sprite = SPRITES_DIR / self.species / "base_body.png"
        layers = [self.base_sprite]
        for _, item in self.inventory.equipped.items():
            if item is not None:
                layers.append(item)
        layers.insert(0, self.base_sprite)
        self.appearance.make_new_animation(layers)

    def draw(self, screen, camera):
        super().draw(screen, camera)
        ######### DEBUG RECTS ###########
        # Draw Destination rect
        pg.draw.rect(screen, (255,255,0), camera.apply_rect(self.destination), 2)
