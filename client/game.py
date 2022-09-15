import pygame,os, sys, time
import random
import yaml
from menu.menu import *
#from Game_Main import Game
from pygame.locals import *
from settings import FONT
FPS = 60

class Game():
    def __init__(self):
       # Music Init and Start
        pygame.mixer.pre_init(44100, -16, 2, 64)

       # Initalize Pygame & Mixer
        pygame.mixer.init()
        pygame.init()

       # Game states
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY, self.F11_KEY = False, False, False, False, False, False, False

       # Display 
        self.fullscreen = False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 1024
        self.monitor_size = [pygame.display.Info().current_w,pygame.display.Info().current_h]
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.bpp = 24 #bit-per-pixel can be set to 8,16 or 24
        self.flags = RESIZABLE|DOUBLEBUF
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)), self.flags, self.bpp)
        self.font_name = FONT

       # self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.prev_time = time.time()
        self.dt = 0

       # Sound
        self.SOUND_CURSOR = pygame.mixer.Sound(os.path.join('assets','sounds','GunSilencer.mp3'))
        self.SOUND_SELECT = pygame.mixer.Sound(os.path.join('assets','sounds','select.wav'))
        self.SFX_VOLUME = 0.5
        self.BGM_VOLUME = 0.5
        self.get_config()

       # Menus
        self.splash = SplashScreen(self)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.volume = SoundMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)

        # self.curr_menu = self.main_menu
        self.curr_menu = self.splash

        # create the locations of the stars for when we animate the background
        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []

        for slow_stars in range(50): #birth those plasma balls, baby
            star_loc_x = random.randrange(0, self.DISPLAY_W)
            star_loc_y = random.randrange(0, self.DISPLAY_H)
            self.star_field_slow.append([star_loc_x, star_loc_y])

        for medium_stars in range(35):
            star_loc_x = random.randrange(0, self.DISPLAY_W)
            star_loc_y = random.randrange(0, self.DISPLAY_H)
            self.star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):
            star_loc_x = random.randrange(0, self.DISPLAY_W)
            star_loc_y = random.randrange(0, self.DISPLAY_H)
            self.star_field_fast.append([star_loc_x, star_loc_y])
        print(self.star_field_fast)
    
    def get_config(self):
        self.config = None
        # Read YAML file
        with open(os.path.join('config','client.yaml'), 'r') as file:
            self.config = yaml.safe_load(file)
    
    def start_bgm(self):
        #self.BGM = pygame.mixer.Sound(os.path.join('Assets','sounds','01-The Prelude.mp3'))
        self.BGM = pygame.mixer.Sound(os.path.join('assets','sounds','NewGame.mp3'))
        self.BGM.set_volume(self.BGM_VOLUME)
        self.BGM.play(-1)

    def fps_counter(self):
        self.font = pygame.font.Font(self.font_name,20)
        self.fps = str(int(self.clock.get_fps()))
        self.fps_t = self.font.render(self.fps , 1, pygame.Color('GREEN'))
        self.window.blit(self.fps_t,(0,0)) 

    def game_loop(self):
        #self.level = Level()
        while self.playing:
            self.check_events()
            # if self.BACK_KEY:
            #     self.playing = False
            #     self.curr_menu = self.main_menu
            # Limit framerate
            self.clock.tick(FPS)
            # Calculate delta time 
            now = time.time()
            self.dt = now - self.prev_time
           # print(self.dt)
            self.prev_time = now
            self.window.fill((0,45,10))
            self.check_events()
            self.level.run(self.dt)
            self.fps_counter()
            self.check_events()
            pygame.display.update()
            pygame.display.flip()
            pygame.event.pump()
    # def cursor_sound(self):
    #     CURSOR = pygame.mixer.Sound(os.path.join('Assets','sounds','cursor_change.mp3'))
    #     CURSOR.play()

    def check_events(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                print('\nGame Shuting Down!')
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                    self.window = pygame.display.set_mode(((SCREEN_WIDTH,SCREEN_HEIGHT)),pygame.RESIZABLE) 
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_m]:
                self.playing = False
                self.curr_menu = self.main_menu

            if event.type == pygame.KEYDOWN: 
                print('KEY pressed is ' + str(event.key) + '.') 
                if event.key == pygame.K_RETURN:
                    self.SOUND_SELECT.play()
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                    self.playing = False
                    self.curr_menu = self.main_menu
                # if event.key == pygame.K_m:
                #     self.playing = False
                #     self.curr_menu = self.main_menu
                if event.key == pygame.K_DOWN:
                    self.SOUND_CURSOR.play()
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.SOUND_CURSOR.play()
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    #self.SFX.play()
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    #self.SFX.play()
                    self.RIGHT_KEY = True
                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.window = pygame.display.set_mode((self.monitor_size),pygame.FULLSCREEN)
                    else:
                        self.window = pygame.display.set_mode((self.display.get_width(),self.display.get_height()),pygame.RESIZABLE)
                        os.environ['SDL_VIDEO_CENTERED'] = '1'
        

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY, self.F11_KEY = False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def stars(self,DISPLAY_W,DISPLAY_H,star_field_slow, star_field_medium,star_field_fast):
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
        self.clock.tick(FPS) / 1000
