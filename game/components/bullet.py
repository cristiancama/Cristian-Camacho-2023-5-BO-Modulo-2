import pygame

from pygame.sprite import Sprite

from game.utils.constants import BULLET



class Bullet(Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.image_size = (40, 60)
        self.image = pygame.transform.scale(BULLET, (10, 30))  # Ajusta el tamaño de la imagen de la bala
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = -10  # Velocidad de la bala hacia arriba

    def update(self):
        self.rect.y += self.velocity

        # Elimina la bala si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()

        #Detección de colisiones con los enemigos    
        collisions = pygame.sprite.spritecollide(self, self.game.enemy_group, True)
        for enemy in collisions:
            enemy.kill()