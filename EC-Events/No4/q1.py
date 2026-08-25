from ec import *


def p1():
    data = parse_lines(1, get_ints)

    acc = 0
    for line in data:
        # print(line)
        visited = set()
        cur = 0
        for i in line:
            nxt = cur - i
            if nxt > 0 and nxt not in visited:
                cur = nxt
            else:
                cur = cur + i
            # print(cur)
            visited.add(cur)
        acc += cur
    return acc

    return


def p2():
    data = parse_lines(2, get_ints)

    acc = 0
    for line in data:
        # print(line)
        visited = set()
        cur = 0
        for i in line:
            nxt = cur - i
            if nxt > 0 and nxt not in visited:
                cur = nxt
            else:
                cur = cur + i
                while cur in visited:
                    cur += 1
            # print(cur)
            visited.add(cur)
        acc += cur
    return acc


def p3():
    data = parse_lines(3, get_ints)

    acc = 0
    for line in data:
        # print(line)
        visited = set()
        max_visited = 0

        direction = False  # false = down, true = up
        blocked_ranges_up = []
        blocked_ranges_down = []
        all_ranges = []
        def current_range():
            if direction:
                return blocked_ranges_up
            else:
                return blocked_ranges_down

        def intersects_any_range(a,b):
            r = current_range()
            for c,d in r:
                if a <= d and c <= b and not ((a > c and b < d) or (a < c and b > d)):
                    return True
            return False

        cur = 0
        for i in line:
            last = cur
            nxt = cur - i
            if nxt > 0 and nxt not in visited and not intersects_any_range(nxt, last):
                cur = nxt
            else:
                cur = cur + i
                while cur in visited:
                    cur += 1
                while cur < (max_visited + i + 1):
                    if intersects_any_range(last, cur):
                        cur += 1
                    else:
                        break
                else:
                    cur = last

            if cur != last:
                max_visited = max(max_visited, cur)
                current_range().append(sorted([last, cur]))
                all_ranges.append([last,cur])

                visited.add(cur)
                direction = not direction

        acc += cur
    return acc


setquest(1)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
