from states.state_base import State

class SequencerState(State):
    """Used when transitioning between maps and such in the gameplay state.
    
    This state essentially runs all parts of the GameplayState but doesn't allow
    user input while sequences are playing.
    """

    def __init__(self, sequencer, gameplay_state) -> None:
        super().__init__()
        self.sequencer = sequencer
        self.gameplay_state = gameplay_state

    def handle_events(self, _events):
        if self.sequencer.is_finished():
            return ["CHANGE_STATE", "gameplay"]

    def update(self):
        self.sequencer.update()
        self.gameplay_state.update()

    def draw(self, screen):
        self.gameplay_state.draw(screen)
