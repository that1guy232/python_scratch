import pygame
import psutil
import os
import math

from settings import *

from GameObject import GameObject
from GameObjectRenderer import GameObjectRenderer
from Camera import Camera
from Chunk import Chunk
from Settlement import Settlement


class Game:

    def __init__(self):
        pygame.init()

        self.process = psutil.Process(os.getpid())

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.camera = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('My Game')

        self.running = True
        self.delta_time = 0
        self.chunks = []
        self.ObjectRenderer = GameObjectRenderer()

        for y in range(-1, 2):
            for x in range(-1, 2):
                self.chunks.append(Chunk(x, y))

        self.test_object = GameObject(8, 8, pygame.image.load('assets/character_outline.png'), 0)
        self.test_settlement = Settlement(0, 0)
        self.get_chunk_by_pos(0, 0).add_game_object(self.test_settlement)
        self.get_chunk_by_pos(0, 0).add_game_object(self.test_object)
        self.run()

    def get_chunk_by_pos(self, x, y):
        """ Returns the chunk at it's given coordinate position."""
        for chunk in self.chunks:
            if chunk.x == x and chunk.y == y:
                return chunk
        raise ValueError('No chunk found at the given position.')

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_world_x, mouse_world_y = self.camera.to_world(*event.pos)
                for chunk in self.chunks:
                    if chunk.x * chunk.width * TILE_SIZE < mouse_world_x < chunk.x * chunk.width * TILE_SIZE + chunk.width * TILE_SIZE and chunk.y * chunk.height * TILE_SIZE < mouse_world_y < chunk.y * chunk.height * TILE_SIZE + chunk.height * TILE_SIZE:
                        for tile in chunk.tiles:
                            if tile.x * TILE_SIZE + chunk.x * chunk.width * TILE_SIZE < mouse_world_x < tile.x * TILE_SIZE + chunk.x * chunk.width * TILE_SIZE + TILE_SIZE and tile.y * TILE_SIZE + chunk.y * chunk.height * TILE_SIZE < mouse_world_y < tile.y * TILE_SIZE + chunk.y * chunk.height * TILE_SIZE + TILE_SIZE:
                                pass

    def update(self):
        self.camera.update(self.delta_time)

        for chunk in self.chunks:
            chunk.update(self.delta_time)

        if pygame.mouse.get_pressed()[0]:
            mouse_world_x, mouse_world_y = self.camera.to_world(*pygame.mouse.get_pos())
            chunk = self.get_chunk_by_mouse_pos(mouse_world_x, mouse_world_y)
            tile = chunk.get_tile_from_world_pos(mouse_world_x, mouse_world_y)
            objects = chunk.get_objects_on_tile(tile.x, tile.y)
            print(objects)

    def draw(self):
        self.screen.fill('white')
        for chunk in self.chunks:
            chunk.draw(self.screen, self.camera)
            self.ObjectRenderer.draw(self.screen, self.camera, chunk)
        mem_info = self.process.memory_info()
        mem_usage = mem_info.rss / (1024 * 1024)
        pygame.display.set_caption(f'{TITLE} FPS: {self.clock.get_fps()} Memory: {mem_usage:.2f} MB')
        pygame.display.flip()

    def quit(self):
        self.running = False

    def get_chunk_by_mouse_pos(self, mouse_world_x, mouse_world_y):
        return self.get_chunk_by_pos(math.floor(mouse_world_x / (TILE_SIZE * CHUNK_WIDTH)),
                                     math.floor(mouse_world_y / (TILE_SIZE * CHUNK_HEIGHT)))
