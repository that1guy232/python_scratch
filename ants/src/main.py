from settings import *
import pygame
from camera import Camera
from ents.character import Character


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        # alpha channel support
        self.screen.set_alpha(0)
        self.clock = pygame.time.Clock()
        self.running = True

        self.camera = Camera(0, 0)
        self.character = Character(0, 0)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.camera.update(self.character)
        pass

    def draw(self):
        self.screen.fill((0, 0, 0, 255))

        # draw the entity with the camera offset
        self.character.draw(self.screen, self.camera)
        pygame.display.flip()


if __name__ == '__main__':
    Main().run()
