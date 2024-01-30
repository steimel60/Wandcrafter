import pygame as pg
from config.game_settings import FPS

class AnimatedTile:
    """A parent class for objects that are animated directly in the map.
    
    Params:
        - frames: A list of AnimationFrame objects from pytmx. The property
        "gid" can be used to load the image and the property "duration" is
        the time in milliseconds the frame should be displayed/
        - rect: pg.Rect that represents the objects hitbox.
    """
    def __init__(self, frames, rect: pg.Rect):
        self.frames = frames
        self.frame_time = 0
        self.curr_frame = 0
        self.rect = rect

    def update(self):
        """Add time and switch frames if needed."""
        self.frame_time += 1 / FPS
        if self.frame_time >= (self.frames[self.curr_frame][1] / 1000):
            self.frame_time = 0
            self.curr_frame += 1

        if self.curr_frame >= len(self.frames):
            self.curr_frame = 0

    def draw(self, screen, camera):
        """Draw the current frame to the screen."""
        screen.blit(
            self.frames[self.curr_frame][0],
            camera.apply_rect(self.rect)
        )
