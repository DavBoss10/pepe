import pygame
import sys
import random

# --- КЛАСС ПУЛИ ---
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((16, 6), pygame.SRCALPHA)
        self.image.fill((255, 220, 0))  # Желтый цвет пули
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 12
        self.direction = direction

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()


# --- КЛАСС ХАОТИЧНО ДВИЖУЩИХСЯ МИШЕНЕЙ ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.radius = 16
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (230, 40, 40), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius // 2)
        
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.x = random.randint(50, self.screen_width - 50)
        self.rect.y = random.randint(50, self.screen_height - 50)
        self.speed_x = random.choice([-3, -2, 2, 3])
        self.speed_y = random.choice([-3, -2, 2, 3])
        self.change_dir_timer = random.randint(30, 90)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от рамок экрана 800x600
        if self.rect.left <= 0 or self.rect.right >= self.screen_width:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            self.speed_y *= -1

        self.change_dir_timer -= 1
        if self.change_dir_timer <= 0:
            self.speed_x = random.choice([-3, -2, 1, 2, 3])
            self.speed_y = random.choice([-3, -2, 1, 2, 3])
            self.change_dir_timer = random.randint(30, 90)


# --- КЛАСС ИГРОКА ---
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames_right = [
            pygame.image.load("soldier1.png").convert_alpha(),
            pygame.image.load("soldier2.png").convert_alpha(),
            pygame.image.load("soldier3.png").convert_alpha(),
            pygame.image.load("soldier4.png").convert_alpha()
        ]
        self.frames_left = [
            pygame.transform.flip(img, True, False) for img in self.frames_right
        ]

        self.direction = "right"
        self.frame_index = 0
        self.image = self.frames_right[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.speed = 5
        self.anim_timer = 0
        self.shoot_cooldown = 0

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        keys = pygame.key.get_pressed()
        is_moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"
            is_moving = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
            is_moving = True

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            is_moving = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            is_moving = True

        # 1. ОГРАНИЧЕНИЕ ДВИЖЕНИЯ ПО КРАЯМ ЭКРАНА
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

        # Анимация
        if is_moving:
            self.anim_timer += 1
            if self.anim_timer >= 6:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames_right)
        else:
            self.frame_index = 0

        if self.direction == "right":
            self.image = self.frames_right[self.frame_index]
        else:
            self.image = self.frames_left[self.frame_index]

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 10  # Задержка между выстрелами
            bullet_x = self.rect.right if self.direction == "right" else self.rect.left
            bullet_y = self.rect.centery - 2
            return Bullet(bullet_x, bullet_y, self.direction)
        return None


# --- КЛАСС ИГРЫ ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen_widht = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_widht, self.screen_height))
        pygame.display.set_caption("PYGAME GAME 67")

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.is_running = True

        self.player = Player(self.screen_widht // 2, self.screen_height // 2)

        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.all_sprites.add(self.player)

        # 3. ДОБАВЛЕНИЕ ХАОТИЧНО ДВИЖУЩИХСЯ ОБЪЕКТОВ
        for _ in range(5):
            enemy = Enemy(self.screen_widht, self.screen_height)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        self.trees = [
            (80, 90), (230, 70), (420, 100), (600, 75), (730, 95),
            (110, 480), (290, 500), (480, 475), (670, 495)
        ]

    def run(self):
        while self.is_running:
            self._check_events()
            self._update()
            self._draw()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False

        # 2. СТРЕЛЬБА ПО НАЖАТИЮ / ЗАЖАТИЮ ПРОБЕЛА
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)

    def _update(self):
        self.all_sprites.update()

        # Уничтожение/возрождение мишеней при попадании пули
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy in hits:
            enemy.respawn()

    def _draw(self):
        self.screen.fill((65, 130, 55))

        pygame.draw.rect(self.screen, (175, 145, 100), (0, 200, self.screen_widht, 200))
        pygame.draw.rect(self.screen, (145, 115, 75), (0, 200, self.screen_widht, 8))
        pygame.draw.rect(self.screen, (145, 115, 75), (0, 392, self.screen_widht, 8))

        pygame.draw.circle(self.screen, (130, 110, 80), (150, 250), 5)
        pygame.draw.circle(self.screen, (130, 110, 80), (350, 340), 6)
        pygame.draw.circle(self.screen, (130, 110, 80), (550, 270), 4)
        pygame.draw.circle(self.screen, (130, 110, 80), (680, 330), 5)

        for tx, ty in self.trees:
            pygame.draw.rect(self.screen, (100, 65, 35), (tx - 8, ty + 15, 16, 30))
            pygame.draw.circle(self.screen, (40, 95, 35), (tx, ty), 32)
            pygame.draw.circle(self.screen, (50, 110, 42), (tx - 6, ty - 6), 22)

        pygame.draw.rect(self.screen, (90, 55, 30), (395, 155, 10, 45))
        pygame.draw.rect(self.screen, (160, 110, 60), (360, 125, 80, 40))
        pygame.draw.rect(self.screen, (90, 55, 30), (360, 125, 80, 40), 3)
        sign_text = self.font.render("67", True, (255, 255, 255))
        self.screen.blit(sign_text, (383, 128))

        self.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
