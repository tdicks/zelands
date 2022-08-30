import pygame,os
import random

screen = pygame.display.set_mode([1024, 768])
height = pygame.display.Info().current_h
width = pygame.display.Info().current_w
pygame.display.set_caption('Window Caption')
clock = pygame.time.Clock()
font_name = os.path.join('client','menu','8-BIT WONDER.TTF')

#create the locations of the stars for when we animate the background
star_field_slow = []
star_field_medium = []
star_field_fast = []

for slow_stars in range(50): #birth those plasma balls, baby
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_slow.append([star_loc_x, star_loc_y]) #i love your balls

for medium_stars in range(35):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_medium.append([star_loc_x, star_loc_y])

for fast_stars in range(15):
    star_loc_x = random.randrange(0, width)
    star_loc_y = random.randrange(0, height)
    star_field_fast.append([star_loc_x, star_loc_y])

#define some commonly used colours
WHITE = (255, 255, 255)
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
                                 
#create the window
pygame.init()

app_is_alive = True

def draw_text(text, size, x, y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    screen.blit(text_surface,text_rect)

while app_is_alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exiting... All hail the void!")
            app_is_alive = False #murderer!
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Exiting... All hail the void!")
            app_is_alive = False #murderer!

    #my soul knows only darkness
    screen.fill(BLACK)
    draw_text('Thanks for Playing', 20, 512, 384)
    #animate some motherfucking stars
    for star in star_field_slow:
        star[1] += 1
        if star[1] > height:
            star[0] = random.randrange(0, width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, DARKGREY, star, 3)

    for star in star_field_medium:
        star[1] += 4
        if star[1] > height:
            star[0] = random.randrange(0, width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, LIGHTGREY, star, 2)

    for star in star_field_fast:
        star[1] += 8
        if star[1] > height:
            star[0] = random.randrange(0, width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, CYAN, star, 1)
    
    #redraw everything we've asked pygame to draw
    pygame.display.flip()
    #set frames per second
    clock.tick(30)

#quit gracefully
pygame.quit()