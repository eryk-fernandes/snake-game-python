import pygame, os
from pygame.math import Vector2 as Vect

class Snake:
    def __init__(self, cell_number: int) -> None:
        head = Vect(cell_number - 5, cell_number / 2 - 1)

        self.body = [head, Vect(head.x + 1, head.y), Vect(head.x + 2, head.y)]

        self.head_sprite = pygame.image.load(os.path.join('../', 'assets', 'sprites', 'head.png')).convert_alpha()
        self.body_sprite = pygame.image.load(os.path.join('../', 'assets', 'sprites', 'body.png')).convert_alpha()
        self.tail_sprite = pygame.image.load(os.path.join('../', 'assets', 'sprites', 'tail.png')).convert_alpha()

    # Retorna os retângulos da cobra
    def get_snake_rect(self, cell_size: int) -> list:
        width = height = cell_size

        block_list = []

        for block in self.body:
            # Multiplicando as posições pelo tamanho da célula o retângulo é desenhado corretamente na matriz
            x_pos = int(block.x) * cell_size
            y_pos = int(block.y) * cell_size

            block_rect = pygame.Rect(x_pos, y_pos, width, height)
            block_list.append(block_rect)

        return block_list

    # O corpo da cobra aumenta uma célula
    def grow_snake(self) -> None:
        self.body.append(Vect(self.body[-1].x, self.body[-1].y))

    # Move a cabeça da cobra para cima
    # Reposiciona os blocos de corpo no lugar do item do vetor anterior
    # Cria uma lista body e atribui a lista atributo body
    def move_up(self) -> None:
        head = Vect(self.body[0].x, self.body[0].y - 1)
        body = [head]

        for i in range(len(self.body) - 1):
            body.append(Vect(self.body[i].x, self.body[i].y))

        self.body = body

    # Move a cabeça da cobra para baixo
    # Reposiciona os blocos de corpo no lugar do item do vetor anterior
    # Cria uma lista body e atribui a lista atributo body
    def move_down(self) -> None:
        head = Vect(self.body[0].x, self.body[0].y + 1)
        body = [head]

        for i in range(len(self.body) - 1):
            body.append(Vect(self.body[i].x, self.body[i].y))

        self.body = body

    # Move a cabeça da cobra para esquerda
    # Reposiciona os blocos de corpo no lugar do item do vetor anterior
    # Cria uma lista body e atribui a lista atributo body
    def move_left(self) -> None:
        head = Vect(self.body[0].x - 1, self.body[0].y)

        body = [head]

        for i in range(len(self.body) - 1):
            body.append(Vect(self.body[i].x, self.body[i].y))

        self.body = body

    # Move a cabeça da cobra para direita
    # Reposiciona os blocos de corpo no lugar do item do vetor anterior
    # Cria uma lista body e atribui a lista atributo body
    def move_right(self) -> None:
        head = Vect(self.body[0].x + 1, self.body[0].y)
        body = [head]

        for i in range(len(self.body) - 1):
            body.append(Vect(self.body[i].x, self.body[i].y))

        self.body = body

    # Move a cobra usando como referência a última tecla de movimentação pressionada
    def move(self, last_key) -> None:
        if last_key == 'UP' and self.body[0].y <= self.body[1].y:
            self.move_up()
        elif last_key == 'DOWN' and self.body[0].y >= self.body[1].y:
            self.move_down()
        elif last_key == 'LEFT' and self.body[0].x <= self.body[1].x:
            self.move_left()
        elif last_key == 'RIGHT' and self.body[0].x >= self.body[1].x:
            self.move_right()
