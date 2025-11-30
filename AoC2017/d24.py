
from aoc import *


def solve():
    cmps_by_port = defaultdict(set)
    for line in data:
        t = tuple(int(s) for s in line.split('/'))
        l, r = t
        t_r = (r, l)
        cmps_by_port[l].add(t)
        cmps_by_port[r].add(t_r)

    def rdfs(prev):
        node, plink = prev.popitem()
        prev[node] = plink

        has_neighbor = False
        max_s = 0
        max_l = (0,0)
        for n in cmps_by_port[node[1]]:
            n_r = tuple(reversed(n))
            
            if {n, n_r} & prev.keys():
                continue
            has_neighbor = True

            next_prev = prev.copy()
            next_prev[n] = node

            r = rdfs(next_prev)

            max_s = max(max_s, r[0])
            max_l = max(max_l, r[1])

        if not has_neighbor:
            strength = sum(a+b for a,b in prev.keys())
            return strength, (len(prev), strength)
        else:
            return max_s, max_l

    r = rdfs({(0, 0): (0, 0)})
    return r


setday(24)

data = parselines()

r = solve()
print('part1: %d\npart2: %d' % (r[0], r[1][1]))
