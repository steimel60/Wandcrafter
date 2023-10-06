import pygame as pg
from pathlib import Path
from config.directories import ANIM_DIR
from config.game_settings import FPS

class Animation:
    def __init__(self, folder_name, frame_duration):
        self.path = ANIM_DIR / folder_name
        self.images = [pg.image.load(f) for f in self.path.iterdir()]
        self.n_frames = len(self.images)
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.elapsed_frames = 0
        self.finished = False

    def update(self):
        self.elapsed_frames += 1

        if self.elapsed_frames >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % self.n_frames
            self.elapsed_frames = 0

    def get_current_frame(self):
        return self.images[self.current_frame]
