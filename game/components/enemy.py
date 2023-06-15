import pygame


from pygame.sprite import Sprite

from game.utils.constants import ENEMY_1, SCREEN_WIDTH, SCREEN_HEIGHT




class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()  # Asegura que el constructor de la clase (sprite) se ejecute antes de la inicialización de enemy
        self.image_size = (40, 60) # Tamaño de la imagen
        self.image = pygame.transform.scale(ENEMY_1, self.image_size)  # Para redimensionar la imagen al tamaño especificado 
        self.rect = self.image.get_rect() # Rectangulo de colisión 
        self.rect.centerx = x  # Coordenadas del centro del rectángulo de colisión
        self.rect.centery = y
        self.velocity = 5  # Velocidad de la nave
        self.direction = 1  # Dirección inicial movimiento hacia la derecha

    def update(self):  #  La nave enemiga se mueve multiplicando su velocidad por la dirección
        self.rect.x += self.velocity * self.direction  
        self.check_boundary()

    def check_boundary(self):  # Si la nave enemiga alcanza los límites de la pantalla se cambia la dirección (change_direction)
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.change_direction()

    def change_direction(self):  # Invierte la dirección multiplicandola por -1
        self.direction *= -1
