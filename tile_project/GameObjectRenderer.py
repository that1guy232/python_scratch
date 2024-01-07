from settings import TILE_SIZE
import pygame


class GameObjectRenderer:

    def __init__(self):
        pass

    def draw(self, screen, camera, chunk):
        object_map = chunk.tile_object_map
        for coordinate in object_map:
            if len(object_map[coordinate]) == 0:
                continue
            for game_object in object_map[coordinate]:
                adjusted_rect = camera.apply(
                    pygame.Rect(game_object.tile_x * TILE_SIZE + chunk.x * chunk.width * TILE_SIZE,
                                game_object.tile_y * TILE_SIZE + chunk.y * chunk.height * TILE_SIZE,
                                game_object.image.get_width(), game_object.image.get_height()))
                screen.blit(game_object.image, adjusted_rect)
