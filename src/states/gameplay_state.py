from pathlib import Path
from .state_base import State
from config.colors import *
from config.directories import USER_GAME_DIR
from utils.save_system import save_game_data

# CLASSES FOR LOAD MACTH STATEMENT
from entities.player_entity import PlayerEntitiy
from maps.map import TiledMap

class GameplayState(State):
    def __init__(self, path = None, player = None, map = None): 
        super().__init__()
        self.FILE_PATH = path
        self.player = player
        self.map = map
        self.save_data = dict()

    def handle_events(self, events):
        self.player.handle_events(events)

    def update(self):
        # Update logic for the gameplay state
        self.player.update()

    def draw(self, screen):
        # Draw the gameplay on the screen
        screen.fill(MYSTIC_BLUE)
        self.map.draw(screen)
        self.player.draw(screen)

    def set_filepath(self, new_path: Path):
        if new_path.suffix == ".pkl": self.FILE_PATH = new_path

    def set_game_data(self, game_data):
        self.game_data = game_data

    def set_player(self, player):
        self.player = player

    def set_quest_data(self, quest_data):
        self.quest_data = quest_data

    def open_map(self, map_name):
        self.map = TiledMap(map_name)

    def load_data(self, data, tags):
        match data:
            case PlayerEntitiy():
                self.new_game(data) if "NEW_GAME" in tags else self.load_player(data)
            case _: self.load_game(data)

    def load_player(self, player):
        self.set_player(player)

    def load_game(self, save_dict):
        player = PlayerEntitiy(
            name = save_dict["player_data"]["name"],
            wand = save_dict["player_data"]["wand"],
            coord = save_dict["player_data"]["coord"]
        )
        self.set_player(player)
        self.open_map(save_dict["map"])
        self.set_filepath(save_dict["file_path"])

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
        save_data = {
            "player_data" : self.player.get_save_data(),
            "map" : self.map.name,
            "file_path" : self.FILE_PATH
        }
        save_game_data(self.FILE_PATH, save_data)