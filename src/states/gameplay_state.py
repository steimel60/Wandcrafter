"""
GameplayState Module

This module defines the `GameplayState` class, which represents the game state
where the player is actively playing the game.
"""

from pathlib import Path
import pygame as pg
from states.state_base import State
from config.colors import MYSTIC_BLUE, BLACK
from config.game_settings import TILESIZE
from config.directories import USER_GAME_DIR
from utils.save_system import save_game_data
from entities.player_character import PlayerCharacter
from maps.map import TiledMap

class GameplayState(State):
    """
    GameplayState Class

    This class represents the game state where the player is actively playing
    the game. It manages game events, updates, and rendering of the game world.
    """
    def __init__(self, path = None, player = None, tile_map = None):
        """Initialize the Gameplay State.
            
        Args:
            path (Path, optional): The file path for saving/loading the game. Defaults to None.
            player (PlayerCharacter, optional): The player entity. Defaults to None.
            tile_map (TiledMap, optional): The tile map. Defaults to None.
        """
        super().__init__()
        self.file_path = path
        self.player = player
        self.map = tile_map
        self.save_data = {}
        self.quest_data = None

    def handle_events(self, events, *args):
        """Handle events in the gameplay state.

        Args:
            events (list): A list of pygame events to process.
        """
        ####### TESTING SAVE FUNCTIONALITY, MAKE BETTER EVENT CATCH LATER #######
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_y:
                        self.save_game()
        ###########################    END TEST    ###############################
        self.player.handle_events(events)

    def update(self, *args):
        """Update logic for the gameplay state."""
        self.player.update()

    def draw(self, screen, *args):
        """Draw the gameplay on the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        screen.fill(MYSTIC_BLUE)
        self.map.draw(screen)
        self.draw_grid(screen)
        self.player.draw(screen)

    def draw_grid(self, screen):
        """Draw tiles on screen."""
        w, h = pg.display.get_surface().get_size()
        for x in range(0, w, TILESIZE):
            pg.draw.line(screen, BLACK, (x,0), (x, h))
        for y in range(0, h, TILESIZE):
            pg.draw.line(screen, BLACK, (0, y), (w, y))

    def set_filepath(self, new_path: Path):
        """Set the file path for saving/loading the game.

        Args:
            new_path (Path): The new file path.
        """
        if new_path.suffix == ".pkl":
            self.file_path = new_path

    def set_player(self, player):
        """Set the player entity.

        Args:
            player (PlayerCharacter): The player entity to set.
        """
        self.player = player

    def set_quest_data(self, quest_data):
        """Set the quest data.

        Args:
            quest_data: The quest data to set.
        """
        self.quest_data = quest_data

    def open_map(self, map_name):
        """Open and load a map.

        Args:
            map_name (str): The name of the map to load.
        """
        self.map = TiledMap(map_name)

    def load_data(self, data, tags):
        """Load game data based on tags.

        Args:
            data: The game data to load.
            tags: Tags indicating how to handle the data.

        Current Implemented Tags:
        - "NEW_GAME": Starts a new game when the data passed is a PlayerCharacter.

        The method processes the provided data based on the specified tags. Each tag
        triggers a different action or behavior within the method.
        """

        match data:
            case PlayerCharacter():
                if "NEW_GAME" in tags:
                    self.new_game(data)
                else: self.load_player(data)
            case _: self.load_game(data)

    def load_player(self, player):
        """Load a player entity.

        Args:
            player (PlayerCharacter): The player entity to load.
        """
        self.set_player(player)

    def load_game(self, save_dict):
        """Load a saved game.

        Args:
            save_dict: A dictionary containing saved game data.
        """
        player = PlayerCharacter(
            name = save_dict["player_data"]["name"],
            wand = save_dict["player_data"]["wand"],
            x = save_dict["player_data"]["x"],
            y = save_dict["player_data"]["y"]
        )
        self.set_player(player)
        self.open_map(save_dict["map"])
        self.set_filepath(save_dict["file_path"])

    def new_game(self, player):
        """Start a new game.

        Args:
            player (PlayerCharacter): The player entity for the new game.
        """
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
        """Save the current game data."""
        save_data = {
            "player_data" : self.player.get_save_data(),
            "map" : self.map.name,
            "file_path" : self.file_path
        }
        save_game_data(self.file_path, save_data)
