"""Portal Class and subclasses.

These classes are used to transition from map to map.
"""
import pygame as pg
from gui.message_box import MessageBox
from states.sequencer import Scene, Sequencer
from sfx.fader import FadeOut

class Portal:
    """A parent class for static map objects."""
    def __init__(self, rect: pg.Rect, name:str, properties: dict, img: pg.Surface = None):
        self.rect = rect
        self.name = name
        self.pid = properties["pid"]
        self.to_pid = properties["to_pid"]
        self.img = img

    def interact(self):
        box = MessageBox(
            [
                f"It's a {type(self).__name__}...",
                f"It looks like it goes to {self.name}!"
            ]
        )
        return ["CHANGE_STATE", "message_box", box]

    def draw(self, screen, camera):
        if self.img:
            screen.blit(self.img, camera.apply_rect(self.rect))
        pg.draw.rect(screen, (255,0,255), camera.apply_rect(self.rect), 2)

    def get_map_change_seq(self, character, game_state):
        """Creates a sequencer for an entire map change.
        
        Includes the following scenes:
        - Walk In: Player walks in to the portal.
        - Map Change: No anim, just executes map change.
        - Walk Out: Player walks 1 tile in current direction.
        """
        dx = self.rect.x - character.hitbox.rect.x
        dy = self.rect.y - character.hitbox.rect.y
        walk_in = Scene(
            character,
            "change_destination",
            [dx, dy, []],
            "has_arrived"
        )
        change_map = Scene(
            game_state,
            "use_portal",
            [self],
            "test"
        )
        walk_out = Scene(
            character,
            "change_destination",
            [dx, dy, []],
            "has_arrived",
            pre_delay=0.5
        )
        return Sequencer([walk_in, change_map, walk_out])

class Door(Portal):
    def __init__(self, rect, name, properties, frames):
        super().__init__(rect, name, properties)
        self.is_locked = properties["is_locked"]
        self.open_state = 0
        self.frames = frames

    def draw(self, screen, camera):
        """Draw the current frame to the screen."""
        screen.blit(
            self.frames[self.open_state][0],
            camera.apply_rect(self.rect)
        )

    def update(self):
        pass

    def open_door(self):
        self.open_state = 1

    def close_door(self):
        self.open_state = 0

    def interact(self):
        self.open_state = (self.open_state + 1) % 2
        return super().interact()

    def is_open(self):
        return self.open_state

    def get_map_change_seq(self, character, game_state) -> Sequencer:
        """Returns the sequencer for map change via door."""
        portal_seq = super().get_map_change_seq(character, game_state)
        open_door = Scene(
            self,
            "open_door",
            [],
            "is_open",
            pre_delay=0,
            post_delay=0.5
        )
        portal_seq.insert_seq(0, open_door)
        return portal_seq
