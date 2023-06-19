import pygame

from pygame.sprite import Sprite

from game.utils.constants import  SCREEN_WIDTH, SCREEN_HEIGHT, WIN

from pygame.locals import *

import sys


class WinScreen (Sprite):
    def __init__(self, screen):
        self.screen = screen

    def show(self):
        self.screen.fill((0, 0, 0))  # Rellena la pantalla con negro

        # Mostrar la imagen "YOU WIN"
        you_win_width = WIN.get_width()
        you_win_height = WIN.get_height()
        you_win_x = (SCREEN_WIDTH - you_win_width) // 2
        you_win_y = (SCREEN_HEIGHT - you_win_height) // 2
        self.screen.blit(WIN, (you_win_x, you_win_y))

        # Mostrar el texto "Presiona 'Q' para salir"
        font = pygame.font.Font(None, 24)
        text = font.render("Presiona 'Q' para salir", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, you_win_y + you_win_height + 30))
        self.screen.blit(text, text_rect)

        pygame.display.flip()
