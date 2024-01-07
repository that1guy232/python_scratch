import pygame
from settings import *
import psutil
import os
import math
import random

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Game:
    def __init__(self):
        pygame.init()
        self.process = psutil.Process(os.getpid())
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("My Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0

        self.bounding_circle_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.bounding_circle_radius = SCREEN_HEIGHT // 2 - 5

        self.bouncy_ball_velocity = [random.randint(-450, 450), random.randint(-450, 450)]
        self.bouncy_ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.bouncy_ball_radius = 5
        self.gravity = 90

        self.trails = pygame.surface.Surface(SCREEN_SIZE)

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
        # Apply gravity
        print(self.bouncy_ball_velocity[1])
        self.bouncy_ball_velocity[1] += self.gravity * self.delta_time

        # Update position
        self.bouncy_ball_pos[0] += self.bouncy_ball_velocity[0] * self.delta_time
        self.bouncy_ball_pos[1] += self.bouncy_ball_velocity[1] * self.delta_time

        # Bounce off the bounding circle
        dist_x = self.bouncy_ball_pos[0] - self.bounding_circle_pos[0]
        dist_y = self.bouncy_ball_pos[1] - self.bounding_circle_pos[1]
        dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if dist > self.bounding_circle_radius - self.bouncy_ball_radius:
            # Move ball back to the edge of the circle
            overlap = dist - (self.bounding_circle_radius - self.bouncy_ball_radius)
            angle = math.atan2(dist_y, dist_x)
            self.bouncy_ball_pos[0] -= overlap * math.cos(angle)
            self.bouncy_ball_pos[1] -= overlap * math.sin(angle)

            # Reflect velocity
            normal_x, normal_y = dist_x / dist, dist_y / dist
            velocity_dot_normal = (self.bouncy_ball_velocity[0] * normal_x +
                                   self.bouncy_ball_velocity[1] * normal_y)
            self.bouncy_ball_velocity[0] -= 2 * velocity_dot_normal * normal_x
            self.bouncy_ball_velocity[1] -= 2 * velocity_dot_normal * normal_y

            # Damp the velocity a bit to simulate energy loss
            self.bouncy_ball_velocity[0] *= 1
            self.bouncy_ball_velocity[1] *= 1

        mem_info = self.process.memory_info()
        mem_usage = mem_info.rss / (1024 * 1024)  # Convert to MB
        pygame.display.set_caption(
            f"{TITLE} FPS: {self.clock.get_fps()} Memory: {mem_usage:.2f} MB"
        )

    def draw(self):
        self.screen.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.circle(
            self.screen,
            pygame.Color(255, 255, 255),
            self.bounding_circle_pos,
            self.bounding_circle_radius,
            3,
        )

        pygame.draw.circle(
            self.screen,
            pygame.Color(255, 255, 255),
            self.bouncy_ball_pos,
            self.bouncy_ball_radius,
            3,
        )
        pygame.display.flip()

    def quit(self):
        self.running = False


if __name__ == "__main__":
    Game()
