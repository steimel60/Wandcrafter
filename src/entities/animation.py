"""
Module for handling animations from sprite sheets.

This module contains the `Animation` class, which is designed to represent and manage animations
from sprite sheets. It provides functionality to load animation frames, update the current frame,
and retrieve the current animation frame.
"""

from pathlib import Path
import pygame as pg
from config.directories import ANIM_DIR
from utils.asset_management import get_anim_data

class Animation:
    """
    Represents an animation from a sprite sheet.

    This class loads and manages animations from a sprite sheet, allowing you to easily
    cycle through animation frames and retrieve the current frame.

    Attributes:
        sprite_sheet (pygame.Surface): The sprite sheet containing animation frames.
        anim_data (dict): Dictionary containing information like frame width, height and duration.
        frames (list[pg.Surface]): Individual images in the animation.
        current_frame (int): Index representing which frame is currently being played.
        frame_timer (int): Counter showing how many frames the current image has been displayed.

    Methods:
        load_frames(): Load animation frames from the sprite sheet.
        update(): Update the animation frame based on the frame duration.
        get_current_frame(): Get the current frame of the animation.
    """
    def __init__(self,
                 sprite_sheet : str,
                 animation : str
                 ):
        """
        Initialize an Animation object.

        Args:
            sprite_sheet (str): The name of the sprite sheet containing the animation frames.
            animation (str): The name of the animation to load from the sprite sheet.
        """
        self.sprite_sheet = pg.image.load(
            Path(ANIM_DIR / f"{sprite_sheet}.png")
        )
        self.anim_data = get_anim_data(sprite_sheet, animation)
        self.frames = self.load_frames()
        self.current_frame = 0
        self.frame_timer = 0

    def load_frames(self):
        """
        Load animation frames from the sprite sheet.

        Returns:
            list: A list of pygame Surfaces, each representing a frame of the animation.
        """
        frames = []
        for x in self.anim_data["seq"]:
            frame_rect = pg.Rect(
                x * self.anim_data["frame_w"],
                self.anim_data["row"] * self.anim_data["frame_h"],
                self.anim_data["frame_w"],
                self.anim_data["frame_h"]
            )
            frame = self.sprite_sheet.subsurface(frame_rect)
            frames.append(frame)
        return frames

    def update(self):
        """
        Update the animation frame based on the frame duration.
        """
        self.frame_timer += 1
        if self.frame_timer >= self.anim_data["duration"]:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        """
        Get the current frame of the animation.

        Returns:
            pygame.Surface: The current frame as a pygame Surface.
        """
        return self.frames[self.current_frame]
