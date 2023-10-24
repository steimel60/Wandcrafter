"""Entity Module.

This module is for anything drawn in the game.
"""
from pathlib import Path
import pygame as pg
from utils.asset_management import get_anims_in_sprite_sheet, get_sprite_data

from entities.animation import Animation

class Entity(pg.sprite.Sprite):
    """Entity class.
    
    This class represents anything that is drawn in game.
    """
    def __init__(
            self,
            groups: list[pg.sprite.Group],
            x: int,
            y: int,
            sprite_sheet: list[Path]
            ) -> None:
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.appearance = EntityAppearance(sprite_sheet=sprite_sheet)
        self.hitbox = HitBox(x, y, self.appearance)

    @property
    def rect(self):
        """An entity's rect is just the hitbox rect."""
        return self.hitbox.rect

    def draw(self, screen, camera):
        """
        Draw the player character on the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        self.appearance.draw(screen, self.x + camera.rect.x, self.y + camera.rect.y)
        self.hitbox.draw(screen, camera)

    def update(self, **_kwargs) -> None:
        """Update the entity's animation."""
        self.appearance.update()

    def change_position(self, dx, dy):
        """Change position by a given amount."""
        self.x += dx
        self.y += dy

    def set_animation(self, anim):
        """Set the current animation for the character.

        Args:
            anim (str): The name of the animation to set.
        """
        self.appearance.set_animation(anim)

class EntityAppearance:
    """Handles the appearance and animations of an entity.

    This class manages the appearance and animations for any entity in the game.

    Attributes:
        sprite_sheet (str): The name of the sprite sheet for the entity.
        anim_dict (dict): A dictionary containing animations for the entity.
        current_anim (str): The name of the current animation to display. Used as a key
            for self.anim_dict

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
            sprite_sheet : list[Path],
            anim: str = None
    ) -> None:
        if isinstance(sprite_sheet, Path):
            sprite_sheet = [sprite_sheet]  # Convert a single string to a list of one string
        self.sprite_sheet = sprite_sheet
        self.anim_dict = self.initialize_anim_dict()
        if anim:
            self.current_anim = anim
        else:
            self.current_anim = list(self.anim_dict.keys())[0]

    def initialize_anim_dict(self):
        """
        Initialize animations for the player character.

        Load necessary animations, images, and character customization options for the player.

        Returns:
            dict: A dictionary where keys are animation names and values are Animation objects.
        """
        # Load in body images
        anim_dict = {}
        anims = get_anims_in_sprite_sheet(self.sprite_sheet[0])
        for anim in anims:
            anim_dict[anim] = Animation(
                sprite_sheets=self.sprite_sheet,
                animation=anim
            )
        return anim_dict

    def make_new_animation(self, sprite_sheets: list[Path]):
        """Replace the current layers with a new set of sprite sheets"""
        # Load in body images
        anim_dict = {}
        anims = get_anims_in_sprite_sheet(sprite_sheets[0])
        for anim in anims:
            anim_dict[anim] = Animation(
                sprite_sheets=sprite_sheets,
                animation=anim
            )
        self.anim_dict = anim_dict

    def get_image(self):
        """Get the current image of the character.

        Returns:
            pygame.Surface: The current image of the character.
        """
        return self.anim_dict[self.current_anim]

    def update(self, *_args, **_kwargs):
        """Update the character's animation."""
        self.anim_dict[self.current_anim].update()

    def set_animation(self, anim):
        """Set the current animation for the character.

        Args:
            anim (str): The name of the animation to set.
        """
        if anim in self.anim_dict:
            self.current_anim = anim

    def get_current_anim(self):
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

class HitBox:
    """An entity's hitbox.
    
    Used for collision events.
    """
    def __init__(self, x_pos, y_pos, appearance) -> None:
        data = get_sprite_data(appearance.sprite_sheet[0])
        self.x_offset, self.y_offset = self.get_offset(appearance.sprite_sheet[0])
        self.rect = pg.Rect(
            x_pos + self.x_offset,
            y_pos + self.y_offset,
            data["sheet_data"]["hit_box_w"],
            data["sheet_data"]["hit_box_h"]
            )

    def get_offset(self, sprite):
        """Difference between a characters sprite size and hitbox."""
        data = get_sprite_data(sprite)
        frame_w = data["sheet_data"]["tile_w"]
        frame_h = data["sheet_data"]["tile_h"]
        hit_box_w = data["sheet_data"]["hit_box_w"]
        hit_box_h = data["sheet_data"]["hit_box_h"]
        x_offset = frame_w - hit_box_w
        y_offset = frame_h - hit_box_h
        return x_offset, y_offset

    def move(self, x, y):
        """Move the hitbox."""
        self.rect.x = x + self.x_offset
        self.rect.y = y + self.y_offset

    def draw(self, screen, camera):
        """Draw hitbox to screen."""
        pg.draw.rect(screen, (255,0,0), camera.apply(self), 2)
