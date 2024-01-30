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
from entities.inventory import CharacterInventory
from maps.portals import Portal, Door

class Character(Entity):
    """Base class for character entities in the game.

    Attributes:
        name (str): The name of the character.
    """
    def __init__(self, data: dict) -> None:
        sprite_sheet = SPRITES_DIR / data["race"] / data["sprite"]
        super().__init__(
            sprite_sheet=sprite_sheet,
            x = data["location"]["position"]["x"],
            y = data["location"]["position"]["y"]
        )
        self.data = data
        self.inventory = CharacterInventory.from_json(data["inventory"])
        self.update_appearance()
        self.speed = WALK_SPEED
        self.destination = self.hitbox.rect.copy()

    def change_destination(self, x, y, obstacles):
        """Change the character's target destination."""
        if self.hitbox.rect == self.destination:
            self.destination.x += x
            self.destination.y += y
        if (idx := self.destination.collidelist(obstacles)) != -1:
            self.destination = self.hitbox.rect.copy()
            return obstacles[idx]
        return None

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
        #if self.has_arrived():
            #self.appearance.set_to_idle()

    def update(self):
        """Update the character's position and appearance."""
        super().update()
        if self.hitbox.rect != self.destination: # If moving
            self.move(self.speed)
        else:
            self.appearance.set_to_idle()

    def update_appearance(self):
        """Update the character's sprite based on their current inventory."""
        base_sprite = SPRITES_DIR / self.data["race"] / self.data["sprite"]
        layers = [base_sprite]
        for _, item in self.inventory.equipped.items():
            if item:
                if item.sprite_sheet is not None:
                    layers.append(item.sprite_sheet)
        layers.insert(0, base_sprite)
        self.appearance.make_new_animation(layers)

    def draw(self, screen, camera):
        super().draw(screen, camera)
        ######### DEBUG RECTS ###########
        # Draw Destination rect
        pg.draw.rect(screen, (255,255,0), camera.apply_rect(self.destination), 2)

    def set_position(self, x, y):
        super().set_position(x, y)
        self.destination.x, self.destination.y = x, y

    def has_arrived(self) -> bool:
        return self.destination == self.hitbox

    def is_idle(self) -> bool:
        return "idle" in self.appearance.current_anim

    def get_save_data(self):
        """
        Retrieve the data necessary to re-initialize the player.

        Returns:
            dict: A dictionary containing player data for re-initialization.
        """
        return {
            "race": self.data["race"],
            "sprite" : self.data["sprite"],
            "location" : {
                "map": "-",
                "position" : {
                    "x" : self.x,
                    "y" : self.y
                }
            },
            "inventory": self.inventory.save()
        }
