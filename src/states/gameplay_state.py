"""
GameplayState Module

This module defines the `GameplayState` class, which represents the game state
where the player is actively playing the game.
"""

import json
from pathlib import Path
import pygame as pg
from states.state_base import State
from config.colors import MYSTIC_BLUE, BLACK
from config.game_settings import TILESIZE
from config.directories import USER_GAME_DIR, DATA_DIR
from utils.save_system import save_game_data
from entities.player_character import PlayerCharacter
from entities.npc import NPC
from maps.map import TiledMap
from maps.camera import Camera

### TEST ONLLY ###
from gui.message_box import MessageBox
from entities.animals import Animal

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

    def handle_events(self, events):
        """Handle events in the gameplay state.

        Args:
            events (list): A list of pygame events to process.
        """
        self.handle_global_events(events)
        response = self.handle_player_events(events)
        self.handle_continuous_player_movement()
        return response

    def handle_global_events(self, events):
        """Handle global events."""
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_y:
                        self.save_game()
            if event.type == pg.VIDEORESIZE:
                self.camera.change_screen_size()

    def handle_player_events(self, events):
        """Logic for key up/down events involving the player character."""
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        if "idle" in self.player.appearance.current_anim:
                            print("INTERACT EVENT")
                            return self.player.interact(self.map.obstacles)
                    ########## TEST EVENTS #############
                    case pg.K_i:
                        if "idle" in self.player.appearance.current_anim:
                            print("EQUIP EVENT")
                            self.player.inventory.equip(self.player.inventory.bag[-1])
                            self.player.update_appearance()
                    case pg.K_u:
                        if "idle" in self.player.appearance.current_anim:
                            print("UNEQUIP EVENT")
                            self.player.inventory.unequip("Cloak")
                            self.player.update_appearance()
                    case pg.K_m:
                        box = MessageBox(
                            [
                                "Congrats, you hit 'M'! This is a super duper long message just to test the capabilities of the message box state. it should wrap the text in a message box and also close when you hit space. It should now also create slides for a super long message like this one. Like you'll probaby have to hit space to have seen this.",
                                "Surprise! 2 Messages work (:"
                            ]
                        )
                        return ["CHANGE_STATE", "message_box", box]
                    ################# END TEST ############
            if event.type == pg.KEYUP:
                match event.key:
                    case pg.K_UP | pg.K_w:
                        self.player.set_animation("idle_up")
                    case pg.K_DOWN | pg.K_s:
                        self.player.set_animation("idle_down")
                    case pg.K_LEFT | pg.K_a:
                        self.player.set_animation("idle_left")
                    case pg.K_RIGHT | pg.K_d:
                        self.player.set_animation("idle_right")

    def handle_continuous_player_movement(self):
        """Handle continuous player movement based on currently pressed keys."""
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.player.set_animation("walk_up")
            self.player.change_destination(0, -TILESIZE, self.map.obstacles)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.player.set_animation("walk_down")
            self.player.change_destination(0, TILESIZE, self.map.obstacles)
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.set_animation("walk_left")
            self.player.change_destination(-TILESIZE, 0, self.map.obstacles)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.set_animation("walk_right")
            self.player.change_destination(TILESIZE, 0, self.map.obstacles)

    def update(self):
        """Update logic for the gameplay state."""
        for sprite in self.sprite_groups["characters"]:
            sprite.update()
        self.map.update()
        self.camera.update(self.player.hitbox)

    def draw(self, screen):
        """Draw the gameplay on the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        screen.fill(MYSTIC_BLUE)
        self.map.draw(screen, self.camera)
        self.draw_grid(screen)
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
            "all_sprites" : [],
            "characters" : [],
            "player" : [],
            "npcs" : []
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
        self.init_sprite_groups()
        self.sprite_groups["all_sprites"].append(self.player)
        self.sprite_groups["characters"].append(self.player)
        self.sprite_groups["npcs"].append(self.player)
        self.map = TiledMap(map_name)
        with open(DATA_DIR / "npc_data.json", encoding="utf-8") as f:
            npc_data = json.load(f)
        npc_data = npc_data["npcs"]
        for npc_id in npc_data:
            if npc_data[npc_id]["location"]["map"] == map_name:
                npc = NPC(npc_id)
                self.map.obstacles.append(npc)
                self.sprite_groups["all_sprites"].append(npc)
                self.sprite_groups["characters"].append(npc)
                self.sprite_groups["npcs"].append(npc)
        bunny = Animal("jackalope")
        self.map.obstacles.append(bunny)
        self.sprite_groups["all_sprites"].append(bunny)
        self.sprite_groups["characters"].append(bunny)
        self.sprite_groups["npcs"].append(bunny)
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
                        PlayerCharacter(data)
                    )
                else:
                    self.load_player(
                        PlayerCharacter(data)
                    )
            case "saved_game": self.load_game(data)
            case _: print("Data load case not recognized.")

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
        player = PlayerCharacter(data = save_dict["player_data"])
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
