import config

CHUNKS = {'oceans': {},
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
PANGEA = [['plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain',
           'plain'],
          ['desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert',
           'desert'],
          ['plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain',
           'plain'],
          ['desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert',
           'desert'],
          ['plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain',
           'plain'],
          ['desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert',
           'desert'],
          ['plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain',
           'plain'],
          ['desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert',
           'desert'],
          ['plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain', 'plain',
           'plain'],
          ['desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert', 'desert',
           'desert'],
          ]
