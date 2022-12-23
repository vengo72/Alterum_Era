import pygame
import os

size = window_width, window_height = 800, 800
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class World:
    def __init__(self, *args, **kwargs):
        pass


class Board:
    def __init__(self, width, height, cell_size, *args, **kwargs):
        self.cell_size = cell_size
        self.left = args[0]
        self.top = args[1]
        self.board = [[Cell(x, y, self) for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height

    '''def render(self, scr):
        for i in range(self.width):
            for j in range(self.height):
                self.board[j][i].cell_size = self.cell_size'''

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        a, b = (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        return (a, b) if self.left + (self.cell_size * self.width) >= x >= self.top and self.top + (
                self.cell_size * self.height) >= y >= self.top else None


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, board, terrain='desert',
                 *args,
                 **kwargs):
        super().__init__(cell_group)
        self.x = x
        self.y = y
        self.board = board

        self.terrain = terrain
        picture = self.terrain + '_tile.png'
        self.picture = picture
        self.image = load_image(picture)
        self.image = pygame.transform.scale(self.image,
                                            (self.board.cell_size - 1, self.board.cell_size - 1))

        self.rect = self.image.get_rect()
        self.rect.x = self.x * self.board.cell_size + self.board.left + self.x
        self.rect.y = self.y * self.board.cell_size + self.board.top + self.y

    def update(self):
        self.rect.x = self.x * self.board.cell_size + self.board.left
        self.rect.y = self.y * self.board.cell_size + self.board.top


cell_group = pygame.sprite.Group()
a = Board(10, 10, 50, 10, 10)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Alterum Era')
    size = window_width, window_height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass

        screen.fill((0, 0, 0))

        cell_group.draw(screen)
        pygame.display.flip()
