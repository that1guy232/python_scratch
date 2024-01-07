class GameObject:
    """
    A class that represents a game object.
    Every game object has a tile position, chunk position, , a sprite, and a z-index for drawing order.
    """

    def __init__(self, tile_x, tile_y, image, z_index):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.image = image
        self.z_index = z_index

    def update(self, delta_time):
        pass

    def handle_event(self, event):
        pass