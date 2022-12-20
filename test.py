import pygame
import os


def upd():
    screen.fill(pygame.Color("black"))
    board.render(screen)
    all_sprites.draw(screen)
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


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tester = dict()
        self.tester['city'] = 'None'
        self.tester['place'] = 'random'
        self.tester['units'] = 'None None'
        self.board = [[]]
        for i in range(height):
            for j in range(width):
                self.board[i].append(self.tester.copy())
            self.board.append([])
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x = j * self.cell_size + self.left
                y = i * self.cell_size + self.top
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)


def unit_click(x, y):
    if (10 < x < 510) and (10 < y < 510):
        s = x - 10
        s = s // board.cell_size
        t = y - 10
        t = t // board.cell_size
        if 0 <= s < board.width and 0 <= t < board.height:
            if board.board[s][t]['units'] != 'None None':
                return board.board[s][t]['units']


class Heroes(pygame.sprite.Sprite):
    def __init__(self, name, damage, health, power, speed, picture, x, y, color,  *group):
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

        self.image = load_image(picture)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x * board.cell_size + 10
        self.rect.y = y * board.cell_size + 10
        self.x = x
        self.y = y

        if board.board[x][y]['units'] == 'None None':
            board.board[x][y]['units'] = self

    def update(self, x, y):
        s = x - 10
        s = s // board.cell_size
        g = 10 + board.cell_size * s
        t = y - 10
        t = t // board.cell_size
        w = 10 + board.cell_size * t

        s1 = self.rect.x
        s1 = s1 // board.cell_size
        g1 = 10 + board.cell_size * s1
        t1 = self.rect.y
        t1 = t1 // board.cell_size
        w1 = 10 + board.cell_size * t1
        while g1 != g or w1 != w:
                g1 = self.rect.x
                w1 = self.rect.y
                if g > self.rect.x:
                    self.rect.x += 1
                if w > self.rect.y:
                    self.rect.y += 1
                if g < self.rect.x:
                    self.rect.x -= 1
                if w < self.rect.y:
                    self.rect.y -= 1
                upd()

        self.flag = False
        self.flag2 = False
        board.board[s1][t1]['units'] = 'None None'
        board.board[s][t]['units'] = self


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    # создадим спрайт
    sprite = pygame.sprite.Sprite()
    plaer_color = 'red'
    size = width, height = 520, 520
    screen = pygame.display.set_mode(size)
    board = Board(10, 10)
    board.render(screen)
    warrior = Heroes('warrior', 10, 30, 0, 3, 'warrior.png', 0, 0, 'red')
    warrior1 = Heroes('warrior1', 10, 30, 0, 3, 'warrior.png', 2, 1, 'red')
    screen.fill(pygame.Color("black"))
    all_sprites.add(warrior)
    all_sprites.add(warrior1)
    running = True
    f = 0
    unit = warrior
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                f = event.pos
                if (10 < f[0] < 510) and (10 < f[1] < 510):
                    un = unit_click(f[0], f[1])
                    if not un and unit:
                        unit.flag = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                f = event.pos
                unit = unit_click(f[0], f[1])
                if unit:
                    unit.flag2 = True
                    unit.flag = False
                    unit.old_x = f[0]
                    unit.old_y = f[1]
        if unit:
            if unit.flag and unit.flag2:
                unit.update(f[0], f[1])
        upd()
    pygame.quit()
