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

    def update(self): # Llama a la entrada del teclado y a los limites de la pantalla
        self.handle_input()
        self.handle_boundary()

    def handle_input(self):  # Para manejar la entrada del teclado
        keys = pygame.key.get_pressed()   

        if keys[pygame.K_RIGHT]:
            self.move_right()
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_UP]:
            self.move_up()
        if keys[pygame.K_DOWN]:
            self.move_down()

    def handle_boundary(self):  # Para manejar los límites de la pantalla y los métodos 
        if self.image_rect.right > SCREEN_WIDTH:
            self.image_rect.left = 0
        if self.image_rect.left < 0:
            self.image_rect.right = SCREEN_WIDTH
        if self.image_rect.bottom > SCREEN_HEIGHT:
            self.image_rect.top = 0
        if self.image_rect.top < 0:
            self.image_rect.bottom = SCREEN_HEIGHT

    def move_right(self):
        self.image_rect.x += self.velocity

    def move_left(self):
        self.image_rect.x -= self.velocity

    def move_up(self):
        self.image_rect.y -= self.velocity

    def move_down(self):
        self.image_rect.y += self.velocity


        


