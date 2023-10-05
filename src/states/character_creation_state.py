import pygame as pg
from .state_base import State
from .gameplay_state import GameplayState
from entities.player_entity import PlayerEntitiy
from items.wand import Wand, WandCore, WandLength, WandWood
from config.colors import *
from pathlib import Path
from config.directories import USER_GAME_DIR
from utils.save_system import save_game_data, load_game_data

class CharacterCreationState(State):
    def __init__(self):
        super().__init__()
        self.font = pg.font.Font(None, 36)
        self.options = {
            'Name' : ['Dylan', 'Cody', 'Bob'],
            'Wand Wood' : ['Oak', 'Pine', 'Larch'],
            'Wand Core' : ['Dragon Heartstring', 'Pheonix Feather', 'Unicorn Hair'],
            'Wand Length (inches)' : [9, 11, 13],
            'Start Game' : [None],
            'Back' : [None]
        }
        self.current_attr = 0
        self.attribute_idx = [0 for key in self.options]

    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    # Select Current Attribute
                    case pg.K_UP:
                        self.current_attr = (self.current_attr - 1) % len(self.options)
                    case pg.K_DOWN:
                        self.current_attr = (self.current_attr + 1) % len(self.options)
                    # Select Attribute Choice
                    case pg.K_LEFT:
                        self.attribute_idx[self.current_attr] -= 1
                        self.attribute_idx[self.current_attr] = self.attribute_idx[self.current_attr] % len(self.options[list(self.options.keys())[self.current_attr]])
                    case pg.K_RIGHT:
                        self.attribute_idx[self.current_attr] = (self.attribute_idx[self.current_attr] + 1) % len(self.options[list(self.options.keys())[self.current_attr]])
                    # Start new game!
                    case pg.K_RETURN:
                        selection = list(self.options.keys())[self.current_attr]
                        if selection == "Start Game":
                            return ["LOAD_DATA", self.make_player(), "NEW_GAME"]
                        elif selection == "Back":
                            return ["CHANGE_STATE", "main_menu"]

    def draw(self, screen):
        # Draw the gameplay on the screen
        screen.fill(MYSTIC_RED)
        # Add Title
        text_color = WHITE
        text = self.font.render("Character Creation Screen", True, text_color)
        text_rect = text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(text, text_rect)
        # Add Options
        for i, attribute in enumerate(self.options):
            text_color = WHITE if i == self.current_attr else LIGHTGREY
            if attribute in ["Back", "Start Game"]: text = attribute
            else: text = f"{attribute}: {self.options[attribute][self.attribute_idx[i]]}"
            text = self.font.render(text, True, text_color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 50))
            screen.blit(text, text_rect)

    def make_player(self) -> PlayerEntitiy:
        player = PlayerEntitiy(
            name = self.options["Name"][self.attribute_idx[0]],
            wand = Wand(
                wood = WandWood(self.options["Wand Wood"][self.attribute_idx[1]]),
                core = WandCore(self.options["Wand Core"][self.attribute_idx[2]]),
                length = WandLength(self.options["Wand Length (inches)"][self.attribute_idx[3]])
            )
        )
        return player