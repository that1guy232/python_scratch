from GameObject import GameObject
import pygame

class Settlement(GameObject):

    def __init__(self, tile_x, tile_y):
        image = pygame.image.load('assets/village.png')
        super().__init__(tile_x, tile_y, image, 0)
        pass

    def update(self, delta_time):
        pass

    def handle_event(self, event):
        pass