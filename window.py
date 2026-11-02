import pygame
import sys

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

        self.font = pygame.font.SysFont("Arial", 72, bold=True)

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
        pass

    def _draw(self):
        self.screen.fill((40, 44, 52))

        text_surface = self.font.render("67", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen_widht // 2, self.screen_height // 2))
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
