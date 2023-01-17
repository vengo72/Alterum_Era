import random

import pygame
import os
import config

from Classes_City import City, Player, Picture
from Classes import load_image, Board, Heroes, upd, World
from Pil_test import unit_icon

if __name__ == '__main__':
    alpha = World(50, 50)
    # создадим спрайт
    running = True
    cit = False
    unit = None

    cell_group = config.cell_group
    all_sprites = config.all_sprites
    mish_sprites = config.mish_sprites
    pygame.init()
    sprite = pygame.sprite.Sprite()
    player_color = 'green'
    size = width, height = 520, 520
    screen = config.screen
    board_global = alpha.board
    board_global.render(screen)
    able_tiles = []
    board_global = alpha.board
    board_global.render(screen)
    screen.fill(pygame.Color("black"))
    select_unit = False
    gl_screen = screen
    # for y in range(board_global.height):
    #     for x in range(board_global.weight):
    #         able_tiles.append((x, y))
    # x, y = random.choice(able_tiles)
    player = Player('blue', 'Vova', board_global)
    player1 = Player('green', 'V1', board_global)
    all_sprites.add(player.cities['firstTown'])
    all_sprites.add(player1.cities['firstTown'])
    g_image = load_image('arrow.png', color_key='green')
    im = pygame.transform.scale(g_image.copy(), (100, 70))
    rect = im.get_rect()
    rect.x = 420
    rect.y = 450

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                un = board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                        'units')
                mish_sprites = pygame.sprite.Group()
                if not un:
                    if unit and type(unit) != City:
                        unit.unit_move(*event.pos)
                        all_sprites.update()
                elif un and type(unit) != City:
                    unit.fight(un, event.pos[0], event.pos[1])
                elif unit.color != player.color:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                unit = board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                    'units', None)
                mish_sprites = pygame.sprite.Group()
                if cit:
                    cit = False
                if type(unit) == City:
                    for i in range(board_global.get_cell(event.pos)[0] - 1,
                                   board_global.get_cell(event.pos)[0] + 2):
                        for j in range(board_global.get_cell(event.pos)[1] - 1,
                                       board_global.get_cell(event.pos)[1] + 2):
                            if not board_global.get_cell_object(i, j).content.get('units', None):
                                if i != board_global.get_cell(event.pos)[0] or j != board_global.get_cell(event.pos)[1]:
                                    mish_sprites.add(Picture('mish.png', board_global, i, j))
                elif not unit and select_unit:
                    gh = select_unit.create_unit('warrior', select_unit.x, select_unit.y, board_global, event, 1)
                    if gh:
                        all_sprites.add(gh)
                    select_unit = False
            if event.type == pygame.MOUSEWHEEL:
                board_global.zoom_to_center(event.y)
                board_global.update()
                all_sprites.update()
                mish_sprites.update()
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
        mish_sprites.update()
        upd(board_global, all_sprites, mish_sprites)
        pygame.display.flip()
    pygame.quit()
