from multiprocessing import Event
from shared_functions import zoom_keys
from debug import debug as db
import pygame


class SpritesByLayerCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        # Camera offset for tracking the player sprite
        self.offset = pygame.math.Vector2(100,100)

        # Zoom function
        self.zoomscale = 1
        self.full_zoom_resolution = (2500,2500)
        self.surface_zoomed = pygame.Surface(self.full_zoom_resolution, pygame.SRCALPHA)
        self.internal_rect = self.surface_zoomed.get_rect(center = (self.half_height, self.half_width))
        self.internal_surface_vector = pygame.math.Vector2(self.full_zoom_resolution)

        

    def custom_draw(self,player):

        # generating camera offset to follow the player
        zoom_keys(self)
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        self.post_render = []
        self.surface_zoomed.fill((0,45,10))
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.full_zoom_resolution[0] // 2 - self.half_width
        self.internal_offset.y = self.full_zoom_resolution[1] // 2 - self.half_height

        for sprite in self.sprites():
            if "Floor" in str(sprite):
                offset_position = (sprite.rect.topleft - self.offset) + self.internal_offset
                self.surface_zoomed.blit(sprite.image,offset_position)
            else:
                self.post_render.append(sprite) 
        for sprite in sorted(self.post_render,key = lambda sprite: sprite.rect.bottom):
            offset_position = (sprite.rect.topleft - self.offset) + self.internal_offset
            self.surface_zoomed.blit(sprite.image,offset_position)

        scaled_surface = pygame.transform.scale(self.surface_zoomed,self.internal_surface_vector * self.zoomscale)
        scaled_rect = scaled_surface.get_rect(center = (self.half_width, self.half_height))
        self.display_surface.blit(scaled_surface, scaled_rect)