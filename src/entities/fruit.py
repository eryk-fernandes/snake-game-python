import pygame, os
from pygame.math import Vector2 as Vect
from random import randint

class Fruit:
    def __init__(self, cell_number):
        x = randint(1, cell_number - 2)
        y = randint(1, cell_number - 2)

        self.pos = Vect(x, y)
        self.sprite = pygame.image.load(os.path.join('../', 'assets', 'sprites', 'fruit.png')).convert_alpha()

    # Retorna o retângulo da fruta
    def get_fruit_rect(self, cell_size) -> pygame.Rect:
        width = height = cell_size

        # Multiplicando as posições pelo tamanho da célula o retângulo é desenhado corretamente na matriz
        x_pos = int(self.pos.x) * cell_size
        y_pos = int(self.pos.y) * cell_size

        fruit_rect = pygame.Rect(x_pos, y_pos, width, height)
        return fruit_rect
