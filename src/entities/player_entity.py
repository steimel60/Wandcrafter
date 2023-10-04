from items.wand import Wand
import pygame as pg

class PlayerEntitiy:
    def __init__(
            self,
            name : str = None,
            wand : Wand = None
            ) -> None:
        self.name = name
        self.wand = wand