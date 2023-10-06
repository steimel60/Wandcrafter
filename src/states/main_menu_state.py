import pygame as pg
from .state_base import State
from config.colors import *
from config.game_settings import GAME_TITLE
from utils.save_system import load_game

class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.selected_option = 0
        self.options = ["New Game", "Load Game"]
        self.font = pg.font.Font(None, 36)

    def handle_events(self, events):
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
                            return ["CHANGE_STATE", "character_creation"]
                        elif self.selected_option == 1:
                            return self.load_existing_game()

    def draw(self, screen):
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
        game = load_game()
        if game is not None:
            return ["LOAD_DATA", game]