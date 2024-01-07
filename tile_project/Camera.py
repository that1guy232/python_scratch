import pygame


class Camera:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.camera_speed = 100

    def apply(self, rect):
        """Returns the adjusted rectangle's position based on the camera's position and zoom."""
        return pygame.Rect((rect.x - self.x) * self.zoom, (rect.y - self.y) * self.zoom, rect.width * self.zoom,
                           rect.height * self.zoom)

    def translate(self, x, y):
        """Translates the camera's position by the given amount."""
        self.x += x
        self.y += y

    def to_world(self, x, y):
        """Returns the world position of the given screen position."""
        return x / self.zoom + self.x, y / self.zoom + self.y

    def to_screen(self, x, y):
        """
        Returns the screen position of the given world position.
        If the world position is not on screen, returns None.
        """
        screen_x = (x - self.x) * self.zoom
        screen_y = (y - self.y) * self.zoom
        if screen_x < 0 or screen_x > self.width or screen_y < 0 or (screen_y > self.height):
            return None
        return screen_x, screen_y

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        temp_speed = self.camera_speed
        if keys[pygame.K_LSHIFT]:
            temp_speed *= 2
        if keys[pygame.K_w]:
            self.y -= temp_speed * delta_time
        if keys[pygame.K_s]:
            self.y += temp_speed * delta_time
        if keys[pygame.K_a]:
            self.x -= temp_speed * delta_time
        if keys[pygame.K_d]:
            self.x += temp_speed * delta_time
