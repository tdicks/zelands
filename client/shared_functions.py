import pygame
from os.path import join
from os import walk
from settings import TILESIZE,WHITE,BLACK
import textwrap
import yaml
pygame.init()
#font settings for floating text:
font_name = join('client','menu','cambriab.TTF')
font = pygame.font.Font(font_name, 16)
fsize = 12
WHITE = (255,255,255)

# read the client config yaml
def read_yaml():
    config = None
    # Read YAML file
    with open(os.path.join('config','client.yaml'), 'r') as file:
        config = yaml.safe_load(file)
    print(config['controls'])

# loading of images into list so they can be animated.
def import_folder(path):    
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

#sprite loading / modification functions
def load_collision_tile(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    return image, rect, hitbox

def load_usable_tile(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    info_range = rect.inflate(rect.width * 1.5, rect.height* 1.5)
    return image, rect, hitbox, info_range

def load_walkable_tile(lst,pos):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    return image, rect

def load_weapon(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image,(TILESIZE,TILESIZE))
    rect = image.get_rect(topleft = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    info_range = rect.inflate(rect.width * 3, rect.height* 3)
    return image, rect, hitbox, info_range

def load_player(lst,pos,hitbox_x = 0,hitbox_y = 0):
    image = pygame.image.load(join(*lst)).convert_alpha()
    image = pygame.transform.scale(image, (TILESIZE - image.get_width()/4,TILESIZE))
    rect = image.get_rect(center = pos)
    hitbox = rect.inflate(hitbox_x,hitbox_y)
    return image, rect, hitbox

def tile_rotate(image,amount):
    return pygame.transform.rotate(image,amount)

# in-game functions


def floating_text(in_text, sprite_topleft, colour, better):
    if colour == 'blue' or colour == 'purple':
        default_colour = (255,255,255)
    else:
        default_colour = (0,0,0)
    display_surface = pygame.display.get_surface()
    longest = 0
    text_colour = (255,255,255)
    #Draw rarity box
    pygame.draw.rect(display_surface, colour, (sprite_topleft[0]-12, sprite_topleft[-1]-27, 255, 205))
    #Draw inner box
    pygame.draw.rect(display_surface, BLACK, (sprite_topleft[0]-10, sprite_topleft[-1]-25, 250, 200))
    for i,item in enumerate(in_text):
        # if i > 3:
        #     pass
            # if better[i-4] == -1:
            #     text_colour = (255,0,0)
            # if better[i-4] == 1:
            #     text_colour = (0,255,0)
            # if better[i-4] == 0:
            #     text_colour = default_colour

        # else: 
        #     if colour == 'blue' or colour == 'purple':
        #         text_colour = (255,255,255)
        #     else:
        #         text_colour = (0,0,0)

        # Add text 
        text_surface = font.render(item,True, WHITE)
        text_rect = text_surface.get_rect(bottomleft = (sprite_topleft[0], sprite_topleft[1] + (i * 20)))
        if text_rect.width > longest: longest = text_rect.width
        pygame.draw.rect(display_surface, BLACK, text_rect.inflate(10,3))
        display_surface.blit(text_surface, text_rect)    

def draw_health_bar(surface, position, size, color_border, color_background, color_health, progress):
    pygame.draw.rect(surface, color_background, (*position, *size))
    pygame.draw.rect(surface, color_border, (*position, *size), 1)
    innerPos  = (position[0]+1, position[1]+1)
    innerSize = (int((size[0]-2) * progress), size[1]-2)
    pygame.draw.rect(surface, color_health, (*innerPos, *innerSize))
    print('im supposedly drawing a healthbar somewhere')