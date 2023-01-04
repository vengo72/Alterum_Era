import pygame
import os
import config
import map_types
from Pil_test import unit_icon


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


class World:
    def __init__(self, width, height, *args, map_type='pangea', **kwargs):
        self.map_type = map_type
        self.chunks = [['plain' for _ in range((width + 9) // 10)] for _ in
                       range((height + 9) // 10)]
        self.chunks = map_types.PANGEA
        board = Board(width, height, 10, config.cell_group)
        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                for y in range(10):
                    for x in range(10):
                        cell_x = x + j * 10
                        cell_y = y + i * 10
                        board.board[cell_y][cell_x].terrain = self.chunks[i][j]
        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                for func in map_types.CHUNKS[self.chunks[i][j]]:
                    func(board, i, j)


class Board:
    def __init__(self, width, height, cell_size, cell_group, top=10, left=10, *args, **kwargs):
        self.cell_size = cell_size
        self.cell_group = cell_group
        self.left = left
        self.top = top
        self.TERRAINS = ['desert', 'plain', 'ocean']
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
            self.left += 3
        elif keys[pygame.K_RIGHT]:
            self.left -= 3
        elif keys[pygame.K_UP]:
            self.top += 3
        elif keys[pygame.K_DOWN]:
            self.top -= 3
        config.all_sprites.update()


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

    def adjacent(self):
        return [self.board.board[self.y - 1][self.x],
                self.board.board[self.y][self.x + 1],
                self.board.board[self.y + 1][self.x],
                self.board.board[self.y][self.x - 1]]

    def update(self):
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top
        self.image = self.board.tiles_images[self.terrain]


class Heroes(pygame.sprite.Sprite):
    def __init__(self, name, damage, health, power, speed, picture, x, y, color, board, *group):
        super().__init__(*group)
        self.name = name
        self.damage = damage
        self.health = health
        self.power = power
        self.speed = speed
        self.board = board
        self.color = color
        self.picture_name = picture
        unit_icon(self.picture_name, self.color)
        self.orig_image = load_image(self.picture_name.split('.')[0] + '_' + color + '.png',
                                     color_key='black')
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
        self.board.board[self.x][self.y].content['units'] = None
        self.board.board[target_cell[0]][target_cell[1]].content['units'] = self

        self.x = target_cell[0]
        self.y = target_cell[1]
        while (self.rect.x != self.x * self.board.cell_size + self.board.left) or (
                self.rect.y != self.y * self.board.cell_size + self.board.top):
            if self.rect.x > self.x * self.board.cell_size + self.board.left:
                self.rect.x -= 1
            if self.rect.x < self.x * self.board.cell_size + self.board.left:
                self.rect.x += 1
            if self.rect.y > self.y * self.board.cell_size + self.board.top:
                self.rect.y -= 1
            elif self.rect.y < self.y * self.board.cell_size + self.board.top:
                self.rect.y += 1
            upd(self.board, self.groups()[0])

    def update(self):
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top
