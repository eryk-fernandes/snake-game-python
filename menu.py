import pygame

class Menu:
    def __init__(self, font_name, color):
        self.font_name = font_name
        self.color = color

    # Preenche a tela menu
    def fill_menu(self, screen):
        screen.fill(self.color)

    # Escreve textos na tela
    def write_text(self, screen, text, x, y, color, size=30):
        font = pygame.font.SysFont(self.font_name, size, True)

        surface = font.render(text, 1, color)
        screen.blit(surface, (x, y))
