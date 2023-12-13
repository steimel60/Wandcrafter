import pygame as pg
from gui.widget import Widget
from config.colors import DARKGREY
from config.directories import GUI_DIR
from config.game_settings import TILESIZE

class MessageBox(Widget):
    def __init__(self, messages, color: str = "beigeLight", alignment = "bottom_center"):
        image = pg.image.load(GUI_DIR / f"panel_{color}.png")
        image = self.resize(image)
        super().__init__(image, alignment=alignment)
        self.font = pg.font.Font(None, 36)  # Choose your font and size
        if not isinstance(messages, list):
            messages = [messages]
        self.messages = messages
        self.text_surfaces = [self.render_text(m) for m in messages]
        self.message_idx = 0
        self.tab_idx = 0
        

    def draw(self, screen: pg.Surface):
        super().draw(screen)
        pos_x, pos_y = self.get_draw_position()
        # Render and draw the text
        text_surface = self.text_surfaces[self.message_idx][self.tab_idx]
        screen.blit(text_surface, (pos_x + self.padding, pos_y + self.padding))

    def render_text(self, message):
        w = self.image.get_width() - self.padding * 2
        h = self.image.get_height() - self.padding * 2
        surfaces = [] # Store all slides for current message
        current_line = 0 # Row to render text to
        current_x = 0 # Current start position
        line_size = self.font.size("Tg")[1] # Max possible height
        words = message.split(" ")
        done_rendering = False
        while not done_rendering:
            text_surface = pg.Surface((w, h), pg.SRCALPHA)
            text_surface.fill((0, 0, 0, 0))
            word_counter = 0
            for word in words:
                word_counter += 1
                text = self.font.render(f'{word} ', True, DARKGREY)
                word_size = self.font.size(f'{word} ')
                if word_size[0] + current_x > w:
                    current_x = 0
                    current_line += 1
                if current_line*line_size + word_size[1] > h:
                    current_x = 0
                    current_line = 0
                    break
                text_surface.blit(text, (current_x,current_line*line_size))
                current_x += word_size[0]
            surfaces.append(text_surface)
            if word_counter == len(words):
                done_rendering = True
            else:
                words = words[word_counter:]
        return surfaces

    def resize(self, image):
        x, y = self.get_screen_size_in_tiles()
        x = max(1, round((2 * x) / 3))
        y = max(1, round((y / 4)))
        return pg.transform.scale(image, (TILESIZE * x, TILESIZE * y))
    
    def next_tab(self):
        if self.next_tab_exists():
            self.tab_idx += 1

    def next_tab_exists(self):
        return self.tab_idx < len(self.text_surfaces[self.message_idx]) - 1

    def next_message(self):
        if self.next_message_exists():
            self.message_idx += 1
            self.tab_idx = 0

    def next_message_exists(self):
        return self.message_idx < len(self.messages) - 1

    def update(self):
        pass
