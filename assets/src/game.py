import pygame, sys, os
from random import randint

from fruit import Fruit
from snake import Snake
from mechanics import Score
from mechanics import KeysPressed
from menu import Menu

pygame.init()

# Define o tamanho e quantidade células da matriz
CELL_SIZE = 30
CELL_NUMBER = 20

# Define o tamanho da matriz
WIN_WIDTH = WIN_HEIGHT = CELL_SIZE * CELL_NUMBER

# Cria o display usando a matriz
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('SNAKE GAME')

# Cria o relógio pra limitar os quadros por segundo (FPS) do jogo
clock = pygame.time.Clock()
FPS = 10

# Cores
WHITE = (235, 235, 245)
BLUE = (45, 45, 200)

# Criação do objeto Menu com o atributo Nome da Fonte
menu = Menu('segoeuisemibold', BLUE)

# Sprites
fruit_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'fruit.png')).convert_alpha()
snake_head_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'head.png')).convert_alpha()
snake_body_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'body.png')).convert_alpha()
snake_tail_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'tail.png')).convert_alpha()
wall_sprite = pygame.image.load(os.path.join('assets', 'sprites', 'wall.png')).convert_alpha()
grass_sprite = pygame.image.load(os.path.join('assets', 'sprites','grass.png')).convert_alpha()
game_image = pygame.image.load(os.path.join('assets', 'sprites', 'game_image.png')).convert_alpha()

# Toca música de fundo
def play_background_sound():
    pygame.mixer.music.load(os.path.join('assets', 'sounds', 'background_sound.mp3'))
    pygame.mixer.music.play(-1)

# Toca música de fim de jogo
def play_game_over_sound():
    pygame.mixer.music.load(os.path.join('assets', 'sounds', 'game_over_sound.mp3'))
    pygame.mixer.music.play()

# Detecta colisão da cabeça da cobra as demais partes do corpo
def detect_head_body_collision(snake):
    head = snake.body[0]

    for part in snake.body[1:]:
        if head.x == part.x and head.y == part.y:
            return True
    return False

# Detecta colisão da cabeça da cobra com parede
def detect_wall_collision(snake):
    head = snake.body[0]

    if head.y <= 0 or head.y >= CELL_NUMBER - 1 or head.x <= 0 or head.x >= CELL_NUMBER - 1:
        return True
    return False

# Detecta colisão da cabeça da cobra com a fruta
def detect_snake_fruit_collision(snake, fruit):
    head = snake.body[0]

    if head.x == fruit.pos.x and head.y == fruit.pos.y:
        return True
    return False

# Detecta se a posição da fruta ocupa a mesma posição de uma das partes da cobra
def detect_fruit_inside_snake(fruit, snake):
    for part in snake.body:
        if int(fruit.pos.x) == int(part.x) and int(fruit.pos.y) == int(part.y):
            return True
    return False

# Muda a posição da fruta
# Checando se não muda pra uma posição que pertence à cobra
def change_fruit_position(fruit, snake):
    fruit.pos.x = randint(1, CELL_NUMBER - 2)
    fruit.pos.y = randint(1, CELL_NUMBER - 2)

    if detect_fruit_inside_snake(fruit, snake):
        change_fruit_position(fruit, snake)

# Lê os inputs do usuário
def read_user_input():
    return pygame.key.get_pressed()

# Move a cobra
def move_snake(snake, keys_pressed):
    keys = read_user_input()

    # Cada condição só é verdade quando uma tecla WASD é apertada (ou a correspondente na seta)
    # E ao mesmo tempo se a cabeça não colidir com seu corpo indo para tal direção

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and snake.body[0].y <= snake.body[1].y:
        keys_pressed.add_to_list('UP')
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and snake.body[0].y >= snake.body[1].y:
        keys_pressed.add_to_list('DOWN')
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and snake.body[0].x <= snake.body[1].x:
        keys_pressed.add_to_list('LEFT')
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and snake.body[0].x >= snake.body[1].x:
        keys_pressed.add_to_list('RIGHT')

    # Limpa a lista, menos o último item
    keys_pressed.clean_list()

    # Move a cobra usando como referência a última tecla de movimentação pressionada
    snake.move(keys_pressed.get_last_key())

