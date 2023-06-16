import pygame


from pygame.sprite import Sprite

from game.utils.constants import ENEMY_1, SCREEN_WIDTH, SCREEN_HEIGHT




class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_size = (40, 60)
        self.image = pygame.transform.scale(ENEMY_1, self.image_size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 5
        self.direction = 1

    def update(self):
        self.rect.x += self.velocity * self.direction
        self.check_boundary()

    def check_boundary(self):
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.change_direction()

    def change_direction(self):
        self.direction *= -1

