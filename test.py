import pygame
import os
import config

from Classes import load_image, Board, Heroes, upd, World

if __name__ == '__main__':
    alpha = World(100, 100)
    cell_group = config.cell_group
    all_sprites = config.all_sprites
    pygame.init()
    sprite = pygame.sprite.Sprite()
    player_color = 'red'
    size = width, height = 520, 520
    screen = config.screen
    board_global = Board(10, 10, 50, cell_group)
    board_global.render(screen)
    warrior = Heroes('warrior', 10, 30, 0, 3, 'warrior.png', 0, 0, 'red', board_global)
    warrior1 = Heroes('warrior', 10, 30, 0, 3, 'warrior.png', 2, 1, 'red', board_global)
    screen.fill(pygame.Color("black"))
    all_sprites.add(warrior)
    all_sprites.add(warrior1)
    gl_screen = screen
    running = True
    f = 0
    unit = warrior
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                        'units'):
                    if unit:
                        unit.unit_move(*event.pos)
                        all_sprites.update()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                unit = board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                    'units', None)
            if event.type == pygame.MOUSEWHEEL:
                board_global.scroll()
                board_global.zoom_to_center(event.y)
                board_global.update()
                all_sprites.update()
        board_global.scroll()
        cell_group.update()
        board_global.update()
        cell_group.draw(screen)
        all_sprites.update()
        upd(board_global, all_sprites)
        pygame.display.flip()
    pygame.quit()
