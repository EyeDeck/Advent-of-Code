from aoc import *


def p1(beams=None):
    if beams is None:
        beams = [(0, 0, 0)]

    history = set()

    mirrors = {
        '/':  {0: (1,  ), 1: (0,  ), 2: (3,  ), 3: (2,  )},
        '\\': {0: (3,  ), 1: (2,  ), 2: (1,  ), 3: (0,  )},
        '|':  {0: (1, 3), 2: (1, 3)},
        '-':  {1: (0, 2), 3: (0, 2)}
    }

    if RENDER:
        bounds = grid_bounds(grid)
        mirror_grid = {k:v for k,v in grid.items() if v != '.'}

    i = 0
    while beams:
        new_beams = []
        for beam in beams:
            if beam in history:
                continue
            history.add(beam)

            coord = beam[:2]
            heading = beam[-1]
            tile = grid[coord]

            next_coords = []
            if tile in mirrors and heading in mirrors[tile]:
                for new_heading in mirrors[tile][heading]:
                    next_coords.append(vadd(coord, DIRS[new_heading]) + (new_heading,))
            else:
                next_coords.append(vadd(coord,DIRS[heading]) + (heading,))

            for c in next_coords:
                if c[:2] in grid:
                    new_beams.append(c)

        if RENDER:
            i += 1
            render(history, mirror_grid, beams, bounds, i)

        # print_2d('. ', {k:v for k,v in grid.items() if v != '.'}, {k[:2]: dirs[k[-1]] for k in beams})

        beams = new_beams

    flattened = set(k[:2] for k in history)
    # print_2d('.', grid, {k[:2]:'#' for k in flattened})
    return len(flattened)


def p2():
    global RENDER

    highest = (0, 0)
    bounds = grid_bounds(grid)

    edges = [(x,bounds[1],3) for x in range(bounds[0], bounds[2]+1)] + \
            [(x,bounds[3],1) for x in range(bounds[0], bounds[2]+1)] + \
            [(bounds[0],y,0) for y in range(bounds[1], bounds[3]+1)] + \
            [(bounds[2],y,2) for y in range(bounds[1], bounds[3]+1)]

    render_flag = RENDER
    if render_flag:
        RENDER = False

    for start in edges:
        result = p1([start])
        if result > highest[0]:
            highest = (result, start)

    if render_flag:
        RENDER = True
        p1([highest[1]])

    return highest[0]


setday(16)

grid, inverse, unique = parsegrid()

dirs = ['>', '^', '<', 'v']

RENDER = '-r' in sys.argv or '--render' in sys.argv
if RENDER:
    import os
    from PIL import ImageColor, Image

    PATH = 'media\\d16-p1'
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    colors = {
        'BG': ImageColor.getcolor('#101010', 'RGB'),
        'F': ImageColor.getcolor('#FFFF80', 'RGB'),
        '5': ImageColor.getcolor('#99994E', 'RGB'),
    }

    sprites = {
        '~': ('555', '555', '555'),

        '/': ('  9', ' 9 ', '9  '),
        '\\': ('9  ', ' 9 ', '  9'),
        '|': (' 9 ', ' 9 ', ' 9 '),
        '-': ('   ', '999', '   '),

        '>': ('FF ', '  F', 'FF '),
        '^': (' F ', 'F F', 'F F'),
        '<': (' FF', 'F  ', ' FF'),
        'v': ('F F', 'F F', ' F '),
    }


    def draw_sprite(canvas, coord, sprite):
        for y, line in enumerate(sprites[sprite]):
            for x, char in enumerate(line):
                if char == ' ':
                    continue
                if char not in colors:
                    colors[char] = ImageColor.getcolor('#' + char * 6, 'RGB')
                c = vadd(vmul(coord, (3, 3)), (x, y))
                # print(coord, vmul(coord, (3, 3)), (x, y), c)
                canvas.putpixel(c, colors[char])


    def render(history, mirrors, beams, bounds, n):
        print('rendering frame', n, end='\r')

        canvas = Image.new('RGB', ((bounds[2] + 1) * 3, (bounds[3] + 1) * 3), colors['BG'])

        for coord in history:
            draw_sprite(canvas, coord, '~')

        for coord, mirror in mirrors.items():
            draw_sprite(canvas, coord, mirror)

        for beam in beams:
            draw_sprite(canvas, beam[:2], dirs[beam[-1]])

        # canvas.show()
        canvas.save(f'{PATH}\\{str(n).zfill(5)}.png')

print('part1:', p1())

if RENDER:
    PATH = 'media\\d16-p2'
    if not os.path.exists(PATH):
        os.makedirs(PATH)

print('part2:', p2() )
