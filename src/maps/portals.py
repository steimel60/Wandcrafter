"""Portal Class and subclasses.

These classes are used to transition from map to map.
"""
import pygame as pg
from config.game_settings import TILESIZE
from gui.message_box import MessageBox
from states.sequencer import Scene, Sequencer, SceneAction, ExecutableMethod
from sfx.fader import Fader, get_fade_action
from states.sub_message import MessageBoxSubState

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

    def get_enter_seq(self, game_state):
        return Sequencer(self.get_enter_scenes(game_state))

    def get_exit_seq(self, game_state):
        return Sequencer(self.get_exit_scenes(game_state))

    def get_enter_scenes(self, game_state):
        dx = self.rect.x - game_state.player.hitbox.rect.x
        dy = self.rect.y - game_state.player.hitbox.rect.y
        fader1, fade_out_action = get_fade_action(game_state, is_fade_in=False, fade_time=.75)
        return [Scene("Enter Portal",
            [
                SceneAction(
                    action_method=ExecutableMethod(game_state.player, "change_destination", [dx,dy,[]]),
                    condition_method=ExecutableMethod(game_state.player, "has_arrived", [])
                    ),
                fade_out_action
            ])]

    def get_exit_scenes(self, game_state):
        """This should be implemented in subclasses if they have special outro
        if you want special transitions.
        
        e.g. Doors having a scene to close the doors
        """
        fader1, fade_in_action = get_fade_action(game_state, is_fade_in=True, fade_time=.75)
        return [Scene("Exit Portal", [fade_in_action])]

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
        self.open_state = 1 % len(self.frames)

    def close_door(self):
        self.open_state = 0

    def interact(self, game_state):
        self.open_state = (self.open_state + 1) % len(self.frames)
        return super().interact(game_state)

    def is_open(self):
        return self.open_state

    def get_enter_seq(self, game_state):
        seq = super().get_enter_seq(game_state)
        return seq

    def get_exit_seq(self, game_state):
        return Sequencer(self.get_exit_scenes(game_state))

    def get_enter_scenes(self, game_state):
        super_scenes = super().get_enter_scenes(game_state)
        open_door = Scene(
            "Open Door",
            [SceneAction(ExecutableMethod(self, "open_door"))],
            post_delay=.1
            )
        super_scenes.insert(0, open_door)
        return super_scenes

    def get_exit_scenes(self, game_state):
        dx, dy = 0, 0
        anim = game_state.player.appearance.current_anim
        if "up" in anim:
            dy -= TILESIZE
        if "down" in anim:
            dy += TILESIZE
        if "left" in anim:
            dx -= TILESIZE
        if "right" in anim:
            dx += TILESIZE
        fader1, fade_in_action = get_fade_action(game_state, is_fade_in=True, fade_time=.75)
        scene1 = Scene(
            "Exit Portal",
            [
                SceneAction(ExecutableMethod(self, "open_door")),
                SceneAction(
                    action_method=ExecutableMethod(game_state.player, "change_destination", [dx,dy,[]]),
                    condition_method=ExecutableMethod(game_state.player, "has_arrived", [])
                    ),
                fade_in_action
            ]
            )
        scene2 = Scene("Close Door", [SceneAction(ExecutableMethod(self, "close_door"))])
        return [scene1, scene2]
