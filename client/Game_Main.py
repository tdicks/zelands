import pygame, sys, time
from settings import *
from debug import debug
from level import Level
FPS = 60
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('ZeLaNDS')
        self.clock = pygame.time.Clock()
        self.prev_time = time.time()
        self.dt = 0
        self.level = Level()
        self.font_name = FONT


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            # Limit framerate
            self.clock.tick(FPS)
            # Calculate delta time 
            now = time.time()
            self.dt = now - self.prev_time
           # print(self.dt)
            self.prev_time = now

            self.screen.fill((0,45,10))
            self.level.run(self.dt)
            pygame.display.update()
            #dt = self.clock.tick(FPS) /1000


if __name__ == '__main__':
    game = Game()
    game.run()