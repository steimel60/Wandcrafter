"""
MainMenuState Module

This module defines the `MainMenuState` class, which represents the main menu
state design and logic.
"""

import pygame as pg
from states.states import State
from config.colors import MYSTIC_PURPLE, WHITE, LIGHTGREY
from config.game_settings import GAME_TITLE
from utils.save_system import select_saved_game

class MainMenuState(State):
    """
    MainMenuState Class

    Represents the main menu state of the game, allowing the player to choose
    between starting a new game or loading an existing one. It handles user
    input for selecting menu options and triggers corresponding actions.
    """
    def __init__(self, manager):
        """Initialize the main menu state.

        Initializes the main menu state, setting the default selected option
        to "New Game" and defining available menu options.

        Attributes:
            selected_option (int): Index of the currently selected menu option.
            options (list): A list of available menu options.
            font (pygame.font.Font): The font used for rendering text.
        """
        super().__init__(manager)
        self.selected_option = 0
        self.options = ["New Game", "Load Game"]
        self.font = pg.font.Font(None, 36)

    def handle_events(self, events):
        """Handle events in the main menu state.

        Processes keyboard events to navigate and select options in the main menu.

        Args:
            events (list): A list of pygame events to process.

        Returns:
            list or None: A list containing response data if an action occurs,
            or None if no action is taken.
        """
        response = None
        for event in events:
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    case pg.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    case pg.K_RETURN:
                        # Handle the selected option
                        if self.selected_option == 0:
                            self.manager.change_state("character_creation")
                        elif self.selected_option == 1:
                            response = self.load_existing_game()
        return response

    def draw(self, screen):
        """Draw the main menu on the screen.

        Renders the main menu interface, including the game title and menu options.

        Args:
            screen (pygame.Surface): The pygame surface to draw on.
        """
        # Draw the main menu on the screen
        screen.fill(MYSTIC_PURPLE)
        # Add Title
        text_color = WHITE
        text = self.font.render(GAME_TITLE, True, text_color)
        text_rect = text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(text, text_rect)
        # Add Options
        for i, option in enumerate(self.options):
            text_color = WHITE if i == self.selected_option else LIGHTGREY
            text = self.font.render(option, True, text_color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 50))
            screen.blit(text, text_rect)

    def load_existing_game(self):
        """Load an existing game from a save file.

        Opens the file dialog to select a saved game file and attempts to load the game.

        Returns:
            list or None: A list containing response data if a game is loaded,
            or None if no game is loaded.
        """
        game = select_saved_game()
        if game is not None:
            return ["LOAD_DATA", game]
        return None
