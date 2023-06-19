import pygame

from pygame.sprite import Sprite

from game.components.bullet import Bullet

from game.utils.constants import SPACESHIP, SCREEN_WIDTH, SCREEN_HEIGHT, SPACESHIP_SHIELD


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

        self.not_shield = True
        self.shield_duration = 3000  # Duración del escudo en milisegundos (3 segundos)


    def update(self): # Llama a la entrada del teclado y a los limites de la pantalla
        self.handle_input()
        self.handle_boundary() 
        self.handle_shield_duration()

    
    def handle_shield_duration(self):
        if not self.not_shield:  # Si el spaceship está protegido por el escudo
            current_time = pygame.time.get_ticks()  # Obtener el tiempo actual en milisegundos
            if current_time - self.shield_start_time >= self.shield_duration:
                self.not_shield = True  # Desactivar el escudo
                self.change_image()  # Cambiar la imagen del spaceship a su imagen original

    def change_image(self): 
        if self.not_shield:
            self.image_size = (40, 60)
            self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        else:
            self.image_size = (60, 60)
            self.image = pygame.transform.scale(SPACESHIP_SHIELD, self.image_size)
        

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





