"""
Base Game State Module

This module defines the base `State` class. Each derived state should 
inherit from this base class and implement its own logic for handling events,
updating the state, and drawing game content.

This module also provides a consistent interface for all game states.
"""

class State:
    """The `State` class is a foundational class for implementing specific
    game states. Game states handle different aspects of the game, such as
    the main menu, gameplay, character creation, etc.
    """
    def __init__(self) -> None:
        """Initialize a game state."""
        pass  # pylint: disable=unnecessary-pass

    def handle_events(self, events):
        """Handle events for the game state."""
        pass  # pylint: disable=unnecessary-pass

    def update(self):
        """Update the game state."""
        pass  # pylint: disable=unnecessary-pass

    def draw(self, screen):
        """Draw the game state."""
        pass  # pylint: disable=unnecessary-pass
