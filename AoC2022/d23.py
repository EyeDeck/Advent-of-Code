import sys
from collections import *
from aoc import *

dirs = {
    'E': (1, 0),
    'NE': (1, -1),
    'N': (0, -1),
    'NW': (-1, -1),
    'W': (-1, 0),
    'SW': (-1, 1),
    'S': (0, 1),
    'SE': (1, 1),
}


def get_neighbors(b, c):
    neighbors = set()
    for dir, offset in dirs.items():
        x = vadd(c, offset)
        if x in b and b[x] == '#':
            neighbors.add(dir)
    return neighbors


def solve(p2=False, offsets=None):
    proposal_order = [
        lambda neighbors: (not {'N', 'NE', 'NW'}.intersection(neighbors),
                           lambda proposals, coord: proposals[vadd(dirs['N'], coord)].append(coord)),
        lambda neighbors: (not {'S', 'SE', 'SW'}.intersection(neighbors),
                           lambda proposals, coord: proposals[vadd(dirs['S'], coord)].append(coord)),
        lambda neighbors: (not {'W', 'NW', 'SW'}.intersection(neighbors),
                           lambda proposals, coord: proposals[vadd(dirs['W'], coord)].append(coord)),
        lambda neighbors: (not {'E', 'NE', 'SE'}.intersection(neighbors),
                           lambda proposals, coord: proposals[vadd(dirs['E'], coord)].append(coord)),
    ]

    board = data.copy()
    # print_2d('. ', board)

    for round_id in range(1, 1000001 if p2 else 11):
        proposals = defaultdict(list)
        for coord, c in board.items():
            if c == '.':
                continue

            neighbors = get_neighbors(board, coord)

            if not neighbors:
                continue

            for proposal in proposal_order:
                result, op = proposal(neighbors)
                if result:
                    op(proposals, coord)
                    break

        if p2 and not proposals:
            # gather image size before re-running
            if RENDER:
                bounds = min(board, key=itemgetter(0))[0], min(board, key=itemgetter(1))[1], \
                         max(board, key=itemgetter(0))[0], max(board, key=itemgetter(1))[1]
                return bounds + (round_id - 1,)
            return round_id

        next_board = {}
        for coord, ls in proposals.items():
            if len(ls) == 1:
                next_board[coord] = '#'
                del board[ls[0]]

        next_board.update(board)

        proposal_order.append(proposal_order.pop(0))

        board = next_board

        # print(f'==End of Round {round_id+1} ==')
        # print_2d('.', {(0, 0): 0}, next_board)

        if RENDER and offsets:
            print(f'Rendering frame {round_id}/{offsets[4]}...', end='\r')
            img_size = -(offsets[0] - offsets[2]) + 1, -(offsets[1] - offsets[3]) + 1
            img = Image.new('RGB', img_size, BG_COLOR)
            for x, y in board.keys():
                img.putpixel((x - offsets[0], y - offsets[1]), ELF_COLOR)

            scaled_img = img.resize((img_size[0] * 6, img_size[1] * 6), 0)
            scaled_img.save(f'{PATH}\\{str(round_id).zfill(5)}.png')

    bounds = min(board, key=itemgetter(0))[0], min(board, key=itemgetter(1))[1], \
             max(board, key=itemgetter(0))[0], max(board, key=itemgetter(1))[1]
    area = (bounds[2] + 1 - bounds[0]) * (bounds[3] + 1 - bounds[1])
    return area - len(board)


day = 23
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

data = {}
with open(f) as file:
    for y, line in enumerate(file.readlines()):
        for x, c in enumerate(line.strip()):
            if c != '#':
                continue
            data[x, y] = c

RENDER = '-r' in sys.argv or '--render' in sys.argv
if RENDER:
    import os
    from PIL import ImageColor, Image

    BG_COLOR = ImageColor.getcolor('#282828', 'RGB')
    ELF_COLOR = ImageColor.getcolor('#41D800', 'RGB')

    PATH = 'media\\d23'
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    print('Running once to calculate image size...')
    offsets = solve(True)
    print('Bounds calculated as', offsets)
    solve(True, offsets)
    print('\nDone!')
else:
    print('part1:', solve())
    print('part2:', solve(True))
