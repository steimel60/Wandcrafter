"""
Module for handling animations from sprite sheets.

This module contains the `Animation` class, which is designed to represent and manage animations
from sprite sheets. It provides functionality to load animation frames, update the current frame,
and retrieve the current animation frame.
"""

from pathlib import Path
import pygame as pg
from utils.asset_management import get_anim_data

class Animation:
    def __init__(self,
                 sprite_sheets : list[Path],
                 animation : str
                 ):
        """
        Initialize an Animation object.

        Args:
            sprite_sheets (str or list[str]): The name of the sprite sheet(s) containing 
                the animation frames.
            animation (str): The name of the animation to load from the sprite sheet.
        """
        if isinstance(sprite_sheets, Path):
            sprite_sheets = [sprite_sheets]  # Convert a single string to a list of one string
        sprite_sheets = [path.with_suffix(".png") for path in sprite_sheets]
        self.sprite_sheets = sprite_sheets
        self.name = animation
        self.layers = self.create_layers()
        self.frames = self.create_frames()
        self.duration = self.get_duration()
        self.current_frame = 0
        self.frame_timer = 0

    def create_layers(self):
        """
        Initialize AnimationLayers for each sprite sheet used in the animation.
        
        Returns: list[AnimationLayers]
        """
        layers = []
        # Initiate layers
        for sprite_sheet in self.sprite_sheets:
            layer = AnimationLayer(sprite_sheet, self.name)
            layers.append(layer)
        return layers

    def create_frames(self):
        """
        Load animation frames from the sprite sheet.

        Returns:
            list: A list of pygame Surfaces, each representing a frame of the animation.
        """
        # Variables to check for errors
        n_frames = len(self.layers[0].frames)
        height = self.layers[0].anim_data["frame_h"]
        width = self.layers[0].anim_data["frame_w"]
        # Make sure layers are compatible
        if not all(len(l.frames) == n_frames for l in self.layers):
            raise ValueError("Not all layers have the same number of frames")
        if not all(l.anim_data["frame_h"] == height for l in self.layers):
            raise ValueError("Not all layers have the same height")
        if not all(l.anim_data["frame_w"] == width for l in self.layers):
            raise ValueError("Not all layers have the same width")
        # Create combined images
        frames = []
        n_layers = len(self.layers)
        for i in range(n_frames):
            frame = self.layers[0].frames[i].copy()
            for j in range(1,n_layers):
                frame.blit(self.layers[j].frames[i],(0,0))
            frames.append(frame)
        return frames

    def get_duration(self):
        """Get the duration each frame is shown on screen."""
        duration = self.layers[0].anim_data["duration"]
        if not all(l.anim_data["duration"] == duration for l in self.layers):
            raise ValueError("Not all layers have the same duration")
        return duration

    def update(self):
        """
        Update the animation frame based on the frame duration.
        """
        self.frame_timer += 1
        if self.frame_timer >= self.duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        """
        Get the current frame of the animation.

        Returns:
            pygame.Surface: The current frame as a pygame Surface.
        """
        return self.frames[self.current_frame]

class AnimationLayer:
    """A single component to be combined to create an animation.
    
    For example, a character may be made up of a body layer, clothing layer,
    and equipment layer, all combined to create the character's appearance.
    """
    def __init__(self,
                 sprite_sheet : Path,
                 animation : str
                 ):
        """
        Initialize an Animation object.

        Args:
            sprite_sheet (str): The name of the sprite sheet containing the animation frames.
            animation (str): The name of the animation to load from the sprite sheet.
        """
        self.sprite_sheet = pg.image.load(sprite_sheet)
        self.anim_data = get_anim_data(sprite_sheet, animation)
        self.frames = self.load_frames()

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
