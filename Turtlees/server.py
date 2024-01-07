import asyncio
import pygame_gui
import websockets
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIDropDownMenu, UILabel
import threading
import json


class Turtle:
    def __init__(self, id):
        self.id = id
        # Additional properties and methods for Turtle can be added here
        self.fuel = 0


class TurtleManager:
    def __init__(self):
        self.turtle_map = {}
        self.currently_selected_turtle = None

    def connect_turtle(self, id):
        self.turtle_map[id] = Turtle(id)


class WebSocketServer:
    def __init__(self, turtle_manager):
        self.turtle_manager = turtle_manager
        self.server_thread = threading.Thread(target=self.start_server)
        self.loop = asyncio.new_event_loop()
        self.running = True

        self.commands = {
            "connect": self.connect_turtle,
            "heartbeat": lambda: "pong",
            "update_status": self.update_status,
        }

    def connect_turtle(self, id):
        self.turtle_manager.connect_turtle(id)


    def update_status(self, id, fuel):
        print("updating status of turtle " + str(id) + " to " + str(fuel))
        pass

    async def handle_messages(self, websocket, path):
        async for message in websocket:
            decoded = json.loads(message)
            # {'command': {'command': 'command_name', 'data': {various data}}}
            command = decoded["command"]["command"]
            args = decoded["command"]["data"]
            if command in self.commands:
                self.commands[command](**args)


    def start_server(self):
        asyncio.set_event_loop(self.loop)
        start_server = websockets.serve(self.handle_messages, "localhost", 8765)
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.server_thread.join()


class GameWindow:
    def __init__(self, turtle_manager, ws_server):
        self.turtle_manager = turtle_manager
        self.ws_server = ws_server
        self.running = False

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont("Arial", 32)
        self.ui_manager = UIManager((800, 600))

        # a label to tell the user to select a turtle
        turtle_select_x = 5
        turtle_select_y = 30

        label = UILabel(
            pygame.Rect(turtle_select_x, turtle_select_y, 150, 50),
            "Select a turtle",
            self.ui_manager,
        )
        self.turtle_select_dropdown_rect = pygame.Rect(
            turtle_select_x, turtle_select_y + 30, 150, 25
        )
        self.turtle_select_dropdown = UIDropDownMenu(
            ["None"], "None", self.turtle_select_dropdown_rect, self.ui_manager
        )

        # a button to update the status of the selected turtle
        update_status_button_x = 5
        update_status_button_y = 100
        update_status_button_width = 150
        update_status_button_height = 50
        self.update_status_button = UIButton(
            pygame.Rect(
                update_status_button_x,
                update_status_button_y,
                update_status_button_width,
                update_status_button_height,
            ),
            "Update status",
            self.ui_manager,
        )

        self.background = pygame.Surface((800, 600))
        self.background.fill(self.ux_manager.ui_theme.get_colour("dark_bg"))

        self.running = True
        self.main_loop()

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    # if not the first option (None) is selected, get the element id - 1
                    if self.turtle_select_dropdown.selected_option != "None":
                        turtle_id = int(
                            self.turtle_select_dropdown.selected_option.split(" ")[1]
                        )
                        print("selected turtle id: " + str(turtle_id))
                        self.turtle_manager.currently_selected_turtle = turtle_id
                    pass

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.update_status_button:
                        print("update status button pressed")
                        if self.turtle_manager.currently_selected_turtle != None:
                            print(
                                "currently selected turtle: "
                                + str(self.turtle_manager.currently_selected_turtle)
                            )
         

                            pass
                        pass
                self.ui_manager.process_events(event)

            self.screen.fill((0, 0, 0))  # Fill screen with black

            self.draw_ui()

            self.update()

            pygame.display.flip()
        pygame.quit()

    def update(self):
        # how many elements in the dropdown
        # print(len(self.turtle_select_dropdown.object_ids))
        avail = (
            len(self.turtle_select_dropdown.options_list) - 1
        )  # minus the "None" option
        # how many turtles are connected
        # print(len(self.turtle_manager.turtle_map))
        connected = len(self.turtle_manager.turtle_map)
        # rebuild the dropdown if the number of turtles has changed
        if avail != connected:
            list_options = ["None"]
            for i in range(connected):
                list_options.append("id: " + str(i))

            # delete the old dropdown
            self.turtle_select_dropdown.kill()
            print("rebuilding dropdown")
            self.turtle_select_dropdown = UIDropDownMenu(
                list_options, "None", self.turtle_select_dropdown_rect, self.ui_manager
            )

        pass

    def draw_ui(self):
        self.screen.blit(self.background, (0, 0))
        # Display the number of connected turtles
        str_connected = (
            "Connected: " + str(len(self.turtle_manager.turtle_map)) + " turtles"
        )
        text = self.font.render(str_connected, True, (255, 255, 255))
        text_rect = text.get_rect().topleft = (10, 10)

        self.screen.blit(text, text_rect)

        self.ui_manager.draw_ui(self.screen)

        self.ui_manager.update(0.01)


# Main execution
if __name__ == "__main__":
    turtle_manager = TurtleManager()
    ws_server = WebSocketServer(turtle_manager)
    game_window = GameWindow(turtle_manager, ws_server)

    ws_server.start()
    game_window.start()
    ws_server.stop()  # Stop the WebSocket server when Pygame window is closed
