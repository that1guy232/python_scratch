import pygame
from settings import *
import psutil
import os
import math

import pygame_gui


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("My Game")
        self.process = psutil.Process(os.getpid())
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0

        self.amplitude = 100  # The height of the wave
        self.frequency = 0.02  # The number of oscillations
        self.phase_shift = 0  # The phase shift of the wave
        self.speed = 2.0  # Adjust to the desired speed of the wave

        # 128 points starting at x = 0, y = 0 ending at x = screen_width y = 0
        spacing = 1
        print(spacing)
        y = 250

        self.points = [(x, y) for x in range(0, SCREEN_WIDTH, spacing)]
        # a point at the end of the screen
        self.points.append((SCREEN_WIDTH, y))

        self.ui_manager = pygame_gui.UIManager(SCREEN_SIZE)
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (70, 30)),
            text="Reset",
            manager=self.ui_manager,
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((80, 0), (70, 30)),
            text="Quit",
            manager=self.ui_manager,
        )

        self.amplitude_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 30), (150, 20)),
            start_value=100,
            value_range=(0, 200),
            manager=self.ui_manager,
        )
        self.frequency_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 60), (150, 20)),
            start_value=0.02,
            value_range=(0, 0.1),
            manager=self.ui_manager,
        )
        self.phase_shift_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 90), (150, 20)),
            start_value=0,
            value_range=(0, 100),
            manager=self.ui_manager,
        )
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, 120), (150, 20)),
            start_value=2,
            value_range=(-5, 50),
            manager=self.ui_manager,
        )

        self.run()

    def run(self):
        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000.0
            self.phase_shift += (
                self.speed * self.delta_time
            )  
            self.events()
            self.update()
            self.draw()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.reset_button:
                        self.amplitude = 100
                        self.frequency = 0.02
                        self.phase_shift = 0
                        self.speed = 2.0

                    if event.ui_element == self.quit_button:
                        self.quit()

                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.amplitude_slider:
                        self.amplitude = self.amplitude_slider.get_current_value()

                    if event.ui_element == self.frequency_slider:
                        self.frequency = self.frequency_slider.get_current_value()

                    if event.ui_element == self.phase_shift_slider:
                        self.phase_shift = self.phase_shift_slider.get_current_value()

                    if event.ui_element == self.speed_slider:
                        self.speed = self.speed_slider.get_current_value()

            self.ui_manager.process_events(event)

    def update(self):
        # Update points
        for i, (x, _) in enumerate(self.points):
            self.points[i] = (x, self.calculate_wave_y(x))

        self.ui_manager.update(self.delta_time)

    def calculate_wave_y(self, x):
        return SCREEN_HEIGHT // 2 + self.amplitude * math.sin(
            self.frequency * (x + self.phase_shift)
        )

    def draw(self):
        self.screen.fill("white")
        # Start draw

        # Create a polygon that covers the area under the wave
        polygon_points = [(0, SCREEN_HEIGHT)]  # Start at bottom-left
        polygon_points.extend(self.points)  # Add all points of the wave
        polygon_points.append((SCREEN_WIDTH, SCREEN_HEIGHT))  # End at bottom-right

        # Draw the polygon
        pygame.draw.polygon(self.screen, "blue", polygon_points)

        # End draw
        self.ui_manager.draw_ui(self.screen)
        mem_info = self.process.memory_info()
        mem_usage = mem_info.rss / (1024 * 1024)  # Convert to MB
        fps = self.clock.get_fps()
        fps = round(fps, 2)
        pygame.display.set_caption(
            f"{TITLE}: ( FPS: {fps} Memory: {mem_usage:.2f} MB )"
        )
        pygame.display.flip()

    def quit(self):
        self.running = False


if __name__ == "__main__":
    Game()
