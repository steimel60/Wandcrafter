import pygame as pg
from states.sequencer import Scene, SceneAction, ExecutableMethod, Sequencer
from config.game_settings import FPS

class Fader:
    def __init__(self, game_state, is_fade_in, color = (0,0,0), fade_time = 1) -> None:
        info = pg.display.Info()
        self.is_fade_in = is_fade_in
        self.gs = game_state
        self.img = pg.Surface(
            (info.current_w,info.current_h), # screen size
            pg.SRCALPHA # allow alpha
            )
        self.fade_time = fade_time
        self.color = color
        self.timer = 0

    def update(self):
        self.timer += 1 / FPS
        if self.is_fade_in:
            alpha = max(0, 255 - (255 * (self.timer / self.fade_time))) # Fade out
        else:
            alpha = min(255 * (self.timer / self.fade_time), 255) # Fade in
        self.img.set_alpha(alpha)

    def draw(self, screen, _camera):
        self.img.fill(self.color)
        screen.blit(self.img, (0,0))

    def is_done(self):
        return self.timer > self.fade_time

    def end_fade(self):
        self.gs.sprite_groups["all_sprites"].remove(self)

    def place_holder(self):
        pass

    def start_fade(self):
        self.gs.sprite_groups["all_sprites"].append(self)

def get_fade_action(game_state, is_fade_in: bool, include_end: bool = False, color = (0,0,0), fade_time = 1) -> (Fader, SceneAction):
    fader = Fader(
        game_state,
        is_fade_in=is_fade_in,
        color=color,
        fade_time=fade_time)
    fade_out = ExecutableMethod(fader, "start_fade")
    fade_check = ExecutableMethod(fader, "is_done")
    remove_fade = None
    if include_end:
        remove_fade = ExecutableMethod(fader, "end_fade")
    fade_action = SceneAction(
        action_method=fade_out,
        condition_method=fade_check,
        final_method=remove_fade
    )
    return fader, fade_action
