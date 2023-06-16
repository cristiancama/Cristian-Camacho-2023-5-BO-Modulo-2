import pygame

from pygame.sprite import Sprite

from game.utils.constants import BULLET



class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(BULLET, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocity = 10

    def update(self):
        self.rect.y -= self.velocity

        # La bottom es menor que 0 se elimina la bala de la pantalla usando kill
        if self.rect.bottom < 0:
            self.kill()