import pygame, os

class Menu:
    def __init__(self, font_name, color):
        self.font_name = font_name
        self.color = color
        self.game_sprite = pygame.image.load(os.path.join('../', 'assets', 'sprites', 'game_image.png')).convert_alpha()

    # Preenche a tela menu
    def fill_menu(self, screen) -> None:
        screen.fill(self.color)

    # Escreve textos na tela
    def write_text(self, screen, text, x, y, color, size=30) -> None:
        font = pygame.font.SysFont(self.font_name, size, True)

        surface = font.render(text, True, color)
        screen.blit(surface, (x, y))
