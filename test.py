import pygame
import os
import config

from Classes import load_image, Board, Heroes, upd

if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    # создадим спрайт
    sprite = pygame.sprite.Sprite()
    player_color = 'red'
    size = width, height = 520, 520
    screen = config.screen
    cell_group = pygame.sprite.Group()
    board_global = Board(10, 10, 50, cell_group)
    board_global.render(screen)
    warrior = Heroes('warrior', 10, 30, 0, 3, 'warrior.png', 0, 0, 'red', board_global)
    warrior1 = Heroes('warrior1', 10, 30, 0, 3, 'warrior.png', 2, 1, 'red', board_global)
    screen.fill(pygame.Color("black"))
    all_sprites.add(warrior)
    all_sprites.add(warrior1)
    gl_screen = screen
    running = True
    f = 0
    unit = warrior
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                        'units'):
                    if unit:
                        unit.flag = True
                    f = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                f = event.pos
                unit = board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                    'units', None)
                if unit:
                    unit.flag2 = True
                    unit.flag = False
                    unit.old_x = f[0]
                    unit.old_y = f[1]
            if unit:
                if unit.flag and unit.flag2:
                    unit.update(f[0], f[1])
            if event.type == pygame.MOUSEWHEEL:
                board_global.zoom_to_center(event.y)
                board_global.update()
                cell_group.draw(screen)
        board_global.scroll()
        for el in all_sprites:
            el.image = pygame.transform.scale(el.image,
                                                (el.board.cell_size, el.board.cell_size))
            el.rect = el.image.get_rect()
            el.rect.x = el.x * el.board.cell_size + el.board.left
            el.rect.y = el.y * el.board.cell_size + el.board.top
            el.rect.x = el.x * el.board.cell_size + el.board.left
            el.rect.y = el.y * el.board.cell_size + el.board.top
        screen.fill((0, 0, 0))
        cell_group.update()
        board_global.update()
        cell_group.draw(screen)
        upd(board_global, all_sprites)
        pygame.display.flip()
    pygame.quit()
