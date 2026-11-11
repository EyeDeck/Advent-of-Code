from ec import *


def p1():
    grid, inverse, unique = parse_grid(1)

    magma = set(inverse['#'])
    acc = 0
    while magma:
        frontier = {magma.pop(),}
        group = set()
        while frontier:
            cur = frontier.pop()
            group.add(cur)
            neighbors = [vadd(d, cur) for d in DIRS]
            neighbors = [p for p in neighbors if p in magma]
            for p in neighbors:
                magma.remove(p)
                frontier.add(p)
        min_x, max_x = min(group, key=lambda x: x[0])[0], max(group, key=lambda x: x[0])[0]
        min_y, max_y = min(group, key=lambda x: x[1])[1], max(group, key=lambda x: x[1])[1]
        norm_x, norm_y = max_x - min_x + 1, max_y - min_y + 1
        min_spells = min(norm_x, norm_y)
        # print_2d(' ', {k:'#' for k in magma}, {k:'~' for k in group})
        print(f'({min_x}, {min_y}) to ({max_x}, {max_y}) normalized ({norm_x}x{norm_y}) {min_spells}')
        acc += min_spells

    return acc


def p2():
    grid, inverse, unique = parse_grid(2)

    magma = set(inverse['#'])
    acc = 0
    while magma:
        frontier = {magma.pop(),}
        group = set()
        while frontier:
            cur = frontier.pop()
            group.add(cur)
            neighbors = [vadd(d, cur) for d in DIRS]
            neighbors = [p for p in neighbors if p in magma]
            for p in neighbors:
                magma.remove(p)
                frontier.add(p)
        min_x, max_x = min(group, key=lambda x: x[0])[0], max(group, key=lambda x: x[0])[0]
        min_y, max_y = min(group, key=lambda x: x[1])[1], max(group, key=lambda x: x[1])[1]
        norm_x, norm_y = max_x - min_x + 1, max_y - min_y + 1
        if len(group) == norm_x*norm_y:
            min_spells = min(norm_x, norm_y)
            acc += min_spells
            print(f'Full: ({min_x}, {min_y}) to ({max_x}, {max_y}) normalized ({norm_x}x{norm_y}) {min_spells}')
            # print_2d(' ', {k:'#' for k in magma}, {k:'~' for k in group})
        else:
            corners = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
            missing_corner = [p for p in corners if p not in group][0]
            missing_index = corners.index(missing_corner)
            opposite_corners = (corners[(missing_index-1)%4],corners[(missing_index+1)%4])
            opposite_missing_corner = [p for p in corners if p != missing_corner and p not in opposite_corners][0]
            print(f'L: missing_corner {missing_corner}, opposite_corners {opposite_corners}, opposite_missing_corner {opposite_missing_corner}')

            print_2d(' ', {k: '#' for k in magma}, {k: '~' for k in group}, {k: '*' for k in bresenham(opposite_corners[0], opposite_corners[1])})

            rect_a_a = bresenham(opposite_corners[0], missing_corner)
            rect_a_b = bresenham(opposite_corners[0], opposite_missing_corner)

            rect_b_a = bresenham(opposite_corners[1], missing_corner)
            rect_b_b = bresenham(opposite_corners[1], opposite_missing_corner)

            rect_a_a_ct = len([p for p in rect_a_a if p in group])
            rect_a_b_ct = len([p for p in rect_a_b if p in group])
            rect_b_a_ct = len([p for p in rect_b_a if p in group])
            rect_b_b_ct = len([p for p in rect_b_b if p in group])

            print(rect_a_a_ct, rect_a_b_ct, rect_b_a_ct, rect_b_b_ct)

            min_as_arms = min(rect_a_a_ct, rect_a_b_ct) + min(rect_b_a_ct, rect_b_b_ct)
            min_whole = min(norm_x, norm_y)

            acc += min(min_as_arms, min_whole)

            # oh my god

    return acc

# does it work to just take out chunks at random?
def p3():
    grid, inverse, unique = parse_grid(3)
    magma = set(inverse['#'])

    acc = 0
    while magma:
        start = magma.pop()
        magma.add(start)

        group = {start,}
        while True:
            start_len = len(group)
            for d in DIRS:
                try_group = group | set(vadd(p, d) for p in group)
                if try_group <= magma:
                    group = try_group
                    print('expanded', d, group)
            if start_len == len(group):
                break
        print(group)
        min_x, max_x = min(group, key=lambda x: x[0])[0], max(group, key=lambda x: x[0])[0]
        min_y, max_y = min(group, key=lambda x: x[1])[1], max(group, key=lambda x: x[1])[1]
        norm_x, norm_y = max_x - min_x + 1, max_y - min_y + 1

        acc += min(norm_x, norm_y)
        magma -= group

        print_2d(' ', {k: '#' for k in magma}, {k: '~' for k in group})

    return acc
# no

# maybe a little bfs broot on each stack?
def p3():
    grid, inverse, unique = parse_grid(3)

    magma = set(inverse['#'])
    acc = 0
    while magma:
        frontier = {magma.pop(),}
        stack = set()
        while frontier:
            cur = frontier.pop()
            stack.add(cur)
            neighbors = [vadd(d, cur) for d in DIRS]
            neighbors = [p for p in neighbors if p in magma]
            for p in neighbors:
                magma.remove(p)
                frontier.add(p)

        print('stack:', stack)

        best_for_state = defaultdict(lambda: INF)
        queue = deque([[0, stack]])
        while queue:
            # print('queue:', queue)
            moves, state = queue.popleft()

            if not state:
                print('state is empty', moves)
                acc += moves
                break

            # a little queue dedupe to make this run like 500x faster
            as_frozenset = frozenset(state)
            if best_for_state[as_frozenset] <= moves:
                continue
            best_for_state[as_frozenset] = moves

            point = sorted(sorted(state, key=lambda x: x[1]), key=lambda x: x[0])[0]
            # print('point:', point)

            exp_h = point
            h_set = {point, }
            while (exp_h := vadd(exp_h, (1,0))) in state:
                h_set.add(exp_h)
            while (exp_h := vadd(exp_h, (-1,0))) in state:
                h_set.add(exp_h)
            queue.append([moves + 1, state - h_set])

            exp_v = point
            v_set = {point, }
            while (exp_v := vadd(exp_v, (0,1))) in state:
                v_set.add(exp_v)
            while (exp_v := vadd(exp_v, (0,-1))) in state:
                v_set.add(exp_v)
            queue.append([moves + 1, state - v_set])
    return acc
# wow it works


if __name__ == '__main__':
    setquest(12)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
