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
from config.directories import USER_GAME_DIR, SPRITES_DIR
from utils.save_system import save_game_data
from entities.player_character import PlayerCharacter
from entities.npc import NPC
from maps.map import TiledMap
from maps.camera import Camera
from items.inventory import CharacterInventory

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
        self.camera = Camera()
        self.save_data = {}
        self.sprite_groups = self.init_sprite_groups()
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
            if event.type == pg.VIDEORESIZE:
                self.camera.change_screen_size()
        ###########################    END TEST    ###############################
        self.player.handle_events(events)

    def update(self, *args):
        """Update logic for the gameplay state."""
        for sprite in self.sprite_groups["characters"]:
            sprite.update(
                tile_map = self.map,
                sprite_group = self.sprite_groups["all_sprites"]
                )
        self.map.update()
        self.camera.update(self.player.hitbox)

    def draw(self, screen, *args):
        """Draw the gameplay on the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        screen.fill(MYSTIC_BLUE)
        self.map.draw(screen, self.camera)
        self.draw_grid(screen)
        #self.player.draw(screen, self.camera)
        for sprite in self.sprite_groups["all_sprites"]:
            sprite.draw(screen, self.camera)

    def draw_grid(self, screen):
        """Draw tiles on screen."""
        w, h = pg.display.get_surface().get_size()
        for x in range(0, w, TILESIZE):
            pg.draw.line(screen, BLACK, (x,0), (x, h))
        for y in range(0, h, TILESIZE):
            pg.draw.line(screen, BLACK, (0, y), (w, y))

    def init_sprite_groups(self):
        """Create a dict of sprite groups to store dynamic objects.
        
        This dict organizes all the sprites in a map that have some sort of logic. Allowing
        them to be easily updated all at once.
        """
        return {
            "all_sprites" : pg.sprite.Group(),
            "characters" : pg.sprite.Group(),
            "player" : pg.sprite.Group(),
            "npcs" : pg.sprite.Group()
        }

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

    def open_map(self, map_name: str):
        """Open and load a map.

        This method will initialize a TiledMap and store any dynamic objects,
        suchs as NPCs, in it's own sprite_group dict. This allows game logic to
        be applied to groups separately.

        Note: Static objects such as walls are stored in the map object.

        Args:
            map_name (str): The name of the map to load.
        """
        self.map = TiledMap(map_name)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name.lower() == "npc":
                groups = [
                    self.sprite_groups["all_sprites"],
                    self.sprite_groups["characters"],
                    self.sprite_groups["npcs"]
                    ]
                NPC(
                    name = tile_object.name_id,
                    x = tile_object.x,
                    y = tile_object.y,
                    groups = groups
                )
        self.camera.open_map(self.map)

    def load_data(self, data: dict, tags: list[str]) -> None:
        """Load game data based on tags.

        Args:
            data (dict): The game data to load. This dict should always contain
                the key "case" indicating the type of data meant to be loaded.
            tags (list[str]): Tags indicating how to handle the data.

        Current Implemented Cases:
        - "player": The data being passes is keyword args meant for a PlayerCharacter.
        -"saved_game": The data being loaded is a previously saved game.

        Current Implemented Tags:
        - "NEW_GAME": Starts a new game when the data passed is a PlayerCharacter.

        The method processes the provided data based on the specified tags. Each tag
        triggers a different action or behavior within the method.
        """
        case = data.pop("case")
        print(data)
        match case:
            case "player":
                if "NEW_GAME" in tags:
                    self.new_game(
                        PlayerCharacter(
                            **data,
                            groups = [
                                self.sprite_groups["all_sprites"],
                                self.sprite_groups["characters"],
                                self.sprite_groups["player"]
                                ]
                            )
                    )
                else: self.load_player(
                    PlayerCharacter(
                            **data,
                            groups = [
                                self.sprite_groups["all_sprites"],
                                self.sprite_groups["characters"],
                                self.sprite_groups["player"]
                                ]
                            )
                    )
            case "saved_game": self.load_game(data)
            case _: print("Case not recognized.")

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
            data = save_dict["player_data"]["data"],
            name = save_dict["player_data"]["name"],
            x = save_dict["player_data"]["x"],
            y = save_dict["player_data"]["y"],
            inventory = save_dict["player_data"]["inventory"],
            sprite_sheet = save_dict["player_data"]["sprite_sheet"],
            groups = [
                self.sprite_groups["all_sprites"],
                self.sprite_groups["characters"],
                self.sprite_groups["player"]
                ]
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
        name = self.player.data["name"]
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
            "case" : "saved_game",
            "player_data" : self.player.get_save_data(),
            "map" : self.map.name,
            "file_path" : self.file_path
        }
        save_game_data(self.file_path, save_data)
