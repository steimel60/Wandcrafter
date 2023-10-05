from pathlib import Path
from .state_base import State
from config.colors import *
from config.directories import USER_GAME_DIR
from utils.save_system import save_game_data, load_game

# CLASSES FOR LOAD MACTH STATEMENT
from entities.player_entity import PlayerEntitiy

class GameplayState(State):
    def __init__(self, path = None, player = None,
                g_data = {"map":"test"}, q_data = None): 
        super().__init__()
        self.FILE_PATH = path
        self.player = player
        self.game_data = g_data
        self.quest_data = q_data

    def update(self, events):
        # Update logic for the gameplay state
        #print(self.player.name)
        pass

    def draw(self, screen):
        # Draw the gameplay on the screen
        screen.fill(MYSTIC_BLUE)

    def set_filepath(self, new_path: Path):
        if new_path.suffix == ".pkl": self.FILE_PATH = new_path

    def set_game_data(self, game_data):
        self.game_data = game_data

    def set_player(self, player):
        self.player = player

    def set_quest_data(self, quest_data):
        self.quest_data = quest_data

    def open_map(self, level):
        self.game_data["map"] = level

    def load_data(self, data, tags):
        match data:
            case GameplayState():
                self.load_game_state(data)
            case PlayerEntitiy():
                self.new_game(data) if "NEW_GAME" in tags else self.load_player(data)
    
    def load_game_state(self, loaded_state):
        self.set_filepath(loaded_state.FILE_PATH)
        self.set_player(loaded_state.player)
        self.set_game_data(loaded_state.game_data)
        self.set_quest_data(loaded_state.quest_data)

    def load_player(self, player):
        self.set_player(player)

    def new_game(self, player):
        self.set_player(player)
        self.open_map("test")
        name = self.player.name
        filename = f"{name}.pkl"
        i = 2
        while Path.exists(USER_GAME_DIR / filename):
            filename = f"{name}_{i}.pkl"
            i += 1
        self.set_filepath(USER_GAME_DIR / filename)
        self.save_game()

    def save_game(self):
        save_game_data(self.FILE_PATH, self)