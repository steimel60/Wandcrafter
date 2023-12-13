import pygame as pg
from states.state_base import State

class MessageBoxState(State):
    def __init__(self, msg_box, last_state):
        self.msg_box = msg_box
        self.last_state = last_state

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        return ["CHANGE_STATE", self.last_state]

    def draw(self, screen):
        self.msg_box.draw(screen)

    def update(self):
        super().update()
