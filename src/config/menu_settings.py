"""Configuration file for game settings and menu settings.

This file contains various game settings and constants used throughout the game.
These settings include player movement speed, broom speed, tile size, screen width,
and screen height, as well as settings related to the in-game menu.
"""
from config.game_settings import TILESIZE, SCREEN_WIDTH, SCREEN_HEIGHT

#Menu Settings
SIDE_MENU_W = 7*TILESIZE
SIDE_MENU_H = 18*TILESIZE
SIDE_MENU_X = SCREEN_WIDTH - SIDE_MENU_W
SIDE_MENU_Y = ((SCREEN_HEIGHT/TILESIZE - 18)/2)*TILESIZE
