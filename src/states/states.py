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
    """
    A class for creating sub-states within a main game state.

    Sub-states are designed to run a simplified loop of logic that operates concurrently
    with the main state's update and draw loops. This class allows for sub-state operations
    to be executed within a method or function, ensuring that the main state remains active
    until the sub-state's logic concludes.

    Attributes:
        parent (State): The main state that this sub-state is associated with.

    Methods:
        handle_events(_events): Abstract method to handle game events.
        update(): Calls the update method of the parent state.
        draw(screen): Calls the draw method of the parent state.
        run(): Runs the main loop for the sub-state.
    """
    def __init__(self, parent: State) -> None:
        """
        Initializes a new instance of the SubState class.

        Args:
            parent (State): The main state that this sub-state is part of.
        """
        self.parent = parent

    def handle_events(self, _events):
        """
        Handles events passed to the sub-state. This method must be implemented by subclasses.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError(
            f"`handle_events` method not implemented by the class {self.__class__.__name__}. "
            "The `handle_events` method should be defined by all subclasses of `SubState`."
            )

    def update(self):
        """
        Updates the state of the parent state. This method should be overridden by subclasses
        to provide specific update logic.
        """
        self.parent.update()

    def draw(self, screen):
        """
        Draws the parent state onto the given screen. This method should be overridden by subclasses
        to provide specific drawing logic.

        Args:
            screen: The screen surface to draw the parent state on.
        """
        self.parent.draw(screen)

    def run(self):
        """
        Runs the main loop of the sub-state.

        This includes event handling, updating, and drawing the state. The loop should be controlled
        to start and stop at appropriate times by the subclass logic.
        """
        self.handle_events(pg.event.get())
        self.update()
        self.draw(self.parent.manager.gm.screen)
        pg.display.flip()
        self.parent.manager.gm.clock.tick(FPS)
