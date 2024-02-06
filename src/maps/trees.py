from maps.obstacles import Obstacle, AnimatedObstacle
from states.sub_message import MessageBoxSubState
from gui.message_box import MessageBox
from config.game_settings import FPS
from items.item import Item, action, quick_action

class Tree(Obstacle):
    def __init__(self, rect, type):
        super().__init__(rect)
        self.type = type

    def interact(self, game_state):
        i = 0
        for label, _ in self.get_quick_actions():
            print(f"Press {i} to {label}.")
            i += 1
        selection = int(input("Make Selection:")) # Implement gui option later
        self.get_quick_actions()[selection][1](game_state)

    @quick_action
    def inspect(self, game_state):
        MessageBoxSubState(game_state, MessageBox([f"It's a beautiful {self.type} tree!"])).run()

    @quick_action
    def collect(self, game_state):
        game_state.player.inventory.add_item(Stick(self.type))
        MessageBoxSubState(game_state, MessageBox([f"You collected 1 {self.type} stick!"])).run()
        print(game_state.player.inventory.bag)

class MagicTree(Tree):
    def __init__(self, frames, rect, type):
        super().__init__(rect, type)
        self.frames = frames
        self.frame_time = 0
        self.curr_frame = 0

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
    
    @quick_action
    def collect(self, game_state):
        game_state.player.inventory.add_item(MagicStick(self.type))
        MessageBoxSubState(game_state, MessageBox([f"You collected 1 magic {self.type} stick!"])).run()
        print(game_state.player.inventory.bag)

class Stick(Item):
    def __init__(self, type) -> None:
        self.type = type

class MagicStick(Stick):
    def __init__(self, type) -> None:
        super().__init__(type)