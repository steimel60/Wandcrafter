"""Portal Class and subclasses.

These classes are used to transition from map to map.
"""
import pygame as pg
from config.game_settings import FPS
from gui.message_box import MessageBox

class Portal:
    """A parent class for static map objects."""
    def __init__(self, rect: pg.Rect, pid: int):
        self.rect = rect
        self.pid = pid

    def interact(self):
        box = MessageBox(
            [
                f"It's a {type(self).__name__}...",
                f"Here's its save dict: {vars(self)}"
            ]
        )
        return ["CHANGE_STATE", "message_box", box]
