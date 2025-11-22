from ec import *


def check_intersection(seg_a, seg_b):
    """checks whether 2 orthogonal integer line segments intersect"""
    (x1, y1), (x2, y2) = seg_a
    (x3, y3), (x4, y4) = seg_b

    if y1 == y2:
        # seg_a horizontal
        hx1, hx2 = sorted((x1, x2))
        hy = y1
        vx = x3
        vy1, vy2 = sorted((y3, y4))
    else:
        # seg_a vertical
        vx = x1
        vy1, vy2 = sorted((y1, y2))
        hx1, hx2 = sorted((x3, x4))
        hy = y3

    return (hx1 <= vx <= hx2) and (vy1 <= hy <= vy2)


def solve(input_n):
    data = parse_lines(input_n)[0].split(',')

    v_segs = []
    h_segs = []

    diags = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    heading = 1
    start = (0, 0)
    end = None

    pos = start

    important_points = set()

    for i, ins in enumerate(data):
        d, n = ins[0], ins[1:]
        n = int(n)
        heading = (heading + (-1 if d == 'R' else 1)) % 4
        dest = v_segs if heading & 1 else h_segs
        next_end = vadd(pos, vmul(DIRS[heading], (n, n)))

        # important: trim beginning and end line segments 1 short, to avoid interfering with intersection code
        if i == 0:
            pos = vadd(pos, DIRS[heading])
        elif i == len(data) - 1:
            end = next_end
            next_end = vsub(next_end, DIRS[heading])

        dest.append(sorted((pos, next_end)))
        pos = next_end
        important_points.update(vadd(p, o) for p in (pos, next_end) for o in diags)

    important_points.add(end)

    # decent speedup if segments are sorted by wall length
    wall_length = lambda c: vdistm(*c)
    v_segs.sort(key=wall_length, reverse=True)
    h_segs.sort(key=wall_length, reverse=True)

    def get_neighbors(n_pos):
        neighbors = []

        # we want to find every other marked point that can be reached with any orthogonal movement + a right-angle turn
        for point in important_points:
            if n_pos == point:
                continue

            # so create the point that completes both possible right angle turns e.g. └ and ┐
            for midpoint in (n_pos[0], point[1]), (point[0], n_pos[1]):
                # then turn them into line segments, so we can check them against vertical or horizontal wall groups
                for path_seg in (n_pos, midpoint), (midpoint, point):
                    # determine each segment is horizontal or vertical
                    if path_seg[0][1] == path_seg[1][1]:
                        wall_group = v_segs
                    else:
                        wall_group = h_segs

                    # now check if it collides with any orthogonal wall segment
                    collides = True
                    for wall_seg in wall_group:
                        if check_intersection(path_seg, wall_seg):
                            break
                    else:
                        collides = False

                    if collides:
                        break
                else:
                    neighbors.append((point, vdistm(n_pos, point)))
                    break

        return neighbors

    result = wbfs(start, end, get_neighbors)

    return sum(vdistm(result[i], result[i + 1]) for i in range(len(result) - 1))


setquest(15)

print('part1:', solve(1))
print('part2:', solve(2))
print('part3:', solve(3))


