import math
import pygame

from GameObject import GameObject
from Tile import Tile
from settings import *


GRASS_TILE_IMAGE = pygame.image.load('assets/grass.png')

class Chunk:


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = CHUNK_WIDTH
        self.height = CHUNK_HEIGHT
        self.tiles = []
        self.generate_tiles()
        self.tile_object_map = {}
        for tile in self.tiles:
            self.tile_object_map[tile.x, tile.y] = []

    def add_game_object(self, game_object: GameObject):
        if not isinstance(game_object, GameObject):
            raise TypeError('Only GameObjects can be added to the map.')
        coordinate = (game_object.tile_x, game_object.tile_y)
        if coordinate not in self.tile_object_map:
            raise ValueError('The coordinate provided is not in the map. Please use a coordinate within the chunk.')
        self.tile_object_map[coordinate].append(game_object)

    def generate_tiles(self):
        for y in range(self.height):
            for x in range(self.width):
                self.tiles.append(Tile(x, y))

    def draw(self, screen, camera):
        for tile in self.tiles:
            adjusted_rect = camera.apply(pygame.Rect(tile.x * TILE_SIZE + self.x * self.width * TILE_SIZE, tile.y * TILE_SIZE + self.y * self.height * TILE_SIZE, tile.width, tile.height))
            screen.blit(GRASS_TILE_IMAGE, adjusted_rect)
            pygame.draw.rect(screen, 'black', adjusted_rect, 1)

    def update(self, delta_time):
        for coordinate in self.tile_object_map:
            for game_object in self.tile_object_map[coordinate]:
                game_object.update(delta_time)
        pass

    def get_tile_from_world_pos(self, mouse_world_x, mouse_world_y):
        """
        Returns the tile at the given world position.

        :param mouse_world_x: The x position of the mouse in world coordinates.
        :param mouse_world_y: The y position of the mouse in world coordinates.
        :return: The tile at the given world position.

        """
        tile_x = math.floor(mouse_world_x / TILE_SIZE)
        tile_y = math.floor(mouse_world_y / TILE_SIZE)
        return self.get_tile_from_tile_pos(tile_x, tile_y)

    def get_tile_from_tile_pos(self, tile_x, tile_y):
        """
        Returns the tile at the given tile position.

        :param tile_x: The x position of the tile.
        :param tile_y: The y position of the tile.
        :return: The tile at the given tile position.
        """
        if tile_x < 0 or tile_x >= self.width or tile_y < 0 or (tile_y >= self.height):
            return None
        return self.tiles[tile_y * self.width + tile_x]

    def get_objects_on_tile(self, x, y):
        """
        Returns a list of objects on the tile at the given position.

        :param x: The x position of the tile.
        :param y: The y position of the tile.

        :return: A list of objects on the tile at the given position.
        """
        coordinate = (x, y)
        if coordinate not in self.tile_object_map:
            raise ValueError('The coordinate provided is not in the map. Please use a coordinate within the chunk.')
        return self.tile_object_map[coordinate]

