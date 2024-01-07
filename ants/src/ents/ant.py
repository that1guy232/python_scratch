from src.ents.entity import Entity
import pygame


class Ant(Entity):
    def __init__(self, x, y):
        image = pygame.image.load('../assets/ant.png').convert_alpha()  # TODO: replace with a id for the image so we can load it from a dict instead of every ant having its own image
        super().__init__(x, y, image)
