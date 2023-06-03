import pygame
from settings_perlin_ground import *
import pygame_gui
import psutil
import os
from opensimplex import OpenSimplex


class Game:
    def __init__(self):
        pygame.init()
        self.process = psutil.Process(os.getpid())
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        pygame.display.set_caption("My Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0

        self.ui_manager = pygame_gui.UIManager(SCREEN_SIZE)

        # Perlin Noise parameters
        self.scl = 20  # scale
        self.cols = SCREEN_SIZE[0] // self.scl
        self.rows = SCREEN_SIZE[1] // self.scl
        self.flying = 0
        self.noise_increment = 0.2
        self.color = "black"
        self.update_terrain = True

        self.pressed_keys = []

        self.camera_x = 0  # horizontal position of the camera
        self.camera_y = 0  # vertical position of the camera
        self.camera_speed = 2  # how fast the camera moves each frame

        self.terrain = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        self.noise_generator = OpenSimplex(0)

        # GUI elements
        self.scale_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 20), (200, 20)),
            start_value=20,
            value_range=(10, 50),
            manager=self.ui_manager,
        )

        self.flying_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 50), (200, 20)),
            start_value=0,
            value_range=(-0.02, 0.02),
            manager=self.ui_manager,
        )

        self.noise_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 80), (200, 20)),
            start_value=0.2,
            value_range=(0.05, 0.5),
            manager=self.ui_manager,
        )

        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 140), (100, 20)),
            text="Reset",
            manager=self.ui_manager,
        )

        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((130, 140), (100, 20)),
            text="Pause",
            manager=self.ui_manager,
        )

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

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.scale_slider:
                        self.scl = int(self.scale_slider.get_current_value())
                        self.cols = SCREEN_SIZE[0] // self.scl
                        self.rows = SCREEN_SIZE[1] // self.scl
                        self.terrain = [
                            [0 for _ in range(self.rows)] for _ in range(self.cols)
                        ]

                    elif event.ui_element == self.flying_slider:
                        self.flying = self.flying_slider.get_current_value()

                    elif event.ui_element == self.noise_slider:
                        self.noise_increment = self.noise_slider.get_current_value()

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.reset_button:
                        self.reset()
                    if event.ui_element == self.pause_button:
                        self.update_terrain = not self.update_terrain
                        self.pause_button.set_text(
                            "Resume" if not self.update_terrain else "Pause"
                        )

            # pressed and released keys
            if event.type == pygame.KEYDOWN:
                # wasd keys
                if event.key == pygame.K_w:
                    self.pressed_keys.append(pygame.K_w)
                if event.key == pygame.K_a:
                    self.pressed_keys.append(pygame.K_a)
                if event.key == pygame.K_s:
                    self.pressed_keys.append(pygame.K_s)
                if event.key == pygame.K_d:
                    self.pressed_keys.append(pygame.K_d)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.pressed_keys.remove(pygame.K_w)
                if event.key == pygame.K_a:
                    self.pressed_keys.remove(pygame.K_a)
                if event.key == pygame.K_s:
                    self.pressed_keys.remove(pygame.K_s)
                if event.key == pygame.K_d:
                    self.pressed_keys.remove(pygame.K_d)

            self.ui_manager.process_events(event)

    def update(self):
        # move the camera
        if pygame.K_w in self.pressed_keys:
            self.camera_y -= self.camera_speed
        if pygame.K_a in self.pressed_keys:
            self.camera_x -= self.camera_speed
        if pygame.K_s in self.pressed_keys:
            self.camera_y += self.camera_speed
        if pygame.K_d in self.pressed_keys:
            self.camera_x += self.camera_speed

        if self.update_terrain:
            self.flying -= 0.01
            yoff = self.flying

            for y in range(0, self.rows, 2):
                xoff = 0

                for x in range(0, self.cols, 2):
                    noise_value = self.noise_generator.noise2(xoff, yoff) * 100
                    self.terrain[x][y] = noise_value
                    if x + 1 < self.cols:
                        self.terrain[x + 1][y] = noise_value
                    if y + 1 < self.rows:
                        self.terrain[x][y + 1] = noise_value
                    if x + 1 < self.cols and y + 1 < self.rows:
                        self.terrain[x + 1][y + 1] = noise_value
                    xoff += self.noise_increment

                yoff += self.noise_increment

        self.ui_manager.update(self.delta_time)

    def draw(self):
        self.screen.fill("white")

        triangle_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        for y in range(self.rows - 1):
            for x in range(self.cols - 1):
                # subtract the camera position from each position
                pygame.draw.polygon(
                    triangle_surface,
                    (0, 0, 255, 100),
                    [
                        (
                            x * self.scl - self.camera_x,
                            y * self.scl + self.terrain[x][y] - self.camera_y,
                        ),
                        (
                            (x + 1) * self.scl - self.camera_x,
                            y * self.scl + self.terrain[x + 1][y] - self.camera_y,
                        ),
                        (
                            x * self.scl - self.camera_x,
                            (y + 1) * self.scl + self.terrain[x][y + 1] - self.camera_y,
                        ),
                    ],
                )

                pygame.draw.polygon(
                    triangle_surface,
                    (0, 255, 0, 100),
                    [
                        (
                            (x + 1) * self.scl - self.camera_x,
                            y * self.scl + self.terrain[x + 1][y] - self.camera_y,
                        ),
                        (
                            (x + 1) * self.scl - self.camera_x,
                            (y + 1) * self.scl
                            + self.terrain[x + 1][y + 1]
                            - self.camera_y,
                        ),
                        (
                            x * self.scl - self.camera_x,
                            (y + 1) * self.scl + self.terrain[x][y + 1] - self.camera_y,
                        ),
                    ],
                )

        self.screen.blit(triangle_surface, (0, 0))

        # End draw

        self.ui_manager.draw_ui(self.screen)
        triangle_count = (self.cols - 1) * (self.rows - 1) * 2
        mem_info = self.process.memory_info()
        mem_usage = mem_info.rss / (1024 * 1024)  # Convert to MB
        pygame.display.set_caption(
            f"Perlin ground FPS: {self.clock.get_fps()} Triangle Count: {triangle_count} Memory: {mem_usage:.2f} MB"
        )
        pygame.display.flip()

    def reset(self):
        self.scl = 20
        self.cols = SCREEN_SIZE[0] // self.scl
        self.rows = SCREEN_SIZE[1] // self.scl
        self.flying = 0
        self.terrain = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        self.noise_increment = 0.2
        self.color = "black"
        self.update_terrain = True
        self.scale_slider.set_current_value(20)
        self.flying_slider.set_current_value(0)
        self.noise_slider.set_current_value(0.2)
        self.pause_button.set_text("Pause")

    def quit(self):
        self.running = False


if __name__ == "__main__":
    Game()
