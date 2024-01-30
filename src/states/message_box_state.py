import pygame as pg
from states.states import State
from gui.message_box import MessageBox

class MessageBoxState(State):
    def __init__(self, manager, msg_box: MessageBox, last_state: str):
        super().__init__(manager)
        self.msg_box = msg_box
        self.last_state = last_state

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        if self.msg_box.next_tab_exists():
                            self.msg_box.next_tab()
                        elif self.msg_box.next_message_exists():
                            self.msg_box.next_message()
                        else: self.manager.change_state(self.last_state)

    def draw(self, screen):
        self.msg_box.draw(screen)

    def update(self):
        super().update()
