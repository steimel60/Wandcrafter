import sys
import pygame as pg
from .main_menu_state import MainMenuState
from .gameplay_state import GameplayState
from .character_creation_state import CharacterCreationState

class StateManager:
    """Manages which state the game is currently in and all functions
    regarding game state. """
    def __init__(self) -> None:
    
        self.state_dict = {
            'gameplay' : GameplayState(),
            'main_menu' : MainMenuState(),
            'character_creation' : CharacterCreationState(),
        }
        self.current_state = 'main_menu'
    
    def handle_events(self, events):
        if any([event.type == pg.QUIT for event in events]):
            pg.quit()
            sys.exit()
        response = self.state_dict[self.current_state].update(events)
        match response:
            case ["CHANGE_STATE", new_state, *tags]: self.change_state(new_state, tags)
            case ["LOAD_DATA", data, *tags]: self.load_data(data, tags)
            case _: pass

    def draw(self, screen):
        self.state_dict[self.current_state].draw(screen)

    def new_game(self, player):
        self.state_dict["gameplay"].new_game(player)
        self.change_state("gameplay")

    def load_data(self, data, tags = None):
        self.state_dict["gameplay"].load_data(data, tags)
        self.change_state("gameplay")

    def change_state(self, new_state, tags = None):
        """Change the current game state."""
        if new_state in self.state_dict:
            self.current_state = new_state
        else:
            print(f"Error: State '{new_state}' not found.")