from config.game_settings import FPS

class ExecutableMethod:
    def __init__(self, obj, method, params = None) -> None:
        self.obj = obj
        self.method = method
        self.params = params
        self.called = False

    def call_method(self):
        if self.params is not None:
            self.called = True
            return getattr(self.obj, self.method)(*self.params)
        self.called = True
        return getattr(self.obj, self.method)()

    def has_been_called(self):
        return self.called

class SceneAction:
    def __init__(
            self,
            action_method: ExecutableMethod,
            condition_method: ExecutableMethod = None,
            final_method: ExecutableMethod = None
            ) -> None:
        self.action = action_method
        self.condition = condition_method
        self.final_method = final_method
        self.action_complete = False

    def update(self):
        if not self.action.has_been_called():
            self.action.call_method()
        elif self.condition is not None:
            if self.condition.call_method():
                self.action_complete = True
        else: # If method_called and no condition func
            self.action_complete = True

    def is_completed(self):
        return self.action_complete

    def call_final_method(self):
        if self.final_method is not None:
            self.final_method.call_method()

class Scene:
    def __init__(self, name: str, actions: list[SceneAction], pre_delay=0, post_delay=0) -> None:
        self.name = name
        self.pre_delay = pre_delay
        self.actions = actions
        self.post_delay = post_delay
        self.final_methods_called = False

    def update(self):
        if self.is_in_pre_delay():
            self.decrement_pre_delay()
        elif self.are_all_actions_complete():
            if not self.final_methods_called:
                self.call_final_methods()
                self.final_methods_called = True
            self.decrement_post_delay()
        else:
            self.update_actions()

    def insert_scene_action(self, idx, action):
        self.actions.insert(idx, action)

    def is_in_pre_delay(self) -> bool:
        return self.pre_delay > 0

    def decrement_pre_delay(self):
        self.pre_delay -= 1 / FPS

    def are_all_actions_complete(self) -> bool:
        return all(action.is_completed() for action in self.actions)

    def decrement_post_delay(self):
        self.post_delay -= 1 / FPS

    def update_actions(self):
        for action in self.actions:
            if not action.is_completed():
                action.update()

    def call_final_methods(self):
        for action in self.actions:
            action.call_final_method()

    def is_finished(self):
        return self.final_methods_called and self.post_delay <= 0


class Sequencer:
    """A collection of scenes to be played."""
    def __init__(self, scenes: list[Scene]) -> None:
        self.scenes = scenes

    def update(self):
        for scene in self.scenes:
            if not scene.is_finished():
                scene.update()
                break

    def insert_scene(self, idx: int, scene: Scene):
        self.scenes.insert(idx, scene)

    def get_scene_by_name(self, name) -> Scene:
        matches = [s for s in self.scenes if s.name == name]
        if len(matches) > 0:
            return matches[0]
        return None

    def insert_scene_action(self, scene_name, idx, action):
        self.get_scene_by_name(scene_name).insert_scene_action(idx, action)

    def append_seq(self, next_sequencer):
        self.scenes += next_sequencer.scenes

    def is_finished(self) -> bool:
        return all(scene.is_finished() for scene in self.scenes)
