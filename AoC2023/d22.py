import copy
from aoc import *

def p1():
    bricks = {}
    points = {}
    for i, line in enumerate(data):
        # i = chr(i+65)
        a,b = line.split('~')
        a_x, a_y, a_z = [int(n) for n in a.split(',')]
        b_x, b_y, b_z = [int(n) for n in b.split(',')]
        brick = []
        for x in range(a_x, b_x+1):
            for y in range(a_y, b_y+1):
                for z in range(a_z, b_z+1):
                    point = (x,y,z)
                    brick.append(point)
                    points[point] = i
        bricks[i] = brick
        # print(bricks)

    def try_settle(brick):
        brick_points = bricks[brick]
        # print(id, brick_points)
        for point in brick_points:
            below = vsub(point, (0,0,1))
            if below in points and points[below] != brick:
                # print('on something')
                return -1 if points[below] in settled else 0
            if below[2] == 0:
                # print('hit floor')
                return -1
        else:
            # print('aaaa')
            new_points = {vsub(point, (0,0,1)) for point in brick_points}
            new_brick = [*new_points]
            # print(new_brick)
            # input()
            for point in brick_points:
                del points[point]
            for point in new_points:
                points[point] = brick
            bricks[brick] = new_brick
            return 1

    unsettled = deque(bricks.keys())
    settled = set()
    i = 0
    while unsettled:
        i += 1
        # print('unsettled', unsettled)
        # print(i)
        brick = unsettled.pop()
        result = try_settle(brick)
        # print(brick, result)
        if result == -1:  # hit the bottom
            # print('settled', brick)
            settled.add(brick)
        elif result == 0:  # not moving, maybe later
            unsettled.appendleft(brick)
        elif result == 1:  # falling
            unsettled.append(brick)
        # input()

    # print(bricks)

    def check_supporting(brick):
        resting = []
        for point in bricks[brick]:
            above = vadd(point, (0,0,1))
            if above in points and points[above] != brick:
                resting.append(points[above])
        if len(resting) == 0:
            # print(brick, 'supports nothing', 1)
            return 1

        # print(brick, 'below', resting)
        for upper_brick in resting:
            below_bricks = set()
            for point in bricks[upper_brick]:
                below = vsub(point, (0, 0, 1))
                if below in points and points[below] != upper_brick:
                    below_bricks.add(points[below])
            if len(below_bricks) > 1:
                # print(brick, 'hat', upper_brick, 'also supported', below_bricks, 1)
                pass
            else:
                # print(brick, 'hat', upper_brick, 'solely supported by', below_bricks, 0)
                return 0
        return 1

    acc = 0
    for brick in bricks:
        acc += check_supporting(brick)

    return acc

# not right: 538

