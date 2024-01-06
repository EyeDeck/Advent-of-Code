import hashlib
from aoc import *

def md5(s):
    md5 = hashlib.md5()
    md5.update(s.encode())
    return md5.hexdigest()

def solve():
    dir_map = [ ((0,-1), 'U'), ((0,1), 'D'), ((-1,0), 'L'), ((1,0), 'R') ]
    q = deque([((0,0), '')])
    longest = 0
    p1 = None
    while q:
        pos, path = q.popleft()
        # print(pos, path)
        if pos == (3,3):
            if p1 is None:
                p1 = path
            longest = max(longest, len(path))
            continue

        door_hash = md5(data + path)
        opens = [c in 'bcdef' for c in door_hash[:4]]

        for i, (v, c) in enumerate(dir_map):
            if not opens[i]:
                continue

            next_pos = vadd(v, pos)
            if next_pos[0] < 0 or next_pos[0] > 3 or next_pos[1] < 0 or next_pos[1] > 3:
                continue
            next_path = path + c

            q.append((next_pos, next_path))
    return p1, longest


setday(17)

data = parselines()[0]

print('part1: %s\npart2: %s' % solve())