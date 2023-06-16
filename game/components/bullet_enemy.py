import pygame

from pygame.sprite import Sprite

from game.utils.constants import BULLET_ENEMY



class BulletEnemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(BULLET_ENEMY, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # Utilizar el centro x de la nave enemiga
        self.rect.bottom = y  # Utilizar la parte inferior (bottom) de la nave enemiga
        self.image_rect = self.rect.copy()
        self.velocity = -10

    def update(self):
        self.rect.y -= self.velocity

        # La bottom es menor que 0 se elimina la bala de la pantalla usando kill
        if self.rect.top < 0:
            self.kill()