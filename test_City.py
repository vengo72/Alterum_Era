import pygame
import config
import sys

from PyQt5.QtWidgets import QApplication
from Classes_City import City, Player, Picture, Motion
from Classes import load_image, upd, World
from Classes_City import Example
from Win import End


def main_cycle():
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
    first_player = 'blue'
    second_player = 'green'
    player = Player(first_player, 'Vova', board_global)
    config.turn_owner = 1
    player1 = Player(second_player, 'V1', board_global)
    all_sprites.add(player.cities['firstTown'])
    all_sprites.add(player1.cities['firstTown'])
    g_image = load_image('arrow.png', color_key='green')
    moution = Motion('arrow.png')
    cl = 0
    all_sprites.add(moution)
    app = QApplication(sys.argv)
    en = End()
    en.hide()
    ex = Example()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                cl = -1
                un = board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                    'units')
                mish_sprites = pygame.sprite.Group()
                if not un:
                    if unit and type(unit) != City and (
                            config.turn_owner == 1 and first_player == unit.color or
                            config.turn_owner == 0 and second_player == unit.color):
                        unit.unit_move(*event.pos)
                        all_sprites.update()
                elif un and type(unit) != City and (
                        config.turn_owner == 1 and first_player == unit.color or
                        config.turn_owner == 0 and second_player == unit.color):
                    unit.fight(un, event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mish_sprites = pygame.sprite.Group()
                cl += 1
                if event.pos[0] > 365 and event.pos[1] > 385:
                    moution.new_motion(all_sprites, player, player1)
                    cl = 0
                    continue
                unit = board_global.get_cell_object(*board_global.get_cell(event.pos)).content.get(
                    'units', None)
                if type(unit) != City and unit:
                    if unit == board_global.get_cell_object(
                            *board_global.get_cell(event.pos)).content.get('units',
                                                                           None) and unit.name == 'settler' and cl >= 2 and (
                            config.turn_owner == 1 and first_player == unit.color or
                            config.turn_owner == 0 and second_player == unit.color):
                        f, b = unit.x, unit.y
                        cl = 0
                        t = ex.show_city_messagebox()
                        if t:
                            unit.kill()
                            unit = ''
                            if config.turn_owner == 0:
                                player1.cities['Town'] = City(f, b, 'city.png', board_global,
                                                              player1.color, player1)
                                all_sprites.add(player1.cities['Town'])
                            else:
                                player.cities['Town'] = City(f, b, 'city.png', board_global,
                                                             player.color, player)
                                all_sprites.add(player.cities['Town'])
                            t = False
                if cit:
                    cit = False
                if type(unit) == City and (config.turn_owner == 1 and first_player == unit.color or
                                           config.turn_owner == 0 and second_player == unit.color):
                    ex.show()
                    cl = -1
                    cit = True
                    select_unit = unit
                    for i in range(board_global.get_cell(event.pos)[0] - 1,
                                   board_global.get_cell(event.pos)[0] + 2):
                        for j in range(board_global.get_cell(event.pos)[1] - 1,
                                       board_global.get_cell(event.pos)[1] + 2):
                            if not board_global.get_cell_object(i, j).content.get('units', None):
                                if i != board_global.get_cell(event.pos)[0] or j != \
                                        board_global.get_cell(event.pos)[1]:
                                    mish_sprites.add(Picture('mish.png', board_global, i, j))
                elif not unit and select_unit and (
                        config.turn_owner == 1 and first_player == select_unit.color or
                        config.turn_owner == 0 and second_player == select_unit.color) \
                        and config.change_unit:
                    gh = select_unit.create_unit(config.change_unit, select_unit.x, select_unit.y,
                                                 board_global, event, 1)
                    config.change_unit = ''
                    cl = 0
                    if gh:
                        all_sprites.add(gh)
                    select_unit = False
            if event.type == pygame.MOUSEWHEEL:
                board_global.zoom_to_center(event.y)
                board_global.update()
                all_sprites.update()
                mish_sprites.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    en.show()

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


if __name__ == '__main__':
    main_cycle()
