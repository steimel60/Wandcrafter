"""
GameplayState Module

This module defines the `GameplayState` class, which represents the game state
where the player is actively playing the game.
"""

import json
from pathlib import Path
import pygame as pg
from states.states import State
from config.colors import MYSTIC_BLUE, BLACK
from config.game_settings import TILESIZE
from config.directories import USER_GAME_DIR, DATA_DIR
from utils.save_system import save_game_data
from entities.player_character import PlayerCharacter
from entities.npc import NPC
from maps.map import TiledMap
from maps.camera import Camera
from sfx.fader import Fader, get_fade_action
from maps.portals import Portal, Door
from states.sequencer import Scene, Sequencer, ExecutableMethod, SceneAction
from states.sub_message import MessageBoxSubState
from states.sub_sequencer import SequencerSubState

### TEST ONLLY ###
from gui.message_box import MessageBox
from entities.animals import Animal

class GameplayState(State):
    """
    GameplayState Class

    This class represents the game state where the player is actively playing
    the game. It manages game events, updates, and rendering of the game world.
    """
    def __init__(self, manager, path = None, player = None, tile_map = None):
        """Initialize the Gameplay State.
            
        Args:
            path (Path, optional): The file path for saving/loading the game. Defaults to None.
            player (PlayerCharacter, optional): The player entity. Defaults to None.
            tile_map (TiledMap, optional): The tile map. Defaults to None.
        """
        super().__init__(manager)
        self.file_path = path
        self.player = player
        self.map = tile_map
        self.camera = Camera()
        self.save_data = {}
        self.sprite_groups = self.init_sprite_groups()
        self.quest_data = None
        self.sequences = []

    def handle_events(self, events):
        """Handle events in the gameplay state.

        Args:
            events (list): A list of pygame events to process.
        """
        self.handle_global_events(events)
        response = self.handle_player_events(events)
        if response:
            return response
        response = self.handle_continuous_player_movement()
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
                        if self.player.is_idle():
                            items = self.map.items["obstacles"] + self.map.items["portals"]
                            return self.player.interact(items, self)
                    ########## TEST EVENTS #############
                    case pg.K_i:
                        if "idle" in self.player.appearance.current_anim:
                            self.player.inventory.equip(self.player.inventory.bag[-1])
                            self.player.update_appearance()
                    case pg.K_u:
                        if "idle" in self.player.appearance.current_anim:
                            self.player.inventory.unequip("Cloak")
                            self.player.update_appearance()
                    case pg.K_m:
                        box = MessageBox(
                            [
                                ("Congrats, you hit 'M'! "
                                 "This is a super duper long message just to test the capabilities of the message box state. "
                                 "It should wrap the text in a message box and also close when you hit space. "
                                 "It should now also create slides for a super long message like this one. "
                                 "Like you'll probaby have to hit space to have seen this."),
                                "Surprise! 2 Messages work (:"
                            ]
                        )
                        MessageBoxSubState(self, box).run()
                    ################# END TEST ############

    def handle_continuous_player_movement(self):
        """Handle continuous player movement based on currently pressed keys."""
        response =  None
        obstacles = self.map.items["obstacles"] + self.map.items["portals"]
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.player.set_animation("walk_up")
            response = self.player.change_destination(0, -TILESIZE, obstacles)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.player.set_animation("walk_down")
            response = self.player.change_destination(0, TILESIZE, obstacles)
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.set_animation("walk_left")
            response = self.player.change_destination(-TILESIZE, 0, obstacles)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.set_animation("walk_right")
            response = self.player.change_destination(TILESIZE, 0, obstacles)
        if response:
            return self.handle_player_collision_events(response)
        return None

    def handle_player_collision_events(self, collision_object):
        if isinstance(collision_object, Portal):
            return self.use_portal(portal=collision_object)

    def update(self):
            """Update logic for the gameplay state."""
            for sprite in self.sprite_groups["all_sprites"]:
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

    def use_portal(self, portal):
        # Play "Entering" Scenes
        SequencerSubState(self, portal.get_enter_seq(self)).run()
        # Change map and set player at corresponding portal
        self.open_map(portal.name)
        spawn_portal = self.get_portal_by_pid(portal.to_pid)
        self.player.set_position(spawn_portal.rect.x, spawn_portal.rect.y)
        # Play "Exit" scene
        SequencerSubState(self, spawn_portal.get_exit_seq(self)).run()

    def get_portal_by_pid(self, pid, tile_map = None):
        if tile_map is None:
            tile_map = self.map
        for portal in tile_map.items['portals']:
            if portal.pid == pid:
                return portal
        return None

    def add_sprite(self, sprite, groups):
        for group in groups:
            self.sprite_groups[group].append(sprite)

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
        # Clear sprites
        self.sprite_groups = self.init_sprite_groups()
        # Load player
        self.add_sprite(self.player, ["all_sprites", "characters"])
        # Load map
        self.map = TiledMap(map_name)
        # Resize camera
        self.camera.open_map(self.map)
        # Load NPCs
        with open(DATA_DIR / "npc_data.json", encoding="utf-8") as f:
            npc_data = json.load(f)
        npc_data = npc_data["npcs"]
        for npc_id in npc_data:
            if npc_data[npc_id]["location"]["map"] == map_name:
                npc = NPC(npc_id)
                self.map.items["obstacles"].append(npc)
                self.add_sprite(npc, ["all_sprites", "characters", "npcs"])
        # bunny test, remove later
        bunny = Animal("jackalope")
        self.map.items["obstacles"].append(bunny)
        self.add_sprite(bunny, ["all_sprites", "characters", "npcs"])

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
            "player_data" : self.player.get_save_data(),
            "map" : self.map.name,
            "file_path" : self.file_path
        }
        save_game_data(self.file_path, save_data)
