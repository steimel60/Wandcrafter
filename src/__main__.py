"""
This module defines the GameManager class, which serves as the main controller
for the game. It initializes the game window, manages states, and handles game loops.
"""

import pygame as pg
from config.game_settings import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from config.colors import GREEN
from states.state_manager import StateManager

class GameManager:
    """
    GameManager class serves as the main controller for the game.

    Attributes:
        screen (Surface): The Pygame display surface for rendering.
        clock (Clock): The Pygame clock for controlling frame rate.
        font (Font): The Pygame font for displaying current FPS.
        draw_fps (bool): Flag to control whether to display FPS.
        state_manager (StateManager): Manages logic for different game states.
    """
    def __init__(self) -> None:
        # PYGAME INIT
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36) # FOR FPS DISPLAY ONLY
        self.draw_fps = True # FOR FPS DISPLAY ONLY
        pg.key.set_repeat(250,100) # Call multiple KEYDOWN events when held
        # GAME INIT
        self.state_manager = StateManager(self)

    def run(self):
        """Run the main game loop."""
        running = True
        while running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        """Pass input to the State Manager."""
        return self.state_manager.handle_events(pg.event.get())

    def update(self):
        """Update current state based on inputs."""
        self.state_manager.update()

    def draw(self):
        """Draw game to screen."""
        self.state_manager.draw(self.screen)
        if self.draw_fps:
            text = f"FPS: {round(self.clock.get_fps(),0)}"
            text = self.font.render(text, True, GREEN)
            self.screen.blit(text, (10,10))
        pg.display.flip()

if __name__ == "__main__":
    game = GameManager()
    game.run()
