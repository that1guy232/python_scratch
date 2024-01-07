import pygame
from .entity import Entity


class Character(Entity):
    def __init__(self, x, y):
        # TODO: replace with a id for the image so we can load it from a dict instead of every ent storing its own image
        image = pygame.image.load('../assets/character.png').convert_alpha()
        super().__init__(x, y, image)
