from entities.obstacles import Obstacle

class Tree(Obstacle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

class MagicTree(Tree):
    def __init__(self, images, x, y, w, h):
        super().__init__(x, y, w, h)
        self.frame = 0
        self.images = images

    def update(self):
        self.frame += 1
        if self.frame >= len(self.images): self.frame = 0

    def draw(self, screen, camera):
        screen.blit(
            self.images[self.frame],
            camera.apply_rect(self.rect)
        )
