import config
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


CHUNKS = {'ocean': [generate_islands],
          'plains': {},
          'deserts': {},
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
PANGEA = [['ocean', 'ocean'], ['ocean', 'ocean']]
