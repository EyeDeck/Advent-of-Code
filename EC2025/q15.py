from ec import *




def p1():
    data = parse_lines(1)[0].split(',')
    board = set()
    heading = 1
    start = (0, 0)
    pos = start
    for ins in data:
        d, n = ins[0], ins[1:]
        # print(ins, d, n)
        n = int(n)
        heading = (heading + (-1 if d == 'R' else 1)) % 4
        for i in range(n):
            pos = vadd(pos, DIRS[heading])
            board.add(pos)
        # print_2d(' ', {k:'#' for k in board})
        # print(heading)

    board.remove(pos)

    def get_neighbors(pos):
        neighbors = []
        for d in DIRS:
            # print(pos, d)
            n = vadd(pos, d)
            if n not in board:
                neighbors.append((n,1))
        return neighbors

    return len(wbfs(start, pos, get_neighbors))-1



def p2():
    data = parse_lines(2)[0].split(',')
    board = set()
    heading = 1
    start = (0, 0)
    pos = start
    for ins in data:
        d, n = ins[0], ins[1:]
        # print(ins, d, n)
        n = int(n)
        heading = (heading + (-1 if d == 'R' else 1)) % 4
        for i in range(n):
            pos = vadd(pos, DIRS[heading])
            board.add(pos)

        # print(heading)

    board.remove(pos)

    def get_neighbors(pos):
        neighbors = []
        for d in DIRS:
            # print(pos, d)
            n = vadd(pos, d)
            if n not in board:
                neighbors.append((n,1))
        return neighbors

    result = wbfs(start, pos, get_neighbors)
    print_2d(' ', {k:'#' for k in board}, {k:'.' for k in result}, {start:'S', pos:'E'}, constrain=(-512, -512, 512, 512))

    return len(wbfs(start, pos, get_neighbors))-1


def solve(input_n):
    diags = [(1,1), (1,-1), (-1,1), (-1,-1)]
    data = parse_lines(input_n)[0].split(',')
    v_segs = []
    h_segs = []
    heading = 1
    start = (0, 0)
    pos = start
    end = None

    important_points = set()

    for i, ins in enumerate(data):
        d, n = ins[0], ins[1:]
        n = int(n)
        heading = (heading + (-1 if d == 'R' else 1)) % 4
        dest = v_segs if heading & 1 else h_segs
        next_end = vadd(pos, vmul(DIRS[heading], (n,n)))

        # important: trim beginning and end line segments 1 short, to avoid interfering with intersection code
        if i == 0:
            pos = vadd(pos, DIRS[heading])
            # for orth in DIRS:
            #     if orth == pos:
            #         continue
            #     important_points.add(orth)
            #     print('adding', orth)
        if i == len(data)-1:
            end = next_end
            print('end set to', end)
            next_end = vsub(next_end, DIRS[heading])
            pass

        dest.append(sorted((pos, next_end)))
        pos = next_end
        important_points.update(vadd(p,o) for p in (pos, next_end) for o in diags)

    important_points.add(end)

    print(v_segs)
    print(h_segs)

    # some_point = important_points.pop()
    # important_points.add(some_point)

    def check_intersection(seg_a, seg_b):
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


    @memo
    def get_neighbors(n_pos):
        # print('getting neighbors of', n_pos)
        neighbors = []
        x1,y1 = n_pos
        for point in important_points:
            # print(f'\tchecking to {point}')
            if n_pos == point:
                continue

            x2, y2 = point
            segment = (n_pos, point)
            if x1 == x2:
                # on the same vertical column, only check collisions with horizontal segments
                for h_seg in h_segs:
                    # print('checking intersection of', segment , 'and', h_seg,  check_intersection(segment, h_seg))
                    if check_intersection(segment, h_seg):
                        break
                else:
                    neighbors.append((point, vdistm(n_pos, point)))
                    # print(f'\t\t{n_pos} orth with {point} and has LOS')
            elif y1 == y2:
                # on the same horizontal row, only check collisions with vertical segments
                for v_seg in v_segs:
                    if check_intersection(segment, v_seg):
                        break
                else:
                    neighbors.append((point, vdistm(n_pos, point)))
                    # print(f'\t\t{n_pos} orth with {point} and has LOS')
            else:
                # not in line, so need to make both right angles (|_ and ``|) and check if either is clear
                midpoints = [(n_pos[0], point[1]), (point[0], n_pos[1])]
                # print('\tchecking Ls with midpoints:', midpoints)
                for midpoint in midpoints:
                    seg_a = (n_pos, midpoint)
                    if seg_a[0][1] == seg_a[1][1]:
                        wall_group = v_segs
                    else:
                        wall_group = h_segs
                    collides = True
                    for seg in wall_group:
                        if check_intersection(seg_a, seg):
                            break
                    else:
                        collides = False

                    if collides:
                        continue

                    seg_b = (midpoint, point)
                    if seg_b[0][1] == seg_b[1][1]:
                        wall_group = v_segs
                    else:
                        wall_group = h_segs
                    collides = True
                    for seg in wall_group:
                        if check_intersection(seg_b, seg):
                            break
                    else:
                        collides = False

                    if collides:
                        continue

                    # print('seg_a, seg_b', seg_a, seg_b)
                    # print(f'\t\topen path from {n_pos} to {midpoint} to {point}!')
                    neighbors.append((point, vdistm(n_pos, point)))
                    break

        # print('\tReturning', neighbors)
        # input()
        return neighbors

    # print(len(important_points), ' n of', some_point, '=', get_neighbors(some_point))

    v = False
    if v:
        board = set()
        for (x1,y1),(x2,y2) in v_segs:
            for y in range(y1, y2+1):
                board.add((x1,y))
        for (x1,y1),(x2,y2) in h_segs:
            for x in range(x1, x2+1):
                board.add((x,y1))
        # print_2d(' ', {k: 'x' for k in important_points}, {k: '#' for k in board}) #, {start: 'S', end: 'E'}, constrain=(-512, -512, 512, 512))
        # print_2d(' ', {k: '#' for k in board}) # , {start: 'S', end: 'E'}, constrain=(-512, -512, 512, 512))

        # print(heading)

    # for point in important_points:
    #     print(f'checking {point}:')
    #     n = get_neighbors(point)
    #     if not n:
    #         print('no neighbors')
    #         continue
    #     print_2d(' ', {k: '#' for k in board}, {point:'+'}, {k[0]: 'x' for k in n}, ) #, {start: 'S', end: 'E'}, constrain=(-512, -512, 512, 512))
    #     # input()


    result = wbfs(start, end, get_neighbors)
    # print_2d(' ', {k:'#' for k in board}, {start:'S', end:'E'}, {k:'.' for k in result}, constrain=(-512, -512, 512, 512))

    print(result)
    return sum(vdistm(result[i],result[i+1]) for i in range(len(result)-1))



setquest(15)

print('part1:', p1())
print('part2:', p2())
print('part3:', solve(3))
