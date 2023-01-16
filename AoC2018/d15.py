from aoc import *


class Combatant:
    def __init__(self, type, hp, dmg, pos):
        self.type = type
        self.hp = hp
        self.dmg = dmg
        self.pos = pos

    def __str__(self):
        return f'{self.type}  HP:{self.hp} dmg:{self.dmg} @ {self.pos}'

    def hit(self, dmg):
        self.hp -= dmg
        return self.hp > 0


def get_neighbors(pos, cbt, grid):
    neighbors = {}
    for dir in READING_ORDER:
        n = vadd(pos, dir)
        tile = get_tile(n, cbt, grid)
        if tile == '#':
            continue
        neighbors[n] = tile
    return neighbors


def get_tile(pos, cbt, grid):
    if pos in cbt:
        return cbt[pos]
    else:
        return grid[pos]


def bfs(src, cbt, grid):
    q = deque([src])
    start_type = get_tile(src, cbt, grid).type

    parent = {}

    while q:
        cur = q.popleft()
        c = get_tile(cur, cbt, grid)
        if isinstance(c, Combatant):
            if c.type != start_type:
                break
            elif cur != src:
                continue

        for n in get_neighbors(cur, cbt, grid):
            if n in parent:
                continue

            parent[n] = cur
            q.append(n)
    else:
        return None

    target_candidates = [c for c in parent if c in cbt and c != src and cbt[c].type != start_type]

    # paths_dict = {}
    paths = []
    i = 0
    for tgt in target_candidates:
        i += 1
        pos = tgt
        path = []
        while pos != src:
            path.append(pos)
            pos = parent[pos]
        path.append(src)
        path.reverse()
        paths.append(path)
        # paths_dict.update({k:chr(96+i) for k in path})

    paths = [path for path in paths if len(path) == len(min(paths, key=len))]

    # rev = {(0, -1): 'v', (-1, 0): '>', (1, 0):  '<', (0, 1):  '^'}
    # print_2d('  ', grid, {k:rev[vsub(v,k)] for k,v in parent.items()}, {src:start_type}, {k:'?' for k in target_candidates})
    # print_2d('  ', grid, paths_dict, {src:start_type}, {k:'?' for k in target_candidates})

    # print(paths)
    return sorted(paths, key=lambda x:(x[-1][1], x[-1][0]))[0]


def solve(elf_dmg=3, p2=False):
    board = {pos: (c if c in '.#' else '.') for pos, c in grid.items()}
    combatants = {c: Combatant('G', 200, 3, c) for c in inverse['G']} | \
                 {c: Combatant('E', 200, elf_dmg, c) for c in inverse['E']}
    # print_2d('  ', {k: i for i, (k, v) in enumerate(combatants.items())})
    # print('Initially:')
    # print_2d('. ', board, combatants)
    # print()

    for i in range(200):
        combatants = sorted_dict(combatants, key=lambda x: (x[1], x[0]))
        turn_order = [*combatants]

        for pos in turn_order:
            if pos not in combatants:
                continue

            combatant = combatants[pos]

            # check for adjacent targets
            neighbors = get_neighbors(pos, combatants, board)
            neighbors = {k: v for k, v in neighbors.items() if isinstance(v, Combatant) and combatant.type != v.type}

            # move
            if not neighbors:
                path = bfs(pos, combatants, board)
                if path is None:
                    continue

                # print_2d('  ', board, {k: '~' for k in path}, combatants)
                next_tile = path[1]
                combatant.pos = next_tile
                combatants[next_tile] = combatant
                del combatants[pos]

                # recheck for adjacent targets
                neighbors = get_neighbors(next_tile, combatants, board)
                neighbors = {k: v for k, v in neighbors.items() if isinstance(v, Combatant) and combatant.type != v.type}

            # attack
            if neighbors:
                neighbors = sorted([combatants[c] for c in neighbors], key=lambda x: x.hp)
                target = neighbors[0]

                alive = target.hit(combatant.dmg)
                if not alive:
                    del combatants[target.pos]

                    if p2 and target.type == 'E':
                        return None
                    elif len(set(c.type for c in combatants.values())) == 1:
                        return (i + (1 if pos == turn_order[-1] else 0)) * sum(c.hp for c in combatants.values())

        # print(f'After {i} round{"s" if i > 1 else ""}:')
        # print_2d('. ', board, combatants)
        # print([str(c) for c in combatants.values()], '\n')


def p2():
    i = 3
    while True:
        i += 1
        result = solve(i, True)
        if result:
            return result


setday(15)

READING_ORDER = [(0, -1), (-1, 0), (1, 0), (0, 1)]

grid, inverse, unique = parsegrid()

print('part1:', solve())
print('part2:', p2())
