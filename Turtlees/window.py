import pygame
import pygame_gui


class Window:
    def __init__(self, width, height):#, ws_server):
        self.width = width
        self.height = height
        #self.ws_server = ws_server

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface((self.width, self.height))

        self.running = False

        self.delta_time = 0

    def start(self):
        self.running = True
        self.main_loop()

    def main_loop(self):
        while self.running:
            self.delta_time = self.clock.tick(60) / 1000.0

            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()

    def update(self):
        self.ui_manager.update(self.delta_time)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ui_manager.draw_ui(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)



class ServerWindow(Window):
    def __init__(self, width, height, ws_server):
        super().__init__(width, height)
        self.ws_server = ws_server

        
        self.test_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text="Test Button",
            manager=self.ui_manager,
        )



    def handle_events(self):
        super().handle_events()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.test_button:
                        # get the first object out of the clients set
                        client = next(iter(self.ws_server.clients))
                        self.ws_server.send_to_client(client, "test message")

            self.ui_manager.process_events(event)
        

