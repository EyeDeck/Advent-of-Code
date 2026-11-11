from ec import *


def solve(part):
    grid, inverse, unique = parse_grid(part)

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

        best_for_state = defaultdict(lambda: INF)
        queue = deque([[0, frozenset(stack)]])
        while queue:
            moves, state = queue.popleft()

            if not state:
                acc += moves
                break

            # a little queue dedupe to make this run like 500x faster
            if best_for_state[state] <= moves:
                continue
            best_for_state[state] = moves

            point = min(state, key=lambda x: x[0]+x[1])

            for exp_dir in [(1,0), (0,1)]:
                exp = point
                line_set = {point, }
                while (exp := vadd(exp, exp_dir)) in state:
                    line_set.add(exp)
                queue.append([moves + 1, frozenset(state - line_set)])

    return acc


if __name__ == '__main__':
    setquest(12)

    print('part1:', solve(1))
    print('part2:', solve(2))
    print('part3:', solve(3))
