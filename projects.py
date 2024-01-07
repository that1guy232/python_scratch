import pygame
import pygame_gui

import os
import subprocess

from projects_settings import *
from new_project import create_project


class App:
    def __init__(self):
        self.folders = None
        pygame.init()

        self.delta_time = 0

        # scaled
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Projects")
        self.running = True

        self.cur_dir = os.path.dirname(__file__)

        self.ui_manager = pygame_gui.UIManager(SCREEN_SIZE)

        self.projects_scrolling_container = pygame_gui.elements.UIScrollingContainer(
            pygame.Rect(0, 0, 265, SCREEN_SIZE[1] - 50),
            manager=self.ui_manager,
        )

        self.new_project_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                270,
                6,
                150,
                50,
            ),
            text="New Project",
            manager=self.ui_manager,
        )
        self.new_project_name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(
                270 + 150 + 5,
                6,
                150,
                50,
            ),
            manager=self.ui_manager,
        )

        # create a button for each folder
        self.project_buttons = []
        self.kill_buttons = []

        self.update_folders()

        self.processes = {}  # dictionary to store Popen objects

    def update_folders(self):
        self.folders = [
            f
            for f in os.listdir(self.cur_dir)
            if os.path.isdir(os.path.join(self.cur_dir, f))
        ]

        remove_folders = ["__pycache__", ".git", "empty_project", ".github", ".idea"]
        self.folders = [f for f in self.folders if f not in remove_folders]

        for i, folder in enumerate(self.folders):
            self.project_buttons.append(
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(
                        5,
                        i * 50,
                        150,
                        50,
                    ),
                    text=folder,
                    manager=self.ui_manager,
                    container=self.projects_scrolling_container,  # pass panel as container
                )
            )

            kill_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    155,
                    i * 50,
                    100,
                    50,
                ),
                text="Kill",
                manager=self.ui_manager,
                container=self.projects_scrolling_container,  # pass panel as container
            )

            kill_button.disable()  # disable "Kill" button by default
            self.kill_buttons.append(kill_button)

        self.projects_scrolling_container.set_scrollable_area_dimensions(
            (245, len(self.folders) * 50)
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
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(self.project_buttons):
                    if event.ui_element == button:
                        p = subprocess.Popen(
                            ["python", os.path.join(self.folders[i], "main.py")]
                        )
                        self.processes[button] = p  # store the Popen object
                        self.kill_buttons[
                            i
                        ].enable()  # enable corresponding "Kill" button
                        button.disable()  # disable main button after it's pressed

                # check if a "kill" button was pressed
                for i, button in enumerate(self.kill_buttons):
                    if event.ui_element == button:
                        if self.project_buttons[i] in self.processes:
                            self.processes[self.project_buttons[i]].terminate()
                            del self.processes[self.project_buttons[i]]
                            button.disable()  # disable "Kill" button again
                            self.project_buttons[
                                i
                            ].enable()  # enable main button when "Kill" is pressed

                # check if "New Project" button was pressed
                if event.ui_element == self.new_project_button:
                    create_project(self.new_project_name.get_text())
                    # update folders list
                    self.update_folders()

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
