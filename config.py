import pygame
import pygame.sprite

size = window_width, window_height = 520, 520
screen = pygame.display.set_mode(size)
cell_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mish_sprites = pygame.sprite.Group()
PATTERN = {'warrior': [10], 'settler': [20]}
turn_owner = 0
change_unit = ''
first_player_name = ''
second_player_name = ''


def reload_map():
    cell_group.empty()
    all_sprites.empty()
