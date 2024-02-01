from states.states import State, SubState
from states.sequencer import Sequencer

class SequencerSubState(SubState):
    """Used when transitioning between maps and such in the gameplay state.
    
    This state essentially runs all parts of the GameplayState but doesn't allow
    user input while sequences are playing.
    """

    def __init__(self, parent: State, sequencer: Sequencer) -> None:
        super().__init__(parent)
        self.sequencer = sequencer

    def handle_events(self, _events):
        return None

    def update(self):
        self.sequencer.update()
        super().update()

    def draw(self, screen):
        super().draw(screen)

    def run(self):
        while not self.sequencer.is_finished():
            super().run()
