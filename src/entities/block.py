import pygame, os

class Block:
    def __init__(self):
        self.wall_sprite = pygame.image.load(os.path.join('../', 'assets', 'sprites', 'wall.png')).convert_alpha()
        self.grass_sprite = pygame.image.load(os.path.join('../', 'assets', 'sprites', 'grass.png')).convert_alpha()
