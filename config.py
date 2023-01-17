import pygame
import pygame.sprite

size = window_width, window_height = 520, 520
screen = pygame.display.set_mode(size)
cell_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mish_sprites = pygame.sprite.Group()
PATTERN = {'warrior' : [10]}
