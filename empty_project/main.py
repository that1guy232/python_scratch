import pygame
from settings import *
import psutil
import os


class Game:
    def __init__(self):
        pygame.init()
        self.process = psutil.Process(os.getpid())
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        pygame.display.set_caption("My Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0

        self.run()

    def run(self):
        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000.0
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill("white")
        # Start draw

        # End draw
        mem_info = self.process.memory_info()
        mem_usage = mem_info.rss / (1024 * 1024)  # Convert to MB
        pygame.display.set_caption(
            f"Perlin ground FPS: {self.clock.get_fps()} Memory: {mem_usage:.2f} MB"
        )
        pygame.display.flip()

    def quit(self):
        self.running = False


if __name__ == "__main__":
    Game()
