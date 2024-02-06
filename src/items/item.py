"""
Item Module

This module defines the `Item` class, which serves as the base class for items in the game.
Items are objects or artifacts that characters can acquire and use throughout the game.
"""

def action(func):
    """Decorator to mark methods as an action and register them."""
    if not hasattr(func, '__action__'):
        func.__action__ = []  # Initialize once
    func.__action__.append(func.__name__)
    return func

def quick_action(func):
    """Decorator to mark methods as quick actions and register them."""
    action(func)
    if not hasattr(func, '__quick_action__'):
        func.__quick_action__ = []  # Initialize once
    func.__quick_action__.append(func.__name__)
    return func

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
    
    def get_actions(self):
        methods = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        return [(m, getattr(self,m)) for m in methods if hasattr(getattr(self,m), "__action__")]
    
    def get_quick_actions(self):
        methods = [func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__")]
        return [(m, getattr(self,m)) for m in methods if hasattr(getattr(self,m), "__quick_action__")]

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
