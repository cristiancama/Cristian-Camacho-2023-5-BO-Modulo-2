import pygame

from pygame.sprite import Sprite

from game.utils.constants import GAMEOVER, SCREEN_WIDTH, SCREEN_HEIGHT



class GameOverScreen (Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
    
    def show(self):
        self.screen.fill((0, 0, 0))  # Rellena la pantalla con negro

        # Obtener las dimensiones de la pantalla
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Obtener las dimensiones de la imagen "GAMEOVER"
        gameover_width = GAMEOVER.get_width()
        gameover_height = GAMEOVER.get_height()

        # Calcular las coordenadas de posición para centrar la imagen "GAMEOVER"
        gameover_x = (screen_width - gameover_width) // 2
        gameover_y = (screen_height - gameover_height) // 2

        self.screen.blit(GAMEOVER, (gameover_x, gameover_y))

        # Mostrar el contador de "Game Over"
        text = self.font.render(f"Game Over Count: {self.game_over_count}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, gameover_y + gameover_height + 50))
        self.screen.blit(text, text_rect)

        # Mostrar las opciones de reiniciar y cerrar
        restart_text = self.font.render("Press 'R' to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, text_rect.bottom + 50))
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font.render("Press 'Q' to Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(screen_width // 2, restart_rect.bottom + 30))
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

    def set_game_over_count(self, count):
        self.game_over_count = count