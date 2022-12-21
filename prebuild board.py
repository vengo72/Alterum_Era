import pygame


class World:
    def __init__(self, *args, **kwargs):
        pass


class Board:
    def __init__(self, width, height, *args, **kwargs):
        self.board = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height
        self.left = args[0]
        self.top = args[1]
        self.cell_size = args[2]

    def render(self, scr):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(scr, 'white', (
                    (i * self.cell_size), (j * self.cell_size),
                    self.cell_size, self.cell_size), 1)


class Cell:
    def __init__(self, x, y, terrain='plain', *args, **kwargs):
        self.x = x
        self.y = y
        self.terrain = terrain

    def update(self):




a = Board(10, 10, 100, 100, 20)
print(a.board)

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
        screen.fill((0, 0, 0))
        a.render(screen)
        pygame.display.flip()

