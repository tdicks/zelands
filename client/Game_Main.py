import pygame, sys
from Settings import *
from debug import debug
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('ZeLaNDS')
        self.clock = pygame.time.Clock()
        self.level = Level(self.clock.tick(60)/1000)
        self.font_name = '/assets/8-BIT WONDER.TTF'


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0,45,10))
            self.level.run()
            pygame.display.update()
            dt = self.clock.tick(FPS) / 1000


if __name__ == '__main__':
    game = Game()
    game.run()