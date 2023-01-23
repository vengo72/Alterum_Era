import pygame
import os
import config
from Pil_test import unit_icon, city_icon
import map_types
import random
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox


def upd(board, sprites, sp1=''):
    screen = config.screen
    board.render(screen)

    screen.fill(pygame.Color("black"))
    board.render(screen)
    sprites.draw(screen)
    if sp1:
        sp1.draw(screen)
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
        self.board = Board(width, height, 10, config.cell_group)
        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                for y in range(10):
                    for x in range(10):
                        cell_x = x + j * 10
                        cell_y = y + i * 10
                        self.board.board[cell_y][cell_x].terrain = self.chunks[i][j]
        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                for func in map_types.CHUNKS[self.chunks[i][j]]:
                    func(self.board, i, j)


class Board:
    def __init__(self, width, height, cell_size, cell_group, top=10, left=10, *args, **kwargs):
        self.cell_size = cell_size
        self.cell_group = cell_group
        self.left = left
        self.top = top
        self.TERRAINS = ['desert', 'plain', 'ocean', 'plainHill', 'mountain']
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

    def update(self):
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top
        self.image = self.board.tiles_images[self.terrain]


class Heroes(pygame.sprite.Sprite):
    def __init__(self, name, damage, health, power, speed, picture, x, y, color, board, gold, range,
                 *group):
        super().__init__(*group)
        self.name = name
        self.range = range
        self.damage = damage
        self.health = health
        self.power = power
        self.max_power = power
        self.speed = speed
        self.board = board
        self.color = color
        self.picture_name = picture
        self.gold = gold

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
        i = (((target_cell[0] - self.x) ** 2) ** 0.5 + ((target_cell[1] - self.y) ** 2) ** 0.5)
        if i <= 2 and self.power - i >= 0:
            self.board.board[self.x][self.y].content['units'] = None
            self.board.board[target_cell[0]][target_cell[1]].content['units'] = self
            self.power -= i
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

    def fight(self, opponent, x, y):
        if self.color is not opponent.color:
            target_pixel_x, target_pixel_y = x, y
            target_cell = self.board.get_cell((target_pixel_x, target_pixel_y))
            i = (((target_cell[0] - self.x) ** 2) ** 0.5 + ((target_cell[1] - self.y) ** 2) ** 0.5)
            if i <= self.range and self.power >= 0:
                self.power -= 1
                self.health -= opponent.damage
                opponent.health -= self.damage
                if self.health <= 0 and opponent.health <= 0:
                    self.board.board[self.x][self.y].content['units'] = None
                    opponent.board.board[opponent.x][opponent.y].content['units'] = None
                    self.kill()
                    opponent.kill()
                else:
                    if self.health <= 0:
                        self.board.board[self.x][self.y].content['units'] = \
                            opponent.board.board[opponent.x][opponent.y].content['units']
                        self.kill()
                    if opponent.health <= 0:
                        if type(opponent) == City:
                            opponent.player.cit -= 1
                        print(opponent.player.cit)
                        opponent.board.board[opponent.x][opponent.y].content['units'] = \
                            self.board.board[self.x][self.y].content['units']
                        opponent.kill()


class City(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, board, color, player, *group):
        super().__init__(*group)
        self.board = board
        self.color = color
        player.max_pl += 1
        player.cit += 1
        self.player = player
        self.gold_per_move = 5
        self.picture_name = picture
        self.health = 50
        self.damage = 10
        city_icon(self.picture_name, self.color)
        self.orig_image = load_image(self.picture_name.split('.')[0] + '_' + color + '.png',
                                     color_key='black')
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.board.cell_size + self.board.left
        self.rect.y = y * self.board.cell_size + self.board.top
        self.x = x
        self.y = y

        self.able_units = dict()
        self.able_units['Воин'] = True
        self.able_units['Поселенец'] = True
        self.buildings = dict()
        self.buildings['Стены'] = False

        self.board.board[int(x)][int(y)].content['units'] = self

    def create_unit(self, hero, x, y, board, event, rang):
        if self.player.gold > config.PATTERN[hero][0] and type(
                board.get_cell_object(x, y).content.get(
                    'units', None)) == City:
            a = event.pos
            b = board.get_cell(a)
            if (-1 <= x - b[0] <= 1) and (-1 <= y - b[1] <= 1) and (b[0] != 0 and b[1] != 0):
                self.player.gold -= config.PATTERN[hero][0]
                return Heroes(hero, 10, 30, 2, 2, hero + '.png', b[0], b[1], self.color,
                              board, config.PATTERN[hero][0], rang)
        else:
            print('Денег нет')

    def update(self):
        self.image = pygame.transform.scale(self.orig_image.copy(),
                                            (self.board.cell_size, self.board.cell_size))
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top


class Player:
    def __init__(self, color, name, board):
        self.gold = 100
        self.science = 10
        self.color = color
        self.cit = 0
        self.max_pl = 1
        self.name = name
        self.cities = dict()
        if color == 'blue':
            self.x = 15
            self.y = 15
            self.cities['firstTown'] = City(15, 15, 'city.png', board, color, self)
        else:
            self.x = 35
            self.y = 35
            self.cities['firstTown'] = City(35, 35, 'city.png', board, color, self)


class Picture(pygame.sprite.Sprite):
    def __init__(self, name, board, x, y, *group):
        super().__init__(*group)
        self.board = board
        self.name = name
        self.orig_image = load_image(name, color_key='black')
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
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top


class Motion(pygame.sprite.Sprite):
    def __init__(self, name, *group):
        super().__init__(*group)
        self.name = name
        self.orig_image = load_image(name, color_key='black')
        self.image = pygame.transform.scale(self.orig_image.copy(), (150, 130))
        self.rect = self.image.get_rect()
        self.rect.x = 365
        self.rect.y = 385

    def new_motion(self, all_spr, player, player1):
        if config.turn_owner == 0:
            config.turn_owner = 1
        else:
            config.turn_owner = 0
        for i in all_spr:
            if type(i) == Heroes:
                i.power += i.max_power / 2
                i.health += 2.5
            elif type(i) == City:
                if config.turn_owner == 0:
                    player.gold += i.gold_per_move
                else:
                    player1.gold += i.gold_per_move


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Покупка")
        Form.resize(244, 161)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 50, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(60, 110, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 20, 91, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(130, 60, 81, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Воин"))
        self.pushButton_2.setText(_translate("Form", "Поселенец"))
        self.pushButton_3.setText(_translate("Form", "Отмена"))
        self.label.setText(_translate("Form", "10 Золотых"))
        self.label_2.setText(_translate("Form", "20 Золотых"))

    def show_city_messagebox(self):
        choice = QMessageBox.question(self, 'Город', 'Вы хотите основать город?',
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:  # 2
            return True
        elif choice == QMessageBox.No:
            return False


class Example(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run)
        self.pushButton_3.clicked.connect(self.run)

    def closeEvent(self, event):
        event.accept()

    def run(self):
        if self.sender().text() == 'Воин':
            config.change_unit = 'warrior'
            self.close()
        elif self.sender().text() == 'Поселенец':
            config.change_unit = 'settler'
            self.close()
        else:
            self.close()
