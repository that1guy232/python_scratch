from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def apply(self, entity):
        """Apply the camera offset to the entity rect
        :param entity: Entity to apply the camera offset to
        :return: Rect with camera offset
        """
        rect = entity.rect.copy()
        rect.x += self.x
        rect.y += self.y
        return rect

    def update(self, target):
        """Update the camera offset
        :param target: Entity to follow
        :return: None
        """

        # center of the target
        self.x = target.rect.centerx + SCREEN_WIDTH / 2
        self.y = target.rect.centery + SCREEN_HEIGHT / 2



