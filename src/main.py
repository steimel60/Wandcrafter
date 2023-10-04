import pygame as pg
from config.game_settings import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from config.colors import GREEN
from states.state_manager import StateManager
from utils.data_manager import DataManager

class GameManager:
    def __init__(self) -> None:
        # PYGAME INIT
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.font = font = pg.font.Font(None, 36) # FOR FPS DISPLAY ONLY
        self.draw_fps = True # FOR FPS DISPLAY ONLY
        pg.key.set_repeat(250,100) # Call multiple KEYDOWN events when held (maybe move to state func)
        # GAME INIT
        self.state_manager = StateManager()
        self.game_data = DataManager()

    def run(self):
        running = True
        while running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        response = self.state_manager.handle_events(pg.event.get())
        match response:
            case ["NEW_GAME", player_data]:
                self.game_data.create_new_game(player_data)
                self.state_manager.set_game_data(self.game_data)
                self.state_manager.change_state("gameplay")
            case ["LOAD_GAME"]:
                self.game_data.load_game()
                self.state_manager.set_game_data(self.game_data)
                self.state_manager.change_state("gameplay")

    def update(self):
        pass

    def draw(self):
        self.state_manager.draw(self.screen)
        if self.draw_fps:
            text = f"FPS: {round(self.clock.get_fps(),0)}"
            text = self.font.render(text, True, GREEN)
            self.screen.blit(text, (10,10))
        pg.display.flip()

if __name__ == "__main__":
    game = GameManager()
    while True:
        game.run()
