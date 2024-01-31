"""
Base Game State Module

This module defines the base `State` class. Each derived state should 
inherit from this base class and implement its own logic for handling events,
updating the state, and drawing game content.

This module also provides a consistent interface for all game states.
"""
import pygame as pg
from config.game_settings import FPS

class State:
    """The `State` class is a foundational class for implementing specific
    game states. Game states handle different aspects of the game, such as
    the main menu, gameplay, character creation, etc.
    """
    def __init__(self, manager) -> None:
        """Initialize a game state."""
        self.manager = manager

    def handle_events(self, events):
        """Handle events for the game state."""
        pass  # pylint: disable=unnecessary-pass

    def update(self):
        """Update the game state."""
        pass  # pylint: disable=unnecessary-pass

    def draw(self, screen):
        """Draw the game state."""
        pass  # pylint: disable=unnecessary-pass

class SubState:
    """The `SubState` class is used to run a loop with minimal logic inside of a larger State.
    """
    def __init__(self, parent: State) -> None:
        self.parent = parent

    def handle_events(self, _events):
        """Handle events for the game state."""
        raise NotImplementedError(
            f"`handle_events` method not implemented by the class {self.__class__.__name__}. "
            "The `handle_events` method should be defined by all subclasses of `SubState`."
            )

    def update(self):
        """Update the game state."""
        raise NotImplementedError(
            f"`update` method not implemented by the class {self.__class__.__name__}. "
            "The `update` method should be defined by all subclasses of `SubState`."
            )

    def draw(self, _screen):
        """Draw the game state."""
        raise NotImplementedError(
            f"`draw` method not implemented by the class {self.__class__.__name__}. "
            "The `draw` method should be defined by all subclasses of `SubState`."
            )

    def run(self):
        """Main SubState loop.

        All `SubState` subclasses should contain the logic to start and stop this loop.
        """
        self.handle_events(pg.event.get())
        self.update()
        self.draw(self.parent.manager.gm.screen)
        self.parent.manager.gm.clock.tick(FPS)