# Detecta uma borda na matriz se a célula na matriz é uma das bordas
def detect_border(x, y):
    if y == 0 or x == 0 or y == CELL_NUMBER - 1 or x == CELL_NUMBER - 1:
        return True
    return False

# Desenha os sprites na matriz
def draw_background():
    for x in range(CELL_NUMBER):
        for y in range(CELL_NUMBER):

            # Desenha as bordas da matriz com o sprite do arbusto (a parede)
            # E o restante com o sprite da grama
            if detect_border(x, y):
                WINDOW.blit(wall_sprite, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                WINDOW.blit(grass_sprite, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Desenha todos os elementos na tela
def draw_game_elements(snake, fruit, score):
    draw_background()

    # Desenha a fruta
    WINDOW.blit(fruit_sprite, fruit.get_fruit_rect(CELL_SIZE))

    # Cria uma lista com os retângulos do corpo da cobra
    snake_blocks = snake.get_snake_rect(CELL_SIZE)

    # Desenha o corpo da cobra
    for block in snake_blocks[1:-1]:
        WINDOW.blit(snake_body_sprite, block)

    # Desenha a causa da cobra
    WINDOW.blit(snake_tail_sprite, snake_blocks[-1])

    # Desenha a cabeça da cobra
    WINDOW.blit(snake_head_sprite, snake_blocks[0])

    # Desenha a pontuação
    font = pygame.font.SysFont('verdana', 20, True)
    score_text = font.render("SCORE: " + str(score.score), 1, BLUE)
    WINDOW.blit(score_text, (5, 2))

    # Atualiza o display
    pygame.display.update()

# Inicia a lógica do jogo
def game_start(snake, fruit, score, keys_pressed):

    play_background_sound()

    while True:
        # Limita à 10 quadros por segundo
        clock.tick(FPS)

        # Checa o evento de fechar a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Detecta colisão da cabeça da cobra com a fruta, mudando a posição da fruta
        if detect_snake_fruit_collision(snake, fruit):
            
            change_fruit_position(fruit, snake)
            snake.grow_snake()
            score.up_score()

        # Detecta colisão da cabeça da cobra com a parede ou próprio corpo
        if detect_wall_collision(snake) or detect_head_body_collision(snake):
            play_game_over_sound()
            # Pausa o programa 2 segundos pra dar tempo da música de fim de jogo tocar
            pygame.time.delay(2000)
            break

        # Move a cobra
        move_snake(snake, keys_pressed)

        # Desenha os elementos
        draw_game_elements(snake, fruit, score)


def init():

    while True:
        # Checa o evento de fechar a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Fecha o jogo
                pygame.quit()

                # Fecha qualquer código que esteja rodando mesmo após o pygame fechar
                sys.exit()

        # Fecha o programa se o usuário apertar ESC
        if read_user_input()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        
        if read_user_input()[pygame.K_SPACE]:

            # Criando os objetos Cobra e Fruta
            # O parâmetro cell_number faz com que os objetos se comportem em acordo com o tamanho da janela
            snake = Snake(CELL_NUMBER)
            fruit = Fruit(CELL_NUMBER)

            # Cria o objeto Score, pra guardar a pontuação
            score = Score()

            # Cria o objeto KeysPressed, pra ler os inputs das teclas WASD (ou respectivas nas setas)
            keys_pressed = KeysPressed('LEFT')

            game_start(snake, fruit, score, keys_pressed)

        # Desenha o menu
        menu.fill_menu(WINDOW)
        # Escreve os textos do menu
        menu.write_text(WINDOW, "SNAKE GAME", 3 * CELL_SIZE, 2 * CELL_NUMBER, WHITE, 60)
        menu.write_text(WINDOW, "PRESS SPACE TO START", 4 * CELL_SIZE, 8 * CELL_NUMBER, WHITE)

        # Desenhando a imagem exemplo do jogo
        WINDOW.blit(game_image, pygame.Rect(80, 270, 420, 270))

        pygame.display.update()
