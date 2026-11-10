from ec import *
import networkx as nx


def p1():
    data = parse_double_break(1)
    portal_ct = int(data[0].split(':')[1])
    shortcuts = [tuple(int(y) for y in x.split()) for x in data[1].split('\n')]
    # print(portal_ct, shortcuts)

    G = nx.Graph()
    for i in range(1,portal_ct):
        G.add_edge(i,i+1)
    G.add_edge(portal_ct,1)
    # print(G.edges)

    min_raw = nx.shortest_path_length(G)
    min_raw = sum(sum(x[1].values()) for x in min_raw)

    for a,b in shortcuts:
        G.add_edge(a,b)

    min_shortcuts = nx.shortest_path_length(G)
    min_shortcuts = sum(sum(x[1].values()) for x in min_shortcuts)

    return min_raw - min_shortcuts


def p2():
    data = parse_double_break(2)
    portal_ct = int(data[0].split(':')[1])
    shortcuts = [tuple(int(y) for y in x.split()) for x in data[1].split('\n')]
    # print(portal_ct, shortcuts)

    G = nx.Graph()
    for x in range(0,portal_ct):
        for y in range(-3,4):
            a, b = x+1, (x+y)%portal_ct+1
            if a == b:
                continue
            G.add_edge(a,b)

    G.add_edge(portal_ct,1)
    # print(G.edges)

    min_raw = nx.shortest_path_length(G)
    min_raw = sum(sum(x[1].values()) for x in min_raw)

    print(min_raw)

    for a,b in shortcuts:
        G.add_edge(a,b)

    best_resonance = 0

    for x in range(1,portal_ct):
        for y in range(1, portal_ct):
            if x == y or G.has_edge(x,y):
                continue
            G.add_edge(x,y)
            min_shortcuts = nx.shortest_path_length(G)
            min_shortcuts = sum(sum(x[1].values()) for x in min_shortcuts)
            # print(f'{x},{y} = {min_shortcuts}')
            G.remove_edge(x, y)
            best_resonance = max(best_resonance, min_raw-min_shortcuts)

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
    data = parse_double_break(3)
    portal_ct = int(data[0].split(':')[1])
    shortcuts = [tuple(int(y) for y in x.split()) for x in data[1].split('\n')]
    # print(portal_ct, shortcuts)

    G = nx.Graph()
    for x in range(0,portal_ct):
        for y in range(-3,4):
            a, b = x+1, (x+y)%portal_ct+1
            if a == b:
                continue
            G.add_edge(a,b)

    G.add_edge(portal_ct,1)
    # print(G.edges)

    min_raw = nx.shortest_path_length(G)
    min_raw = sum(sum(x[1].values()) for x in min_raw)

    print(min_raw)

    for a,b in shortcuts:
        G.add_edge(a,b)

    best_resonance = 0

    for offset in range(0,portal_ct//8):
        candidates = [offset+(x*(portal_ct//8)) for x in range(8)]
        print(offset, candidates)
        for matching in perfect_matchings(candidates):
            # print(matching)
            if any(G.has_edge(*pair) for pair in matching):
                continue
            for pair in matching:
                G.add_edge(*pair)

            min_shortcuts = nx.shortest_path_length(G)
            min_shortcuts = sum(sum(x[1].values()) for x in min_shortcuts)

            for pair in matching:
                G.remove_edge(*pair)

            best_resonance = max(best_resonance, min_raw - min_shortcuts)

    return best_resonance


if __name__ == '__main__':
    setquest(11)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
