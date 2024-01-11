"""
CharacterCreationState Module

This module defines the `CharacterCreationState` class, which represents the game state
where the player is choosing character attributes.
"""

import pygame as pg
from states.state_base import State
from entities.player_character import PlayerCharacter
from items.wand import Wand, WandCore, WandLength, WandWood
from entities.inventory import CharacterInventory
from items.cloak import Cloak
from config.colors import WHITE, LIGHTGREY, MYSTIC_RED
from config.directories import SPRITES_DIR

class CharacterCreationState(State):
    """
    CharacterCreationState Class

    This class represents the game state where the player is choosing character attributes.
    It manages character attribute selection, character creation, and game initiation.
    """
    def __init__(self):
        """Initialize the Character Creation State."""
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
        self.attr_idx = [0 for key in self.options]

    def handle_events(self, events):
        """
        Handle events in the character creation state.

        Args:
            events (list): A list of pygame events to process.
        
        Returns:
            list: A list indicating the action to take in response to the events in the format
                  [EVENT_NAME, data, tags]
        """
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
                        #self.attr_idx[self.current_attr] -= 1
                        n_choices = len(self.options[list(self.options.keys())[self.current_attr]])
                        self.attr_idx[self.current_attr] = (
                            (self.attr_idx[self.current_attr] - 1) % n_choices
                            )
                    case pg.K_RIGHT:
                        n_choices = len(self.options[list(self.options.keys())[self.current_attr]])
                        self.attr_idx[self.current_attr] = (
                            (self.attr_idx[self.current_attr] + 1) % n_choices
                            )
                    # Start new game!
                    case pg.K_RETURN:
                        selection = list(self.options.keys())[self.current_attr]
                        if selection == "Start Game":
                            return ["LOAD_DATA", self.make_player(), "NEW_GAME"]
                        if selection == "Back":
                            return ["CHANGE_STATE", "main_menu"]
            return None

    def draw(self, screen):
        """Draw the Character Creation menu on the screen.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
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
            else: text = f"{attribute}: {self.options[attribute][self.attr_idx[i]]}"
            text = self.font.render(text, True, text_color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 50))
            screen.blit(text, text_rect)

    def make_player(self) -> PlayerCharacter:
        """
        Create a new player entity based on the selected character attributes.

        Returns:
            dict: a dict of kwargs used to initialize a PlayerCharacter.
        """
        # Get selected options
        species = "human"
        wand = Wand(
                wood = WandWood(self.options["Wand Wood"][self.attr_idx[1]]),
                core = WandCore(self.options["Wand Core"][self.attr_idx[2]]),
                length = WandLength(self.options["Wand Length (inches)"][self.attr_idx[3]])
            )
        cloak = Cloak(species=species, style="school_cloak")
        # Add options to inventory
        inventory = CharacterInventory()
        inventory.equip(cloak)
        inventory.add_item(wand)
        data = {
            "case" : "player",  # Tells state manager passing player data
            "name" : self.options["Name"][self.attr_idx[0]],
            "race": species,
            "sprite" : "base",
            "location" : {
                "map": "-",
                "position" : {
                    "x" : 32,
                    "y" : 32
                }
            },
            "inventory": inventory.save()
        }
        return data
