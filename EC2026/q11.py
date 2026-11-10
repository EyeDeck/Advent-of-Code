from ec import *
import networkx as nx


def parse_input(n):
    data = parse_double_break(n)
    portal_ct = int(data[0].split(':')[1])
    shortcuts = [tuple(int(y) for y in x.split()) for x in data[1].split('\n')]
    # print(portal_ct, shortcuts)
    return portal_ct, shortcuts


def link_adjacent(G, portal_ct, dist):
    for x in range(0,portal_ct):
        for y in range(-dist,dist+1):
            a, b = x+1, (x+y)%portal_ct+1
            if a == b:
                continue
            G.add_edge(a,b)


def calc_total_dist(G):
    return sum(sum(x[1].values()) for x in nx.shortest_path_length(G))


def p1():
    portal_ct, shortcuts = parse_input(1)

    G = nx.Graph()
    link_adjacent(G, portal_ct, 1)

    base_strain = calc_total_dist(G)

    for a,b in shortcuts:
        G.add_edge(a,b)

    return base_strain - calc_total_dist(G)


def p2():
    portal_ct, shortcuts = parse_input(2)

    G = nx.Graph()
    link_adjacent(G, portal_ct, 3)

    base_strain = calc_total_dist(G)

    for a,b in shortcuts:
        G.add_edge(a,b)

    best_resonance = 0

    for x in range(1,portal_ct):
        for y in range(x, portal_ct):
            if x == y or G.has_edge(x,y):
                continue
            G.add_edge(x,y)
            best_resonance = max(best_resonance, base_strain - calc_total_dist(G))
            G.remove_edge(x, y)

    return best_resonance


# this is some annoying combinatorics
# actually pretty useful though, I should think about chucking it in my AoC/EC lib
def perfect_matchings(elements):
    def _match(pool):
        if not pool:
            yield []
            return

        first = pool[0]
        for i in range(1, len(pool)):
            pair = (first, pool[i])
            remaining = pool[1:i] + pool[i + 1:]
            for rest in _match(remaining):
                yield [pair] + rest

    return _match(elements)


def p3():
    portal_ct, shortcuts = parse_input(3)

    G = nx.Graph()
    link_adjacent(G, portal_ct, 3)

    base_strain = calc_total_dist(G)

    for a,b in shortcuts:
        G.add_edge(a,b)

    best_resonance = 0

    for offset in range(0,portal_ct//8):
        candidates = [offset+(x*(portal_ct//8)) for x in range(8)]
        # print(offset, candidates)
        for matching in perfect_matchings(candidates):
            if any(G.has_edge(*pair) for pair in matching):
                continue

            for pair in matching:
                G.add_edge(*pair)

            best_resonance = max(best_resonance, base_strain - calc_total_dist(G))

            for pair in matching:
                G.remove_edge(*pair)

    return best_resonance


if __name__ == '__main__':
    setquest(11)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
