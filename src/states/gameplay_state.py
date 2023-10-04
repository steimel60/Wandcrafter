from .state_base import State
from config.colors import *

class GameplayState(State):
    def __init__(self):
        super().__init__()
        self.game_data = None

    def update(self, events):
        # Update logic for the gameplay state
        #print(self.game_data.data["PLAYER_DATA"].name)
        pass

    def draw(self, screen):
        # Draw the gameplay on the screen
        screen.fill(MYSTIC_BLUE)

    def set_game_data(self, game_data):
        self.game_data = game_data

    def open_map(self, level):
        self.game_data.data["GAME_DATA"]["map"] = level