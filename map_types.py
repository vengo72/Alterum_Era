import random


def generate_islands(board, i, j, chance=0.5):
    terrains = board.TERRAINS.copy()
    # terrains.remove('ocean')
    if random.random() > chance:
        num_isl = random.randint(1, 3)
    else:
        num_isl = 0
    for isl in range(num_isl):
        x = random.randint(3, 7)
        y = random.randint(3, 7)
        cell_x = x + j * 10
        cell_y = y + i * 10
        size_chances = [0, 2, 4, 6, 7, 7, 7, 8, 8, 8, 9, 10, 11, 12]
        island_size = random.choice(size_chances)
        board.board[cell_y][cell_x].terrain = random.choice(terrains)
        island_terrain = random.choice(terrains)
        for tile in range(island_size):
            random.choice(board.board[cell_y][cell_x].adjacent()).terrain = board.board[cell_y][
                cell_x].terrain = island_terrain
            if island_size >= 6:
                random.choice(
                    random.choice(board.board[cell_y][cell_x].adjacent()).adjacent()).terrain = \
                    board.board[cell_y][cell_x].terrain = island_terrain


def continent(board, i, j, chance=0.5):
    terrains = board.TERRAINS.copy()
    for y in range(10):
        for x in range(10):
            cell_x = x + j * 10
            cell_y = y + i * 10
            if 0 < cell_x < board.width and 0 < cell_y < board.height:
                cht = random.choice(board.board[cell_y][cell_x].adjacent()).terrain
                board.board[cell_y][cell_x].terrain = cht

        for y in range(10, -1, -1):
            for x in range(10, -1, -1):
                cell_x = x + j * 10
                cell_y = y + i * 10
                if 0 < cell_x < board.width and 0 < cell_y < board.height:
                    cht = random.choice(board.board[cell_y][cell_x].adjacent()).terrain
                    board.board[cell_y][cell_x].terrain = cht


def generate_hills(board, i, j, chance=0.5):
    terrains = board.TERRAINS.copy()
    # terrains.remove('ocean')
    num_isl = random.randint(1, 3)
    for isl in range(num_isl):
        x = random.randint(3, 7)
        y = random.randint(3, 7)
        cell_x = x + j * 10
        cell_y = y + i * 10
        size_chances = [0, 2, 4, 6, 7, 8, 9, 10, 11, 12]
        hill_size = random.choice(size_chances)
        board.board[cell_y][cell_x].terrain = 'plainHill'
        for tile in range(hill_size):
            random.choice(board.board[cell_y][cell_x].adjacent()).terrain = board.board[cell_y][
                cell_x].terrain = 'plainHill'
            if hill_size >= 6:
                random.choice(
                    random.choice(board.board[cell_y][cell_x].adjacent()).adjacent()).terrain = \
                    board.board[cell_y][cell_x].terrain = 'plainHill'


def generate_mountains(board, i, j, chance=0.5):
    terrains = board.TERRAINS.copy()
    # terrains.remove('ocean')
    num_isl = random.randint(1, 3)
    for isl in range(num_isl):
        x = random.randint(3, 7)
        y = random.randint(3, 7)
        cell_x = x + j * 10
        cell_y = y + i * 10
        size_chances = [2, 4, 4]
        hill_size = random.choice(size_chances)
        board.board[cell_y][cell_x].terrain = 'mountain'
        for tile in range(hill_size):
            if hill_size >= 6:
                random.choice(
                    random.choice(board.board[cell_y][cell_x].adjacent()).adjacent()).terrain = \
                    board.board[cell_y][cell_x].terrain = 'mountain'
                continue
            random.choice(board.board[cell_y][cell_x].adjacent()).terrain = board.board[cell_y][
                cell_x].terrain = 'mountain'
    # for y in range(10):
    #     for x in range(10):
    #         cell_x = x + j * 10
    #         cell_y = y + i * 10
    #         if sum([1 if el.terrain == 'mountain' else 0 for el in
    #                 board.board[cell_y][cell_y].adjacent()]) == 4:
    #             print([(el.x, el.y) for el in board.board[cell_y][cell_y].adjacent()])
    #             board.board[cell_y][cell_x].terrain = 'mountain'



CHUNKS = {'ocean': [generate_islands],
          'plain': [continent, generate_hills, generate_mountains],
          'desert': [],
          'tundras': {},
          'hills': {},
          'forests': {},
          'jungles': {}
          }

# ocean: if sum([1 if el.terrain != 'ocean' else 0 for i in board.board[y][x].adjacent()):
#     if VEROJATNOST:
#           board.board[y][x]
# oceans: if VEROJATNOST summon island:
#
PANGEA = [['ocean', 'ocean', 'ocean', 'ocean', 'ocean'],
          ['ocean', 'plain', 'plain', 'plain', 'ocean'],
          ['ocean', 'plain', 'plain', 'plain', 'ocean'],
          ['ocean', 'plain', 'plain', 'plain', 'ocean'],
          ['ocean', 'ocean', 'ocean', 'ocean', 'ocean']]

