from settings import TILE_SIZE

class Tile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = (255, 0, 0)