from config.game_settings import FPS

class Scene:
    def __init__(self, obj, method, params, condition_func, pre_delay = 0, post_delay = 0) -> None:
        self.pre_delay = pre_delay
        self.obj = obj
        self.method = method
        self.params = params
        self.condition_func = condition_func
        self.post_delay = post_delay
        self.method_called = False

    def update(self):
        if self.pre_delay > 0:
            self.pre_delay -= 1 / FPS
        elif not self.method_called:
            getattr(self.obj, self.method)(*self.params)
            self.method_called = True
        elif not getattr(self.obj, self.condition_func)():
            pass # If condition not yet met, pass
        else: self.post_delay -= 1 / FPS

    def is_finished(self):
        return self.post_delay < 0

class Sequencer:
    """A collection of scenes to be played."""
    def __init__(self, scenes: list[Scene]) -> None:
        self.scenes = scenes

    def update(self):
        for scene in self.scenes:
            if not scene.is_finished():
                scene.update()
                break

    def insert_seq(self, idx: int, scene: Scene):
        self.scenes.insert(idx, scene)

    def is_finished(self):
        return all([scene.is_finished() for scene in self.scenes])