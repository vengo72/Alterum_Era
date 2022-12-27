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
    def __init__(self, width, height, cell_size, top=10, left=10, *args, **kwargs):
        self.cell_size = cell_size
        self.left = left
        self.top = top
        self.board = [[Cell(x, y, self) for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height
        '''self.TERRAINS =
        self.tiles_images = {'desert' : self.image}

        picture = self.terrain + '_tile.png'
        self.picture_name = picture
        self.image_original = load_image(picture)
        self.image = pygame.transform.scale(self.image_original,
                                            (self.board.cell_size - 1, self.board.cell_size - 1))'''

    '''def render(self, scr):
        for i in range(self.width):
            for j in range(self.height):
                self.board[j][i].cell_size = self.cell_size'''

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        a, b = (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        print(a, b)
        return (a, b) if self.left + (self.cell_size * self.width) >= x >= self.top and self.top + (
                self.cell_size * self.height) >= y >= self.top else None

    def zoom_to_center(self, diff):
        center_x, center_y = self.get_cell((window_width // 2, window_height // 2))
        x_from_cell = window_width // 2 - center_x * self.cell_size - self.left
        y_from_cell = window_height // 2 - center_y * self.cell_size - self.top

        self.left = window_width // 2 - center_x * (self.cell_size + diff) - x_from_cell
        self.top = window_height // 2 - center_y * (self.cell_size + diff) - y_from_cell


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
        self.picture_name = picture
        self.image_original = load_image(picture)
        self.image = pygame.transform.scale(self.image_original,
                                            (self.board.cell_size - 1, self.board.cell_size - 1))

        self.rect = self.image.get_rect()
        self.rect.x = self.x * self.board.cell_size + self.board.left + self.x
        self.rect.y = self.y * self.board.cell_size + self.board.top + self.y

    def update(self):
        self.rect.x = self.x * self.board.cell_size + self.board.left + self.x
        self.rect.y = self.y * self.board.cell_size + self.board.top + self.y
        self.image = pygame.transform.scale(self.image_original,
                                            (self.board.cell_size - 1, self.board.cell_size - 1))


cell_group = pygame.sprite.Group()
cursor_sprite = pygame.sprite.Sprite()
cursor_sprite.rect = (pygame.Rect(0, 0, 1, 1))
print(cursor_sprite.rect)
a = Board(30, 30, 50, 10, 10)

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
                    print(a.get_cell(event.pos))
            if event.type == pygame.MOUSEWHEEL:
                a.zoom_to_center(event.y)
                a.cell_size += event.y

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            a.left += 50 // (a.cell_size ** 0.5) + 1
        elif keys[pygame.K_RIGHT]:
            a.left -= 50 // (a.cell_size ** 0.5) + 1
        elif keys[pygame.K_UP]:
            a.top += 50 // (a.cell_size ** 0.5) + 1
        elif keys[pygame.K_DOWN]:
            a.top -= 50 // (a.cell_size ** 0.5) + 1

        screen.fill((0, 0, 0))
        cell_group.update()
        cell_group.draw(screen)
        pygame.display.flip()
