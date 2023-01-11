import pygame
import os
import config


def upd(board, sprites):
    screen = config.screen
    screen.fill(pygame.Color("black"))
    board.render(screen)
    sprites.draw(screen)
    pygame.display.flip()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def units(cit, old_sprites, unit, select_unit, warrior, board_global, all_sprites, player, event):
    if cit:
        all_sprites = old_sprites.copy()
        cit = False
    if not unit and select_unit:
        select_unit.create_unit(warrior, select_unit.x, select_unit.y, board_global,
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


class World:
    def __init__(self, *args, **kwargs):
        pass


class Board:
    def __init__(self, width, height, cell_size, cell_group, top=10, left=10, *args, **kwargs):
        self.cell_size = cell_size
        self.cell_group = cell_group
        self.left = left
        self.top = top
        self.TERRAINS = ['desert']
        self.tiles_images = {}
        self.tiles_images_originals = {}
        for el in self.TERRAINS:
            picture = el + '_tile.png'
            self.tiles_images_originals[el] = load_image(picture)
            self.tiles_images[el] = pygame.transform.scale(self.tiles_images_originals[el],
                                                           (self.cell_size - 1, self.cell_size - 1))
        self.board = [[Cell(x, y, self, cell_group, {'units': None}) for x in range(width)] for y in
                      range(height)]
        self.width = width
        self.height = height

    def render(self, screen):
        self.cell_group.draw(screen)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        a, b = (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        return int(a), int(b) if self.left + (
                self.cell_size * self.width) >= x >= self.top and self.top + (
                                         self.cell_size * self.height) >= y >= self.top else None

    def zoom_to_center(self, diff):
        window_width, window_height = config.window_width, config.window_height
        center_x, center_y = self.get_cell((window_width // 2, window_height // 2))
        x_from_cell = window_width // 2 - center_x * self.cell_size - self.left
        y_from_cell = window_height // 2 - center_y * self.cell_size - self.top
        self.left = window_width // 2 - center_x * (self.cell_size + diff) - x_from_cell
        self.top = window_height // 2 - center_y * (self.cell_size + diff) - y_from_cell
        self.cell_size += diff

    def get_cell_object(self, x, y):
        return self.board[int(x)][int(y)]

    def update(self):
        for el in self.TERRAINS:
            picture = el + '_tile.png'
            self.tiles_images[el] = pygame.transform.scale(self.tiles_images_originals[el],
                                                           (self.cell_size - 1, self.cell_size - 1))

    def scroll(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.left += 50 // (self.cell_size ** 0.5) + 1
        elif keys[pygame.K_RIGHT]:
            self.left -= 50 // (self.cell_size ** 0.5) + 1
        elif keys[pygame.K_UP]:
            self.top += 50 // (self.cell_size ** 0.5) + 1
        elif keys[pygame.K_DOWN]:
            self.top -= 50 // (self.cell_size ** 0.5) + 1


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, board, group, content, terrain='desert',
                 *args,
                 **kwargs):
        super().__init__(group)
        self.x = x
        self.y = y
        self.board = board
        self.content = content

        self.terrain = terrain
        picture = self.terrain + '_tile.png'
        self.picture_name = picture
        self.image_original = load_image(picture)
        self.image = self.board.tiles_images[terrain]

        self.rect = self.image.get_rect()
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top

    def update(self):
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top
        self.image = self.board.tiles_images[self.terrain]


class Heroes(pygame.sprite.Sprite):
    def __init__(self, name, damage, health, power, speed, picture, x, y, color, board, gold,
                 *group):
        super().__init__(*group)
        self.name = name
        self.damage = damage
        self.health = health
        self.power = power
        self.speed = speed
        self.flag = False
        self.flag2 = False
        self.old_x = 0
        self.old_y = 0
        self.board = board
        self.gold = gold
        self.color = color

        self.orig_image = load_image(picture)
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.board.cell_size + self.board.left
        self.rect.y = y * self.board.cell_size + self.board.top
        self.x = x
        self.y = y

        if self.board.board[x][y].content['units'] is None:
            self.board.board[x][y].content['units'] = self

    def unit_move(self, x, y):
        target_pixel_x, target_pixel_y = x, y
        target_cell = self.board.get_cell((target_pixel_x, target_pixel_y))
        if (((target_cell[0] - self.x)**2)**0.5 + ((target_cell[1] - self.y)**2)**0.5) <= 2:
            self.board.board[self.x][self.y].content['units'] = None
            self.board.board[target_cell[0]][target_cell[1]].content['units'] = self

            self.x = target_cell[0]
            self.y = target_cell[1]

    def update(self):
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))

        while (self.rect.x != self.x * self.board.cell_size + self.board.left) or (
                self.rect.y != self.y * self.board.cell_size + self.board.top):
            if self.rect.x > self.x * self.board.cell_size + self.board.left:
                self.rect.x -= 1
            if self.rect.x < self.x * self.board.cell_size + self.board.left:
                self.rect.x += 1
            if self.rect.y > self.y * self.board.cell_size + self.board.top:
                self.rect.y -= 1
            if self.rect.y < self.y * self.board.cell_size + self.board.top:
                self.rect.y += 1
            upd(self.board, self.groups()[0])

        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top


class City(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, board, color, *group):
        super().__init__(*group)
        self.board = board
        self.color = color

        self.orig_image = load_image(picture)
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.board.cell_size + self.board.left
        self.rect.y = y * self.board.cell_size + self.board.top
        self.x = x
        self.y = y
        self.units = dict()
        self.units['Воин'] = True
        self.buildings = dict()
        self.buildings['стены'] = False

        if self.board.board[int(x)][int(y)].content['units'] is None:
            self.board.board[int(x)][int(y)].content['units'] = self

    def create_unit(self, hero, x, y, board, all_sprite, player, event):
        global all_sprites

        if player.gold > hero.gold and type(board.get_cell_object(x, y).content.get(
                    'units', None)) == City:
            a = event.pos
            b = board.get_cell(a)
            if (-1 <= x - b[0] <= 1) and (-1 <= y - b[1] <= 1) and (b[0] != 0 and b[1] != 0):
                all_sprite.add(Heroes('warrior', 10, 30, 10, 2, 'warrior.png', b[0], b[1], 'red', board, 10))
                all_sprites = all_sprite
                player.gold -= hero.gold
        else:
            print('Денег нет')

    def create_picture(self, hero, x, y, board, all_sprite, player):
        global all_sprites
        if player.gold > hero.gold and type(board.get_cell_object(x, y).content.get(
                'units', None)) == City:
            g = False
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if not board.get_cell_object(i, j).content.get('units', None):
                        all_sprite.add(
                            Heroes('warrior', 10, 30, 10, 2, 'warrior.png', i, j, 'red', board, 10))
                        all_sprites = all_sprite
                        g = True
                        player.gold -= hero.gold
                        break
                if g:
                    break
            if not g:
                print('Ошибка')
        else:
            print('денег нет')

    def update(self):
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))

        while (self.rect.x != self.x * self.board.cell_size + self.board.left) or (
                self.rect.y != self.y * self.board.cell_size + self.board.top):
            if self.rect.x > self.x * self.board.cell_size + self.board.left:
                self.rect.x -= 1
            if self.rect.x < self.x * self.board.cell_size + self.board.left:
                self.rect.x += 1
            if self.rect.y > self.y * self.board.cell_size + self.board.top:
                self.rect.y -= 1
            if self.rect.y < self.y * self.board.cell_size + self.board.top:
                self.rect.y += 1
            upd(self.board, self.groups()[0])

        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top


class Player:
    def __init__(self, color, name, board):
        self.gold = 100
        self.science = 10
        self.color = color
        self.name = name
        self.cities = dict()
        self.cities['firstTown'] = City(5, 5, 'city.png', board, 'red')


class Picture(pygame.sprite.Sprite):
    def __init__(self, name, board, x, y, *group):
        super().__init__(*group)
        self.board = board
        self.name = name
        self.orig_image = load_image(name)
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.board.cell_size + self.board.left
        self.rect.y = y * self.board.cell_size + self.board.top
        self.x = x
        self.y = y

    def update(self):
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))

        while (self.rect.x != self.x * self.board.cell_size + self.board.left) or (
                self.rect.y != self.y * self.board.cell_size + self.board.top):
            if self.rect.x > self.x * self.board.cell_size + self.board.left:
                self.rect.x -= 1
            if self.rect.x < self.x * self.board.cell_size + self.board.left:
                self.rect.x += 1
            if self.rect.y > self.y * self.board.cell_size + self.board.top:
                self.rect.y -= 1
            if self.rect.y < self.y * self.board.cell_size + self.board.top:
                self.rect.y += 1
            upd(self.board, self.groups()[0])

        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top
