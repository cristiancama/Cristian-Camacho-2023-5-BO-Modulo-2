import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT

# casi Todo en pygame es un objeto
# Un personaje en mi juego es un objeto (instancia de algo)
# La nave (spaceship) es un personaje => necesito una clase


# SpaceShip es una clase derivada (hija) de Sprite

# spaceship tiene una "imagen"
class SpaceShip(Sprite):
    
    def __init__(self):
        self.image_size = (40, 60)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = self.image_size[0]
        self.image_rect.y = self.image_size[1]
        self.velocity = 5 # Se creo una variable para la velocidad

    def update(self):
        keys = pygame.key.get_pressed() # Esta linea almacena en la variable keys lo que se preciona en el teclado, booleano

        if keys[pygame.K_RIGHT]:  # Verifica si la tecla "right" esta siendo presionada, si es true incremeta la posición x por la velocidad (self.velocity)
            self.image_rect.x += self.velocity
        if keys[pygame.K_LEFT]:
            self.image_rect.x -= self.velocity
        if keys[pygame.K_UP]:
            self.image_rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.image_rect.y += self.velocity
        if self.image_rect.right > SCREEN_WIDTH: # Verifica si el lado derecho de la imagen de la nave ha alcanzado el limite de la pantalla(SCREEN_WIDTH), posición left x = 0
            self.image_rect.left  = 0
        if self.image_rect.left < 0:
            self.image_rect.right = SCREEN_WIDTH
        if self.image_rect.bottom > SCREEN_HEIGHT:
            self.image_rect.top = 0
        if self.image_rect.top < 0:
            self.image_rect.bottom = SCREEN_HEIGHT
        


