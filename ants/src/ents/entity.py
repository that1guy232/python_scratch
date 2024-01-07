from pygame.sprite import Sprite


class Entity(Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self))
