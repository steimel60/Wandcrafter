"""
Item Module

This module defines the `Item` class, which serves as the base class for items in the game.
Items are objects or artifacts that characters can acquire and use throughout the game.
"""

# pylint: disable=R0903
# disables "too few public methods" warning

class Item:
    """Base class for items in game."""
    def __init__(self) -> None:
        pass

    def serialize(self, item):
        data = {}
        for key in (d := vars(item)):
            if hasattr(d[key], "__dict__"):
                data[key] = self.serialize(item)
            else: data[key] = d[key]
        return data

    def save(self) -> dict:
        data = {}
        data["type"] = type(self).__name__
        for key in (d := vars(self)):
            value = d[key]
            if hasattr(value, "__dict__"):
                value = self.serialize(value)
            data[key] = value
        return data

    @classmethod
    def from_json(cls, _data):
        raise NotImplementedError(
            f'"from_json" method not implemented for Class "{cls.__name__}". Item subclasses must implement this method.'
        )
