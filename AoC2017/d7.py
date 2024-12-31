import networkx as nx

from aoc import *


def solve():
    G = nx.DiGraph()
    for line in data:
        parts = line.split()
        name = parts[0]
        weight = int(parts[1][1:-1])
        G.add_node(name, weight=weight)

        if len(parts) > 2:
            for child in [s.replace(',', '') for s in parts[3:]]:
                G.add_edge(name, child)

    assert nx.is_tree(G)
    root_node = next(nx.topological_sort(G))
    yield root_node

    unbalanced = root_node
    while unbalanced:
        successors = list(G.successors(unbalanced))
        weights = [G.nodes[node]['weight'] + sum(G.nodes[d]['weight'] for d in nx.descendants(G, node)) for node in successors]
        weight_dict = defaultdict(list)
        for node, weight in zip(successors, weights):
            weight_dict[weight].append(node)
        if len(weight_dict) == 1:
            yield G.nodes[unbalanced]['weight'] - diff_weight
        ub = min(weight_dict.items(), key=lambda x: len(x[1]))
        b = max(weight_dict.items(), key=lambda x: len(x[1]))
        unbalanced_weight, unbalanced = ub[0], ub[1][0]
        diff_weight = unbalanced_weight - b[0]


setday(7)

data = parselines()

verbose = '-v' in sys.argv or '--verbose' in sys.argv

gen = solve()
print('part1:', next(gen))
print('part2:', next(gen))
