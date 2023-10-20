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
from utils.asset_management import get_anims_in_sprite_sheet, get_hit_box_for_sprite
from entities.animation import Animation
from config.player_settings import WALK_SPEED

class Character(pg.sprite.Sprite):
    """Base class for character entities in the game.

    Attributes:
        name (str): The name of the character.
        x (int): The x-coordinate of the character's position.
        y (int): The y-coordinate of the character's position.
        rect (pygame.Rect): The hit box (rectangle) that defines the character's position and size.
        appearance (Appearance): The appearance of the character.
    """
    def __init__(self,
                 name,
                 x = 0,
                 y = 0,
                 body = "base_body"
                 ) -> None:
        super().__init__()
        self.name = name
        self.x = x
        self.y = y
        self.speed = WALK_SPEED
        self.appearance = CharacterAppearance(body=body)
        self.destination = self.rect.copy()

    @property
    def rect(self):
        """Character's hitbox."""
        w, h = get_hit_box_for_sprite(self.appearance.body_sprite_sheet)
        anim = self.appearance.get_current_anim()
        frame_w = anim.anim_data["frame_w"]
        frame_h = anim.anim_data["frame_h"]
        w_diff = frame_w - w
        h_diff = frame_h - h
        return pg.Rect(self.x + w_diff, self.y + h_diff, w, h)

    @rect.setter
    def rect(self, x, y):
        self.rect.x, self.rect.y = x + self.hit_box_offset[0], y + self.hit_box_offset[1]

    @property
    def hit_box_offset(self):
        """Difference between a characters sprite size and hitbox."""
        w, h = get_hit_box_for_sprite(self.appearance.body_sprite_sheet)
        anim = self.appearance.get_current_anim()
        frame_w = anim.anim_data["frame_w"]
        frame_h = anim.anim_data["frame_h"]
        w_diff = frame_w - w
        h_diff = frame_h - h
        return w_diff, h_diff

    def change_destination(self, x, y):
        """Change the character's target destination."""
        if self.rect == self.destination:
            self.destination.x += x
            self.destination.y += y

    def move(self, speed):
        """Move towards the character's target destination."""
        if self.rect.y > self.destination.y:
            self.y -= speed
        if self.rect.y < self.destination.y:
            self.y += speed
        if self.rect.x > self.destination.x:
            self.x -= speed
        if self.rect.x < self.destination.x:
            self.x += speed

    def update(self):
        """Update the character's position and appearance."""
        if self.rect != self.destination:
            self.move(self.speed)
        self.rect.x, self.rect.y = self.x, self.y
        self.appearance.update()

    def set_animation(self, anim):
        """Set the current animation for the character.

        Args:
            anim (str): The name of the animation to set.
        """
        self.appearance.set_animation(anim)

    def draw(self, screen):
        """
        Draw the player character on the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        self.appearance.draw(screen, self.x, self.y)
        outline_color = (255,0,0)
        outline_width = 2
        pg.draw.rect(screen, outline_color, self.rect, outline_width)
        pg.draw.rect(screen, (255,255,0), self.destination, outline_width)

class CharacterAppearance:
    """Handles the appearance and animations of a character entity.

    This class manages the appearance and animations for a character in the game.

    Attributes:
        body_sprite_sheet (str): The name of the sprite sheet for the character's body.
        anim_dict (dict): A dictionary containing animations for the character.
        current_anim (str): The name of the current animation to display.

    Methods:
        initialize_anim_dict(): Init the character's animations based on the provided sprite sheet.
        get_image(): Get the current image of the character.
        update(): Update the character's animation.
        set_animation(anim: str): Set the current animation for the character.
        draw(screen, x, y): Draw the character on the screen.

    Args:
        body (str): The name of the sprite sheet for the character's body.
    """
    def __init__(
            self,
            body = "base_body",
    ) -> None:
        self.body_sprite_sheet = body
        self.anim_dict = self.initialize_anim_dict()
        self.current_anim = "idle_down"

    def initialize_anim_dict(self):
        """
        Initialize animations for the player character.

        Load necessary animations, images, and character customization options for the player.

        Returns:
            dict: A dictionary where keys are animation names and values are Animation objects.
        """
        # Load in body images
        anim_dict = {}
        anims = get_anims_in_sprite_sheet(self.body_sprite_sheet)
        for anim in anims:
            anim_dict[anim] = Animation(
                sprite_sheet=self.body_sprite_sheet,
                animation=anim
            )
        return anim_dict

    def get_image(self):
        """Get the current image of the character.

        Returns:
            pygame.Surface: The current image of the character.
        """
        return self.anim_dict[self.current_anim]

    def update(self):
        """Update the character's animation."""
        self.anim_dict[self.current_anim].update()

    def set_animation(self, anim):
        """Set the current animation for the character.

        Args:
            anim (str): The name of the animation to set.
        """
        if anim in self.anim_dict:
            self.current_anim = anim

    def get_current_anim(self) -> Animation:
        """Returns the current animation object."""
        return self.anim_dict[self.current_anim]

    def draw(self, screen, x, y):
        """
        Draw the character on the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
            x (int): The x-coordinate where the character should be drawn.
            y (int): The y-coordinate where the character should be drawn.
        """
        screen.blit(
            self.anim_dict[self.current_anim].get_current_frame(),
            (x, y)
        )
