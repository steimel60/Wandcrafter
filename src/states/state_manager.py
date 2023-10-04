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
            case ["CHANGE_STATE", new_state]: self.change_state(new_state)
            case ["NEW_GAME", player]: return ["NEW_GAME", player]
            case ["LOAD_GAME"]: return ["LOAD_GAME"]

    def draw(self, screen):
        self.state_dict[self.current_state].draw(screen)
    
    def change_state(self, new_state):
        """Change the current game state."""
        if new_state in self.state_dict:
            self.current_state = new_state
        else:
            print(f"Error: State '{new_state}' not found.")

    def set_game_data(self, game_data):
        self.state_dict["gameplay"].set_game_data(game_data)