"""Portal Class and subclasses.

These classes are used to transition from map to map.
"""
import pygame as pg
from config.game_settings import TILESIZE
from gui.message_box import MessageBox
from states.sequencer import Scene, Sequencer, SceneAction, ExecutableMethod
from sfx.fader import Fader
from states.gameplay.message_substate import MessageBoxSubState

class Portal:
    """A parent class for static map objects."""
    def __init__(self, rect: pg.Rect, name:str, properties: dict, img: pg.Surface = None):
        self.rect = rect
        self.name = name
        self.pid = properties["pid"]
        self.to_pid = properties["to_pid"]
        self.img = img

    def interact(self, game_state):
        box = MessageBox(
            [
                f"It's a {type(self).__name__}...",
                f"It looks like it goes to {self.name}!"
            ]
        )
        MessageBoxSubState(game_state, box).run()

    def draw(self, screen, camera):
        if self.img:
            screen.blit(self.img, camera.apply_rect(self.rect))
        pg.draw.rect(screen, (255,0,255), camera.apply_rect(self.rect), 2)

    def get_enter_seq(self, character):
        return Sequencer(self.get_enter_scenes(character))

    def get_exit_seq(self, character):
        return Sequencer(self.get_exit_scenes(character))

    def get_enter_scenes(self, character):
        dx = self.rect.x - character.hitbox.rect.x
        dy = self.rect.y - character.hitbox.rect.y
        return [Scene(
            "Enter Portal",
            [SceneAction(
                ExecutableMethod(character, "change_destination", [dx,dy,[]])
                )]
            )]

    def get_exit_scenes(self, character):
        """This should be implemented in subclasses if they have special outro
        if you want special transitions.
        
        e.g. Doors having a scene to close the doors
        """
        return [Scene("Exit Portal", [])]

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

    def interact(self, game_state):
        self.open_state = (self.open_state + 1) % 2
        return super().interact(game_state)

    def is_open(self):
        return self.open_state

    def get_enter_seq(self, character):
        seq = super().get_enter_seq(character)
        return seq

    def get_exit_seq(self, character):
        return Sequencer(self.get_exit_scenes(character))

    def get_enter_scenes(self, character):
        super_scenes = super().get_enter_scenes(character)
        open_door = Scene(
            "Open Door",
            [SceneAction(ExecutableMethod(self, "open_door"))],
            post_delay=.1
            )
        super_scenes.insert(0, open_door)
        return super_scenes

    def get_exit_scenes(self, character):
        dx, dy = 0, 0
        anim = character.appearance.current_anim
        if "up" in anim:
            dy -= TILESIZE
        if "down" in anim:
            dy += TILESIZE
        if "left" in anim:
            dx -= TILESIZE
        if "right" in anim:
            dx += TILESIZE
        scene1 = Scene("Open Door", [SceneAction(ExecutableMethod(self, "open_door"))])
        scene2 = Scene(
            "Exit Portal",
            [SceneAction(ExecutableMethod(character, "change_destination", [dx,dy,[]]))],
            pre_delay = 0.1
            )
        scene3 = Scene("Close Door", [SceneAction(ExecutableMethod(self, "close_door"))])
        return [scene1, scene2, scene3]
