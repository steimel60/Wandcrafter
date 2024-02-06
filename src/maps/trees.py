from maps.obstacles import Obstacle, AnimatedObstacle
from items.item import action, quick_action

class Tree(Obstacle):
    def __init__(self, rect):
        super().__init__(rect)

class MagicTree(AnimatedObstacle):
    def __init__(self, frames, rect):
        super().__init__(frames, rect)
