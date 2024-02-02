"""
StateManager Module

This module defines the `StateManager` class, which is responsible for managing
the current game state and handling various functions related to game state 
management. Namely, calling 'running' loop functions for the current state and
passing data during state transitions.
"""

import sys
import pygame as pg
from states.state_main_menu import MainMenuState
from states.state_gameplay import GameplayState
from states.state_character_creation import CharacterCreationState

class StateManager:
    """Manages the game's state transitions and state-specific functions.

    This class is responsible for managing the current game state and handling
    functions associated with game state, including event handling, updates,
    and rendering.

    Attributes:
        state_dict (dict): A dictionary of game states mapped to their names.
        current_state (str): The name of the current game state.
    """
    def __init__(self, game_manager) -> None:
        """Initialize the StateManager with initial game states."""
        self.state_dict = {
            'gameplay' : GameplayState(self),
            'main_menu' : MainMenuState(self),
            'character_creation' : CharacterCreationState(self),
        }
        self.gm = game_manager
        self.current_state = 'main_menu'

    def handle_events(self, events):
        """Handle events and update the game state.

        Args:
            events (list): A list of pygame events to be processed.
        """
        if pg.QUIT in (event.type for event in events):
            pg.quit()
            sys.exit()
        self.state_dict[self.current_state].handle_events(events)

    def update(self):
        """Update the current game state."""
        self.state_dict[self.current_state].update()

    def draw(self, screen):
        """Render the current game state on the screen.

        Args:
            screen (pygame.Surface): The game screen to render on.
        """
        self.state_dict[self.current_state].draw(screen)

    def load_game(self, game):
        """Load and transition to a new game state using the provided data.

        Args:
            game: The game data to load.
        """
        self.state_dict["gameplay"].load_game(game)
        self.change_state("gameplay")
    
    def new_game(self, data):
        self.state_dict["gameplay"].new_game(data)
        self.change_state("gameplay")

    def change_state(self, new_state, _tags = None):
        """Change the current game state.

        Args:
            new_state (str): The name of the state to transition to.
            tags (list, optional): Additional tags or labels associated with the state transition.
        """
        if new_state in self.state_dict:
            self.current_state = new_state
        else:
            print(f"Error: State '{new_state}' not found.")
