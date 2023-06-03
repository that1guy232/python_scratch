import pygame
from settings import *
import psutil
import os

class Camera:
    def __init__(self, rect = pygame.Rect(100, 100, SCREEN_WIDTH, SCREEN_HEIGHT)):
        self.rect = rect

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

class TileEnum:
    TILE_GRASS = 0


class Tile:
    def __init__(self):
        self.tile_type = TileEnum.TILE_GRASS
    pass

class TileMap:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = [[Tile() for y in range(height)] for x in range(width)]
        
        self.rendred_tile_surface = pygame.Surface((width * tile_size, height * tile_size))

        # add alpha channel
        self.rendred_tile_surface = self.rendred_tile_surface.convert_alpha()
        self.rendred_tile_surface.fill((0, 0, 0, 0))

 
        self.render_tile_surface()

    def render_tile_surface(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                tile_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if tile.tile_type == TileEnum.TILE_GRASS:
                    pygame.draw.rect(self.rendred_tile_surface, (0, 255, 0, 255), tile_rect,1)


    def draw_tile_surface(self, surface, camera):
        # draw the tile surface offset by the camera position
        rel_pos = camera.rect.topleft


        print(rel_pos)
        surface.blit(self.rendred_tile_surface, rel_pos)    

        pass




class Game:
    def __init__(self):
        pygame.init()
        self.process = psutil.Process(os.getpid())
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        pygame.display.set_caption("My Game")

        self.clock = pygame.time.Clock()
        self.running = True
        self.delta_time = 0

        self.tile_map = TileMap(10, 10, 32)

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

    def update(self):
        pass

    def draw(self):
        self.screen.fill("white")
        # Start draw

        #self.screen.blit(self.tile_map.rendred_tile_surface, (0, 0))
        self.tile_map.draw_tile_surface(self.screen, Camera())


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
