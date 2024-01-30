import pygame as pg
from states.states import State, SubState
from gui.message_box import MessageBox

class MessageBoxSubState(SubState):
    def __init__(self, parent: State, msg_box: MessageBox) -> None:
        super().__init__(parent)
        self.msg_box = msg_box
        self.running = True

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        if self.msg_box.next_tab_exists():
                            self.msg_box.next_tab()
                        elif self.msg_box.next_message_exists():
                            self.msg_box.next_message()
                        else: self.running = False

    def draw(self, screen):
        self.parent.draw(screen)
        self.msg_box.draw(screen)

    def update(self):
        super().update()
        self.parent.update()