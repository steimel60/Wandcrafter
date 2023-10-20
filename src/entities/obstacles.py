"""Obstacle Class"""
import pygame as pg

class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)
