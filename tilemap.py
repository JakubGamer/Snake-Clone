import pygame
pygame.init()
from structures import Vec2

class TilemapRow:
    def __init__(self, image, tile_dimensions, row_num):
        self.image = image
        self.row_num = row_num
        self.tile_dimensions = tile_dimensions
    
    def __getitem__(self, index):
        tile = pygame.Surface(tuple(self.tile_dimensions), pygame.SRCALPHA, 32)
        tile.blit(self.image, tuple(-Vec2(index, self.row_num) * self.tile_dimensions))
        return tile

class Tilemap:
    def __init__(self, filepath, tile_dimensions):
        self.image = pygame.image.load(filepath).convert_alpha()
        self.tile_dimensions = tile_dimensions
    
    def __getitem__(self, index):
        return TilemapRow(self.image, self.tile_dimensions, index)