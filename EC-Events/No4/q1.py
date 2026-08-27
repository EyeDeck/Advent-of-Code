from ec import *

def solve(part):
    data = parse_lines(part, get_ints)

    acc = 0
    for line in data:
        visited = set()
        max_visited = 0

        direction = False  # false = down, true = up
        connections_up = []
        connections_down = []
        connections_all = []
        def get_current_connections():
            if direction:
                return connections_up
            else:
                return connections_down

        def intersects_any_connection(a,b):
            r = get_current_connections()
            for c,d in r:
                # if ranges overlap, and one isn't wholly inside the other
                if a <= d and c <= b and not ((a > c and b < d) or (a < c and b > d)):
                    return True
            return False

        cur = 0
        for i in line:
            last = cur
            nxt = cur - i
            if nxt > 0 and nxt not in visited and (part <= 2 or not intersects_any_connection(nxt, last)):
                cur = nxt
            else:
                nxt = cur + i
                if part >= 2:
                    while nxt in visited:
                        nxt += 1
                if part >= 3:
                    while nxt < (max_visited + i + 1):  # heuristic derived empirically, not sure why this works
                        if intersects_any_connection(last, nxt):
                            nxt += 1
                        else:
                            break
                    else:
                        continue
                cur = nxt

            max_visited = max(max_visited, cur)
            get_current_connections().append(sorted([last, cur]))
            connections_all.append([last,cur])


            visited.add(cur)
            direction = not direction

        print(connections_all)
        acc += cur
    return acc


setquest(1)

print('part1:', solve(1))
print('part2:', solve(2))
print('part3:', solve(3))
