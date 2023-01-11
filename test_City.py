import pygame
import os
import config

from Classes import load_image, Board, Heroes, upd, City, Player

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
    screen.fill(pygame.Color("black"))
    player = Player('red', 'Vova', board_global)
    warrior = Heroes('warrior', 10, 30, 0, 3, 'warrior.png', 0, 0, 'red', board_global, 10)
    all_sprites.add(player.cities['firstTown'])
    gl_screen = screen
    running = True
    cit = False
    f = 0
    unit = None
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
                if type(unit) == City:
                    cit = True
            if event.type == pygame.MOUSEWHEEL:
                board_global.zoom_to_center(event.y)
                board_global.update()
                all_sprites.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if type(unit) == City:
                        unit.create_unit(warrior, unit.x, unit.y, board_global, all_sprites, player)
        board_global.scroll()
        screen.fill((0, 0, 0))
        cell_group.update()
        board_global.update()
        cell_group.draw(screen)
        all_sprites.update()
        upd(board_global, all_sprites)
        pygame.display.flip()
    pygame.quit()
