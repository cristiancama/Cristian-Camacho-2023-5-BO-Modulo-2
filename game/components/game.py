import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, GAMEOVER

from game.components.spaceship import SpaceShip

from game.components.enemy import Enemy

from game.components.bullet import Bullet

from game.components.bullet_enemy import BulletEnemy

from pygame.sprite import Group

from pygame.time import get_ticks

from pygame.locals import *

from game.components.game_over_screen import GameOverScreen

from game.components.win_screen import WinScreen

import random

from game.components.power_up import PowerUp


# Game tiene un "Spaceship" - Por lo general esto es iniciliazar un objeto Spaceship en el __init__
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0

        self.score = 0

        self.bullets_hit = 0  # registro de la cantidad de proyectiles disparados por el jugador que han impactado enemigos u objetivos
        self.game_over_count = 0 # conteo de la cantidad de veces que se ha alcanzado el estado de "Game Over" en el juego.

        self.enemy_positions = [] #almacena las posiciones de los enemigos en el juego.

        self.last_enemy_shot = 0 # guarda el tiempo o momento en el juego en el que se realizó el último disparo por parte de un enemigo.

        self.spaceship = SpaceShip()
        self.bullets = Group() #  almacenar y gestionar los proyectiles disparados por el jugador.
        self.enemies = Group() # almacenar y gestionar los enemigos del juego.
        self.bullets_enemy = Group() #  almacenar y gestionar los proyectiles disparados por los enemigos.

        self.power_ups = pygame.sprite.Group()


        self.enemy = self.create_enemy(SCREEN_WIDTH // 2, 100)  # Create an enemy at the specified position

        self.game_over_screen = GameOverScreen(self.screen)

        self.win_screen = WinScreen(self.screen)

    def create_enemy(self, x, y): # Encapsula la creación de un enemigo y su adición al grupo de enemigos
        enemy = Enemy(x, y)
        self.enemies.add(enemy)
        return enemy

    def create_multiple_enemies(self, positions): # crear múltiples enemigos en el juego
        self.enemy_positions.extend(positions) # Actualiza la lista self.enemy_position
        for pos in positions:
            self.create_enemy(*pos)  # Crea el enemigo en cada una de las posiciones

    def create_power_up(self, x, y):  # Añadir argumentos 'x' y 'y' para la posición del power-up
        power_up = PowerUp()
        power_up.rect.x = x
        power_up.rect.y = y
        self.power_ups.add(power_up)

    def run(self):
        self.playing = True
        self.create_multiple_enemies([(100, 100), (200, 100), (300, 100)])  # Ejemplo de creación de múltiples enemigos
        while self.playing:
            self.handle_events()
            self.handle_enemy_events()
            self.update()
            self.draw()
            self.check_win_condition()
        else:
            print("Something occurred to quit the game!!!")
        pygame.display.quit()
        pygame.quit()

    def handle_enemy_events(self):
        current_time = pygame.time.get_ticks()  # Obtener el tiempo actual en milisegundos

        if current_time - self.last_enemy_shot >= 2000: # Controla el tiempo entre los disparos de los enemigos en el juego 
            self.fire_bullet_enemy()
            self.last_enemy_shot = current_time  #  Se actualiza el tiempo del último disparo para el siguiente cálculo

        if random.random() < 0.01:  # Generar power-up con probabilidad del 1%
            self.create_power_up(self.enemy.rect.centerx, self.enemy.rect.bottom)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Presionar la tecla de espacio para disparar un proyectil
                    self.fire_bullet()


    def fire_bullet(self):  # crear una instancia de una bala y agregarla al grupo de balas del juego
        bullet = Bullet(self.spaceship.rect.centerx, self.spaceship.rect.top)
        self.bullets.add(bullet)
    
    def fire_bullet_enemy(self):  # crear instancias de balas enemigas para cada enemigo presente en el juego y agregarlas al grupo de balas enemigas.
        for enemy in self.enemies:
            bullet_enemy = BulletEnemy(enemy.rect.centerx, enemy.rect.bottom)
            self.bullets_enemy.add(bullet_enemy)

    def show_game_over(self):
        self.playing = False  # Controla el estado del juego, al establecerlo en False, indica que el juego ha finalizado.
        self.game_over_count += 1  # Lleva un registro de la cantidad de veces que se ha alcanzado el estado de "Game Over" en el juego.
        self.game_over_screen.set_game_over_count(self.game_over_count)  # Actualizar el contador de "Game Over"
        self.game_over_screen.show()  # Mostrar la pantalla de Game Over

        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_r:  # Presionar la tecla 'R' para reiniciar el juego
                    self.reset_game()
                    break
                elif event.key == K_q:  # Presionar la tecla 'Q' para cerrar la ventana
                    pygame.quit()
                    break
        
    def show_win_screen(self):
        self.playing = False
        self.win_screen.show()

        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                break

    def check_win_condition(self):
        if len(self.enemies) == 0:
            self.show_win_screen()

    def reset_game(self):
        # Restablecer los valores y reiniciar el juego
        self.bullets_hit = 0
        self.enemy_positions = []
        self.last_enemy_shot = 0
        self.spaceship = SpaceShip()
        self.bullets.empty()
        self.enemies.empty()
        self.bullets_enemy.empty()
        self.enemy = self.create_enemy(SCREEN_WIDTH // 2, 100)
        self.score = 0
        self.run()

    def update(self):
        self.spaceship.update()
        self.enemies.update()
        self.bullets.update()
        self.bullets_enemy.update()
        self.power_ups.update()

        # Colisiones entre las balas del spaceship y los enemigos
        #elimina los sprites colisionados de sus grupos correspondientes
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if collisions:
            for enemy in collisions:
                enemy.kill()
                self.score += 1 # Incrementar el puntaje por cada enemigo eliminado

        # Verificar si el contador de balas impactadas es mayor a 5                   
        # Colisiones entre bala enemiga y nave espacial
        collision_spaceship = pygame.sprite.spritecollide(self.spaceship, self.bullets_enemy, True)
        if collision_spaceship:
            self.bullets_hit += len(collision_spaceship)
            if self.bullets_hit >= 5:
                self.show_game_over()

        # Colisiones entre el power_up y la nave espacial
        collisions = pygame.sprite.spritecollide(self.spaceship, self.power_ups, True)
        for self.power_up in collisions:
            self.score += 5
            self.spaceship.not_shield = False
            self.spaceship.shield_start_time = pygame.time.get_ticks()  # Registrar el tiempo de inicio del escudo
            self.spaceship.change_image()


    def draw_score(self):
        font = pygame.font.Font(None, 24)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 40))

    def draw_stats_enemy(self):
        font = pygame.font.Font(None, 24)
        text = font.render(f"Bullets Hit Enemy: {self.bullets_hit}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        self.screen.blit(self.spaceship.image, self.spaceship.rect)
    
        self.enemies.draw(self.screen)  # Se dibuja los enemigos
        self.bullets.draw(self.screen) # Se dibuja las balas del spaceship
        self.bullets_enemy.draw(self.screen) # Se dibuja las balas de los enemigos
        self.draw_score()  # Dibujar el puntaje en la pantalla

        self.draw_stats_enemy()  # Agrega esta línea para dibujar las estadísticas de los proyectiles impactados

        self.power_ups.draw(self.screen)

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

