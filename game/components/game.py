import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE

from game.components.spaceship import SpaceShip

from game.components.enemy import Enemy

from game.components.bullet import Bullet

from pygame.sprite import Group



# Game tiene un "Spaceship" - Por lo general esto es iniciliazar un objeto Spaceship en el __init__
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False  # variable de control para salir del ciclo
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0

        # Game tiene un "Spaceship"
        self.spaceship = SpaceShip()


        self.enemy = Enemy(SCREEN_WIDTH // 2, 100) # Posición inicial 

        self.bullets = Group() # Lista para almacenar las balas disparadas por el Spaceship
        self.enemies = pygame.sprite.Group() # Grupo para almacenar los sprites de los enemigos.
        self.enemies.add(self.enemy) # Es el sprite de un enemigo en el juego

    def run(self):
        # Game loop: events - update - draw
        self.playing = True

        # while self.playing == True
        while self.playing: # Mientras el atributo playing (self.playing) sea true "repito"
            self.handle_events()
            self.update()
            self.draw()
        else:
            print("Something ocurred to quit the game!!!")
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        # Para un "event" (es un elemento) en la lista (secuencia) que me retorna el metodo get()
        for event in pygame.event.get():
            # si el "event" type es igual a pygame.QUIT entonces cambiamos playing a False
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN: # Detecta la tecla espacio y dispara una bala cuando se presiona
                if event.key == pygame.K_SPACE:
                    self.fire_bullet()


    def fire_bullet(self):
        bullet = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.top)  # Pasa las coordenadas de la nave
        self.bullets.add(bullet) # Se agrega la bala al grupo de balas 


    def update(self):
        # pass
        self.spaceship.update()
        self.enemy.update()  # Actualiza el enemigo    

        # Actualizar las balas y enemigos
        self.bullets.update()
        self.enemies.update()

        # Comprobar colisiones entre balas y enemigos
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()


        # dibujamos el objeto en pantalla
        self.screen.blit(self.spaceship.image, self.spaceship.image_rect)
        self.screen.blit(self.enemy.image, self.enemy.rect) # Dibujamos el enemigo en la pantalla

        # Dibujar las balas
        self.bullets.draw(self.screen)
        
        
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed
