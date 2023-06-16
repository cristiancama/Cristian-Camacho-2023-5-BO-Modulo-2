import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, GAMEOVER

from game.components.spaceship import SpaceShip

from game.components.enemy import Enemy

from game.components.bullet import Bullet

from game.components.bullet_enemy import BulletEnemy

from pygame.sprite import Group

from pygame.time import get_ticks



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

        self.bullets_hit = 0
        self.game_over_count = 0

        self.enemy_positions = []

        self.last_enemy_shot = 0

        self.spaceship = SpaceShip()
        self.bullets = Group()
        self.enemies = Group()
        self.bullets_enemy = Group()

        self.enemy = self.create_enemy(SCREEN_WIDTH // 2, 100)  # Create an enemy at the specified position

    def create_enemy(self, x, y): # Encapsula la creación de un enemigo y su adición al grupo de enemigos
        enemy = Enemy(x, y)
        self.enemies.add(enemy)
        return enemy

    def create_multiple_enemies(self, positions):
        self.enemy_positions.extend(positions)
        for pos in positions:
            self.create_enemy(*pos)  # Descomprimir la tupla de posición y crear un enemigo

    def run(self):
        self.playing = True
        self.create_multiple_enemies([(100, 100), (200, 100), (300, 100)])  # Ejemplo de creación de múltiples enemigos
        while self.playing:
            self.handle_events()
            self.handle_enemy_events()
            self.update()
            self.draw()
        else:
            print("Something occurred to quit the game!!!")
        pygame.display.quit()
        pygame.quit()

    def handle_enemy_events(self):
        current_time = pygame.time.get_ticks()  # Obtener el tiempo actual en milisegundos

        if current_time - self.last_enemy_shot >= 2000:
            self.fire_bullet_enemy()
            self.last_enemy_shot = current_time

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Presionar la tecla de espacio para disparar un proyectil
                    self.fire_bullet()

    def fire_bullet(self):  # Encapsula la creación de un proyectil y su adición al grupo de balas
        bullet = Bullet(self.spaceship.rect.centerx, self.spaceship.rect.top)
        self.bullets.add(bullet)
    
    def fire_bullet_enemy(self):
        for enemy in self.enemies:
            bullet_enemy = BulletEnemy(enemy.rect.centerx, enemy.rect.bottom)
            self.bullets_enemy.add(bullet_enemy)

    def show_game_over(self):
        self.playing = False
        self.game_over_count += 1

        # Obtener las dimensiones de la pantalla
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Obtener las dimensiones de la imagen "GAMEOVER"
        gameover_width = GAMEOVER.get_width()
        gameover_height = GAMEOVER.get_height()

        # Calcular las coordenadas de posición para centrar la imagen "GAMEOVER"
        gameover_x = (screen_width - gameover_width) // 2
        gameover_y = (screen_height - gameover_height) // 2

        self.screen.blit(GAMEOVER, (gameover_x, gameover_y))
        pygame.display.flip()
        pygame.time.wait(2000)  # Espera 2 segundos antes de salir del juego

    def update(self):
        self.spaceship.update()
        self.enemies.update()
        self.bullets.update()
        self.bullets_enemy.update()

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if collisions:
            for enemy in collisions:
                enemy.kill()
            self.bullets_hit += len(collisions)

        # Verificar si el contador de balas impactadas es mayor a 5                   
        # Colisiones entre bala enemiga y nave espacial
        collision_spaceship = pygame.sprite.spritecollide(self.spaceship, self.bullets_enemy, True)
        if collision_spaceship:
            self.bullets_hit += len(collision_spaceship)
            if self.bullets_hit >= 5:
                self.show_game_over()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        self.screen.blit(self.spaceship.image, self.spaceship.rect)
    
        self.enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.bullets_enemy.draw(self.screen)

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

