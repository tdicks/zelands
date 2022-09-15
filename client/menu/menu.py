import pygame,os,time
#from .menu_support import *
from game import *
from level import Level
from shared_functions import read_yaml
from settings import *
#define some commonly used colours

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.image = pygame.image.load(os.path.join('assets','sprites', 'menu_selector.png'))
        #self.rect = self.image.get_rect(center = pos)
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 150

    def draw_cursor(self):
        self.game.draw_text('*', 20, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(pygame.transform.scale(self.game.display, self.game.window.get_rect().size), (0,0))
        #self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()  

class SplashScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Splash"

    def display_menu(self):
        self.display_splash = True
        while self.display_splash:
            #self.game.check_events()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Loading...', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.blit_screen()
            time.sleep(1)
            self.state = 'Start'
            self.check_input()

    def check_input(self):
            if self.state == 'Start':
                self.game.curr_menu = self.game.main_menu
                self.game.start_bgm()
                self.display_splash = False

class MainMenu(Menu):
    '''
    Class for main menu
    '''
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        '''
        Draws and displays the main menu
        '''
        self.run_display = True
        while self.run_display:
            # Starts background Music
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", 20, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            #self.cursor_sound()
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            #self.cursor_sound()
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.level = Level()
                self.game.game_loop()
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Exit':
                self.running, self.playing = False, False
                quit()
            self.run_display = False
    
    def cursor_sound(self):
        SFX = pygame.mixer.Sound(os.path.join('Assets','sounds','Gun+Silencer.mp3'))
        SFX.set_volume(self.game.SFX_VOLUME)
        SFX.play(1)
        

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Sound'
        self.soundx, self.soundy = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.soundx + self.offset, self.soundy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Sound", 15, self.soundx, self.soundy)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Sound':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Sound'
                self.cursor_rect.midtop = (self.soundx + self.offset, self.soundy)
        elif self.game.START_KEY:
            if self.state == 'Sound': 
                self.game.curr_menu = self.game.volume
            if self.state == 'Controls': 
                self.game.curr_menu = self.game.controls
        self.run_display = False
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        pygame.mixer.pause()
        CREDITS = pygame.mixer.Sound(os.path.join('Assets','sounds','credits.mp3'))
        CREDITS.set_volume(1)
        CREDITS.play()
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.game.BGM.play()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Judgy , ZeroChaos , Treebeard , DaB00m', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.stars(self.game.DISPLAY_W,self.game.DISPLAY_H, self.game.star_field_slow,self.game.star_field_medium,self.game.star_field_fast)
            self.blit_screen()


class SoundMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'bgm'
        self.bgmx, self.bgmy = self.mid_w, self.mid_h + 20
        self.sfxx, self.sfxy = self.mid_w, self.mid_h + 40
        self.mutex, self.mutey = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.bgmx + self.offset, self.bgmy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.move_cursor()
            if self.game.START_KEY:
                print('Pressed Enter')
            if self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Sound Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('Music Volume : ' + str(round(self.game.BGM_VOLUME,1)), 15, self.bgmx, self.bgmy)
            self.game.draw_text('SFX Volume : ' + str(round(self.game.SFX_VOLUME,1)), 15, self.sfxx, self.sfxy)
            self.game.draw_text('Mute All', 15, self.mutex, self.mutey)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        #print(self.state)
        if self.game.DOWN_KEY:
            #self.cursor_sound()
            if self.state == 'bgm':
                self.cursor_rect.midtop = (self.sfxx + self.offset, self.sfxy)
                self.state = 'sfx'
            elif self.state == 'sfx':
                self.cursor_rect.midtop = (self.mutex + self.offset, self.mutey)
                self.state = 'mute'
            elif self.state == 'mute':
                self.cursor_rect.midtop = (self.bgmx + self.offset, self.bgmy)
                self.state = 'bgm'

        elif self.game.UP_KEY:
            #self.cursor_sound()
            if self.state == 'bgm':
                self.cursor_rect.midtop = (self.mutex + self.offset, self.mutey)
                self.state = 'mute'
            elif self.state == 'mute':
                self.cursor_rect.midtop = (self.sfxx + self.offset, self.sfxy)
                self.state = 'sfx'
            elif self.state == 'sfx':
                self.cursor_rect.midtop = (self.bgmx + self.offset, self.bgmy)
                self.state = 'bgm'

        elif self.game.LEFT_KEY:
            if self.state == 'bgm':
                if self.game.BGM_VOLUME > 0: 
                    self.game.BGM_VOLUME -= 0.1
                    self.game.BGM.set_volume(self.game.BGM_VOLUME)
                    print(str(self.game.BGM_VOLUME))
            if self.state == 'sfx':
                if self.game.SFX_VOLUME > 0:
                    self.game.SFX_VOLUME -= 0.1
                    self.game.SOUND_SELECT.set_volume(self.game.SFX_VOLUME)
                    self.game.SOUND_CURSOR.set_volume(self.game.SFX_VOLUME)
                    print(round(self.game.SFX_VOLUME),1)
                
        elif self.game.RIGHT_KEY:
            if self.state == 'bgm':
                if self.game.BGM_VOLUME < 1:
                    self.game.BGM_VOLUME += 0.1
                    self.game.BGM.set_volume(self.game.BGM_VOLUME)
                    print(str(self.game.BGM_VOLUME))
            if self.state == 'sfx':
                if self.game.SFX_VOLUME < 1:
                    self.game.SFX_VOLUME += 0.1
                    self.game.SOUND_SELECT.set_volume(self.game.SFX_VOLUME)
                    self.game.SOUND_CURSOR.set_volume(self.game.SFX_VOLUME)
                    print(round(self.game.SFX_VOLUME),1)
        
        elif self.game.START_KEY:
            pass




class ControlsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self,game)
        self.state = 'Up'
        self.upx, self.upy = self.mid_w, self.mid_h + 20
        self.downx, self.downy = self.mid_w, self.mid_h + 40
        self.leftx, self.lefty = self.mid_w, self.mid_h + 60
        self.rightx, self.righty = self.mid_w, self.mid_h + 80
        self.pfirex, self.pfirey = self.mid_w, self.mid_h + 100
        self.sfirex, self.sfirey = self.mid_w, self.mid_h + 120
        self.swapweapx, self.swapweapy = self.mid_w, self.mid_h + 140

        self.cursor_rect.midtop = (self.upx + self.offset, self.upy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.move_cursor()
            if self.game.START_KEY:
                print('Pressed Enter')
            if self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Controls', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('Up :' + self.game.config['controls']['up'].split('_')[1], 15, self.upx, self.upy)
            self.game.draw_text('Down : ' + self.game.config['controls']['down'].split('_')[1], 15, self.downx, self.downy)
            self.game.draw_text('Left : ' + self.game.config['controls']['left'].split('_')[1], 15, self.leftx, self.lefty)
            self.game.draw_text('Right : ' + self.game.config['controls']['right'].split('_')[1], 15, self.rightx, self.righty)
            self.game.draw_text('Primary Fire : ', 15, self.pfirex, self.pfirey)
            self.game.draw_text('Alt Fire : ', 15, self.sfirex, self.sfirey)
            self.game.draw_text('Switch Weapon : ', 15, self.swapweapx, self.swapweapy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            #self.cursor_sound()
            if self.state == 'Up':
                self.cursor_rect.midtop = (self.downx + self.offset, self.downy)
                self.state = 'Down'
            elif self.state == 'Down':
                self.cursor_rect.midtop = (self.leftx + self.offset, self.lefty)
                self.state = 'Left'
            elif self.state == 'Left':
                self.cursor_rect.midtop = (self.rightx + self.offset, self.righty)
                self.state = 'Right'
            elif self.state == 'Right':
                self.cursor_rect.midtop = (self.pfirex + self.offset, self.pfirey)
                self.state = 'Primary Fire'
            elif self.state == 'Primary Fire':
                self.cursor_rect.midtop = (self.sfirex + self.offset, self.sfirey)
                self.state = 'Alt Fire'
            elif self.state == 'Alt Fire':
                self.cursor_rect.midtop = (self.swapweapx + self.offset, self.swapweapy)
                self.state = 'Switch Weapon'
            elif self.state == 'Switch Weapon':
                self.cursor_rect.midtop = (self.upx + self.offset, self.upy)
                self.state = 'Up'
        elif self.game.UP_KEY:
            #self.cursor_sound()
            if self.state == 'Up':
                self.cursor_rect.midtop = (self.swapweapx + self.offset, self.swapweapy)
                self.state = 'Switch Weapon'
            elif self.state == 'Switch Weapon':
                self.cursor_rect.midtop = (self.sfirex + self.offset, self.sfirey)
                self.state = 'Alt Fire'
            elif self.state == 'Alt Fire':
                self.cursor_rect.midtop = (self.pfirex + self.offset, self.pfirey)
                self.state = 'Primary Fire'
            elif self.state == 'Primary Fire':
                self.cursor_rect.midtop = (self.rightx + self.offset, self.righty)
                self.state = 'Right'
            elif self.state == 'Right':
                self.cursor_rect.midtop = (self.leftx + self.offset, self.lefty)
                self.state = 'Left'
            elif self.state == 'Left':
                self.cursor_rect.midtop = (self.downx + self.offset, self.downy)
                self.state = 'Down'
            elif self.state == 'Down':
                self.cursor_rect.midtop = (self.upx + self.offset, self.upy)
                self.state = 'Up'
