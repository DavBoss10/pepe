import pygame
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # загружаем кадры анимации солдатика без фона
        self.frames_right = [
            pygame.image.load("soldier1.png").convert_alpha(),
            pygame.image.load("soldier2.png").convert_alpha(),
            pygame.image.load("soldier3.png").convert_alpha(),
            pygame.image.load("soldier4.png").convert_alpha()
        ]
        # поворачиваем картинки для бега влево
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

    def update(self):
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

        # чтобы солдатик не выходил за края экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 50:
            self.rect.top = 50
        if self.rect.bottom > 580:
            self.rect.bottom = 580

        # меняем кадры только когда солдатик бежит
        if is_moving:
            self.anim_timer += 1
            if self.anim_timer >= 6:
                self.anim_timer = 0
                self.frame_index += 1
                if self.frame_index >= 4:
                    self.frame_index = 0
        else:
            # когда стоит на месте - первый кадр
            self.frame_index = 0

        if self.direction == "right":
            self.image = self.frames_right[self.frame_index]
        else:
            self.image = self.frames_left[self.frame_index]


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
        self.all_sprites.add(self.player)

        self.font = pygame.font.SysFont("Arial", 32, bold=True)

        # координаты елочек в лесу (сверху и снизу от лесной дороги)
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

    def _update(self):
        self.all_sprites.update()

    def _draw(self):
        # зеленая лесная трава
        self.screen.fill((65, 130, 55))

        # песчаная лесная дорога посередине
        pygame.draw.rect(self.screen, (175, 145, 100), (0, 200, self.screen_widht, 200))
        # края тропинки чуть темнее
        pygame.draw.rect(self.screen, (145, 115, 75), (0, 200, self.screen_widht, 8))
        pygame.draw.rect(self.screen, (145, 115, 75), (0, 392, self.screen_widht, 8))

        # простые камушки на тропинке
        pygame.draw.circle(self.screen, (130, 110, 80), (150, 250), 5)
        pygame.draw.circle(self.screen, (130, 110, 80), (350, 340), 6)
        pygame.draw.circle(self.screen, (130, 110, 80), (550, 270), 4)
        pygame.draw.circle(self.screen, (130, 110, 80), (680, 330), 5)

        # рисуем простые деревья (коричневый ствол и зеленый круг)
        for tx, ty in self.trees:
            pygame.draw.rect(self.screen, (100, 65, 35), (tx - 8, ty + 15, 16, 30))
            pygame.draw.circle(self.screen, (40, 95, 35), (tx, ty), 32)
            pygame.draw.circle(self.screen, (50, 110, 42), (tx - 6, ty - 6), 22)

        # деревянная табличка с цифрой 67 у дороги
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