# def p2():
#     bricks = {}
#     points = {}
#     for i, line in enumerate(data):
#         i = chr(i+65)
#         a,b = line.split('~')
#         a_x, a_y, a_z = [int(n) for n in a.split(',')]
#         b_x, b_y, b_z = [int(n) for n in b.split(',')]
#         brick = []
#         for x in range(a_x, b_x+1):
#             for y in range(a_y, b_y+1):
#                 for z in range(a_z, b_z+1):
#                     point = (x,y,z)
#                     brick.append(point)
#                     points[point] = i
#         bricks[i] = brick
#         # print(bricks)
#
#     def try_settle(brick):
#         brick_points = bricks[brick]
#         # print(id, brick_points)
#         for point in brick_points:
#             below = vsub(point, (0,0,1))
#             if below in points and points[below] != brick:
#                 # print('on something')
#                 return -1 if points[below] in settled else 0
#             if below[2] == 0:
#                 # print('hit floor')
#                 return -1
#         else:
#             # print('aaaa')
#             new_points = {vsub(point, (0,0,1)) for point in brick_points}
#             new_brick = [*new_points]
#             # print(new_brick)
#             # input()
#             for point in brick_points:
#                 del points[point]
#             for point in new_points:
#                 points[point] = brick
#             bricks[brick] = new_brick
#             return 1
#
#     unsettled = deque(bricks.keys())
#     settled = set()
#     while unsettled:
#         # print('unsettled', unsettled)
#         brick = unsettled.pop()
#         result = try_settle(brick)
#         # print(brick, result)
#         if result == -1:  # hit the bottom
#             # print('settled', brick)
#             settled.add(brick)
#         elif result == 0:  # not moving, maybe later
#             unsettled.appendleft(brick)
#         elif result == 1:  # falling
#             unsettled.append(brick)
#         # input()
#
#     # print(bricks)
#
#     @memo
#     def get_supported_by(brick):
#         print('testing', brick)
#         resting = []
#         for point in bricks[brick]:
#             above = vadd(point, (0, 0, 1))
#             if above in points and points[above] != brick:
#                 resting.append(points[above])
#
#         if len(resting) == 0:
#             return 0  # nothing on top to fall
#
#         fallers = 0
#         for upper_brick in resting:
#             below_bricks = set()
#             for point in bricks[upper_brick]:
#                 below = vsub(point, (0, 0, 1))
#                 if below in points and points[below] != upper_brick and points[below] != brick:
#                     below_bricks.add(points[below])
#
#             print(brick, 'hat', upper_brick, 'supported by', below_bricks)
#             if len(below_bricks) != 0:
#                 continue
#
#             fallers += 1 + get_supported_by(upper_brick)
#         print(brick, 'falls', fallers)
#         return fallers
#
#     acc = 0
#     for brick in bricks:
#         acc += get_supported_by(brick)
#
#     return acc


def p2():
    bricks = {}
    points = {}
    for i, line in enumerate(data):
        # i = chr(i+65)
        a,b = line.split('~')
        a_x, a_y, a_z = [int(n) for n in a.split(',')]
        b_x, b_y, b_z = [int(n) for n in b.split(',')]
        brick = []
        for x in range(a_x, b_x+1):
            for y in range(a_y, b_y+1):
                for z in range(a_z, b_z+1):
                    point = (x,y,z)
                    brick.append(point)
                    points[point] = i
        bricks[i] = brick
        # print(bricks)

    def try_settle(brick, bs, ps):
        brick_points = bs[brick]
        # print(id, brick_points)
        for point in brick_points:
            below = vsub(point, (0,0,1))
            if below in ps and ps[below] != brick:
                # print('on something')
                return -1 if ps[below] in settled else 0
            if below[2] == 0:
                # print('hit floor')
                return -1
        else:
            # print('aaaa')
            new_points = {vsub(point, (0,0,1)) for point in brick_points}
            new_brick = [*new_points]
            # print(new_brick)
            # input()
            for point in brick_points:
                del ps[point]
            for point in new_points:
                ps[point] = brick
            bs[brick] = new_brick
            return 1

    unsettled = deque(bricks.keys())
    settled = set()
    i = 0
    while unsettled:
        i += 1
        # print('unsettled', unsettled)
        brick = unsettled.pop()
        result = try_settle(brick, bricks, points)
        # print(brick, result)
        if result == -1:  # hit the bottom
            # print('settled', brick)
            settled.add(brick)
        elif result == 0:  # not moving, maybe later
            unsettled.appendleft(brick)
        elif result == 1:  # falling
            unsettled.append(brick)

    # bruteforce, ho!
    acc = 0
    for i, brick in enumerate(bricks):
        print(i, len(bricks), '...', end='\r')
        moved = set()
        new_bricks = copy.deepcopy(bricks)
        new_points = copy.deepcopy(points)
        del new_bricks[brick]
        for point in bricks[brick]:
            del new_points[point]

        unsettled = deque(new_bricks.keys())
        settled = set()
        while unsettled:
            # print('unsettled', unsettled)
            brick2 = unsettled.pop()
            result = try_settle(brick2, new_bricks, new_points)
            # print(brick, result)
            if result == -1:  # hit the bottom
                # print('settled', brick)
                settled.add(brick2)
            elif result == 0:  # not moving, maybe later
                unsettled.appendleft(brick2)
            elif result == 1:  # falling
                moved.add(brick2)
                unsettled.append(brick2)
        acc += len(moved)

    return acc


setday(22)

data = parselines()

print('part1:', p1() )
print('part2:', p2() )
