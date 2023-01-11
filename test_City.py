import random

import pygame
import os
import config

from Classes_City import City, Player, Picture
from Classes import load_image, Board, Heroes, upd, World

if __name__ == '__main__':
    alpha = World(20, 20)
    pygame.init()
    all_sprites = pygame.sprite.Group()
    # создадим спрайт
    sprite = pygame.sprite.Sprite()
    player_color = 'red'
    size = width, height = 520, 520
    screen = config.screen
    cell_group = pygame.sprite.Group()
    board_global = alpha.board
    board_global.render(screen)
    screen.fill(pygame.Color("black"))
    player = Player('green', 'Vova', board_global)
    # warrior = Heroes('warrior', 10, 30, 0, 3, 'warrior.png', 0, 0, 'red', board_global, 10)
    all_sprites.add(player.cities['firstTown'])
    old_sprites = all_sprites
    select_unit = False
    gl_screen = screen
    running = True
    cit = False
    unit = None

    cell_group = config.cell_group
    all_sprites = config.all_sprites
    pygame.init()
    sprite = pygame.sprite.Sprite()
    player_color = 'green'
    size = width, height = 520, 520
    screen = config.screen
    board_global = alpha.board
    board_global.render(screen)
    able_tiles = []
    # for y in range(board_global.height):
    #     for x in range(board_global.weight):
    #         able_tiles.append((x, y))
    # x, y = random.choice(able_tiles)
    player = Player('red', 'Vova', board_global)
    all_sprites.add(player.cities['firstTown'])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                        'units'):
                    if unit and type(unit) != City:
                        unit.unit_move(*event.pos)
                        all_sprites.update()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                unit = board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                    'units', None)
                if cit:
                    all_sprites = old_sprites.copy()
                    cit = False
                if not unit and select_unit:
                    select_unit.create_unit('warrior', select_unit.x, select_unit.y, board_global,
                                            all_sprites, player, event)
                    select_unit = False
                    old_sprites = all_sprites.copy()
                elif type(unit) == City:
                    all_sprites = old_sprites.copy()
                    old_sprites = all_sprites.copy()
                    for i in range(board_global.get_cell(event.pos)[0] - 1,
                                   board_global.get_cell(event.pos)[0] + 2):
                        for j in range(board_global.get_cell(event.pos)[1] - 1,
                                       board_global.get_cell(event.pos)[1] + 2):
                            if not board_global.get_cell_object(i, j).content.get('units', None):
                                if i != board_global.get_cell(event.pos)[0] or j != board_global.get_cell(event.pos)[1]:
                                    all_sprites.add(Picture('mish.png', board_global, i, j))
                else:
                    all_sprites = old_sprites.copy()
            if event.type == pygame.MOUSEWHEEL:
                board_global.zoom_to_center(event.y)
                board_global.update()
                all_sprites.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if type(unit) == City:
                        cit = True
                        select_unit = unit
        board_global.scroll()
        screen.fill((0, 0, 0))
        cell_group.update()
        board_global.update()
        cell_group.draw(screen)
        all_sprites.update()
        upd(board_global, all_sprites)
        pygame.display.flip()
    pygame.quit()
