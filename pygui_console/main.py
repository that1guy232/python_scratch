import pygame
import pygame_gui

from settings import *
import psutil
import os


class Game:
    def __init__(self):
        pygame.init()
        self.process = psutil.Process(os.getpid())
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        pygame.display.set_caption("My Game")

        self.ui_manager = pygame_gui.UIManager(SCREEN_SIZE)

        text_entry_height = 50
        self.console_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, text_entry_height)),
            manager=self.ui_manager,
        )

        # create a text box under the text entry line
        self.console_output = pygame_gui.elements.UITextBox(
            html_text="",
            relative_rect=pygame.Rect(
                (0, text_entry_height),
                (SCREEN_WIDTH, SCREEN_HEIGHT - text_entry_height),
            ),
            manager=self.ui_manager,
        )

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

            # if the enter key is pressed get the text from the text entry line
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(self.console_input.get_text())

            self.ui_manager.process_events(event)

    def update(self):
        self.ui_manager.update(self.delta_time)
        pass

    def draw(self):
        self.screen.fill("white")
        # Start draw

        self.ui_manager.draw_ui(self.screen)
        # End draw
        mem_info = self.process.memory_info()
        mem_usage = mem_info.rss / (1024 * 1024)  # Convert to MB
        pygame.display.set_caption(
            f"{TITLE} FPS: {self.clock.get_fps()} Memory: {mem_usage:.2f} MB"
        )
        pygame.display.flip()

    def quit(self):
        self.running = False


if __name__ == "__main__":
    Game()
