import pygame
import pygame_gui

import os
import subprocess


from projects_settings import *


class App:
    def __init__(self):
        pygame.init()

        self.delta_time = 0

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Projects")
        self.running = True

        self.cur_dir = os.path.dirname(__file__)
        self.folders = [
            f
            for f in os.listdir(self.cur_dir)
            if os.path.isdir(os.path.join(self.cur_dir, f))
        ]

        self.remove_folders = ["__pycache__", ".git", "empty_project"]
        self.folders = [f for f in self.folders if f not in self.remove_folders]

        print(self.folders)

        self.ui_manager = pygame_gui.UIManager(SCREEN_SIZE)

        # create a button for each folder
        self.buttons = []
        for i, folder in enumerate(self.folders):
            self.buttons.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        0,
                        i * 50,
                        100,
                        50,
                    ),
                    text=folder,
                    manager=self.ui_manager,
                )
            )

    def run(self):
        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


            # handle button events
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    for i, button in enumerate(self.buttons):
                        if event.ui_element == button:
                            print(self.folders[i])
                            # can we start a new process here?
                            subprocess.Popen(["python", os.path.join(self.folders[i], "main.py")])
                            #os.system(f"python {self.folders[i]}/main.py")


            self.ui_manager.process_events(event)

    def update(self):
        self.ui_manager.update(self.delta_time)
        pass

    def draw(self):
        self.screen.fill((22, 22, 22))
        # Start draw

        # End draw
        self.ui_manager.draw_ui(self.screen)
        pygame.display.flip()

    pass


def main():
    app = App()
    app.run()
    pass


if __name__ == "__main__":
    main()
