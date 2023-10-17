"""Configuration file for game settings.

This file contains important settings for your game, including the game title,
screen dimensions (width and height), frames per second (FPS), and tile size.
It also calculates the grid dimensions based on the screen dimensions and tile size.
"""
# game settings
GAME_TITLE = "Wandcrafter"
SCREEN_WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
SCREEN_HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60

TILESIZE = 32
GRIDWIDTH = SCREEN_WIDTH / TILESIZE
GRIDHEIGHT = SCREEN_HEIGHT / TILESIZE
