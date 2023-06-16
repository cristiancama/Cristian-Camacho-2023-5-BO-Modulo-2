import pygame

from pygame.sprite import Sprite

from game.components.bullet import Bullet

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
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.image_size[0] // 2
        self.rect.y = SCREEN_HEIGHT // 2 - self.image_size[1] // 2
        self.velocity = 10 # Se creo una variable para la velocidad



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
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
        if self.rect.top < 0:
            self.rect.bottom = SCREEN_HEIGHT

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_up(self):
        self.rect.y -= self.velocity

    def move_down(self):
        self.rect.y += self.velocity





