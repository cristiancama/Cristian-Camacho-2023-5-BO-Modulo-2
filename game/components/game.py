import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE

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
        for pos in positions:
            self.create_enemy(*pos)  # Descomprimir la tupla de posición y crear un enemigo

    def run(self):
        self.playing = True
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

        if current_time - self.last_enemy_shot >= 2000:  # Verificar si han pasado 2 segundos (2000 ms)
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
        bullet = Bullet(self.spaceship.image_rect.centerx, self.spaceship.image_rect.top)
        self.bullets.add(bullet)
    
    def fire_bullet_enemy(self):
        bullet_enemy = BulletEnemy(self.enemy.rect.centerx, self.enemy.rect.bottom)
        self.bullets_enemy.add(bullet_enemy)

    def update(self):
        self.spaceship.update()
        self.enemies.update()
        self.bullets.update()
        self.bullets_enemy.update()

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if collisions:
            for enemy in collisions:
                enemy.kill()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()

        self.screen.blit(self.spaceship.image, self.spaceship.image_rect)
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

