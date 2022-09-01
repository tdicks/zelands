import pygame,os, sys
import random
from menu import *

class Game():
    def __init__(self):
        pygame.init()
       # Music Init and Start
        pygame.mixer.init()
        BGM = pygame.mixer.Sound(os.path.join('Assets','sounds','01-The Prelude.mp3'))
        BGM.set_volume(1)
        BGM.play(-1)
       # Game states
        self.running, self.playing = True, False

        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 1024
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = os.path.join('client','menu','8-BIT WONDER.TTF')
       # self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.clock = pygame.time.Clock()
       # Menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.stars(self.DISPLAY_W,self.DISPLAY_H)
            self.draw_text('Insert Awesome Game Here', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            #self.level.run()
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
        self.clock.tick(60) / 1000

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def stars(self,DISPLAY_W,DISPLAY_H):
        #create the locations of the stars for when we animate the background
        star_field_slow = []
        star_field_medium = []
        star_field_fast = []

        for slow_stars in range(50): #birth those plasma balls, baby
            star_loc_x = random.randrange(0, DISPLAY_W)
            star_loc_y = random.randrange(0, DISPLAY_H)
            star_field_slow.append([star_loc_x, star_loc_y])

        for medium_stars in range(35):
            star_loc_x = random.randrange(0, DISPLAY_W)
            star_loc_y = random.randrange(0, DISPLAY_H)
            star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):
            star_loc_x = random.randrange(0, DISPLAY_W)
            star_loc_y = random.randrange(0, DISPLAY_H)
            star_field_fast.append([star_loc_x, star_loc_y])

        for star in star_field_slow:
            star[1] += 1
        if star[1] > DISPLAY_H:
            star[0] = random.randrange(0, DISPLAY_W)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(self.display, DARKGREY, star, 3)

        for star in star_field_medium:
            star[1] += 4
            if star[1] > DISPLAY_H:
                star[0] = random.randrange(0, DISPLAY_W)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.display, LIGHTGREY, star, 2)

        for star in star_field_fast:
            star[1] += 8
            if star[1] > DISPLAY_H:
                star[0] = random.randrange(0, DISPLAY_W)
                star[1] = random.randrange(-20, -5)
            pygame.draw.circle(self.display, CYAN, star, 1)
    #redraw everything we've asked pygame to draw
        pygame.display.flip()
    #set frames per second
        self.clock.tick(30)
