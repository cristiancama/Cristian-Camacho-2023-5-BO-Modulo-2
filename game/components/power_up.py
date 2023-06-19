import pygame


from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP_SHIELD, SCREEN_HEIGHT, SCREEN_WIDTH

import random


class PowerUp(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(SPACESHIP_SHIELD, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.velocity = 5

    def update(self):
        self.rect.y += self.velocity

        # Si el power-up sale de la pantalla, se elimina
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            