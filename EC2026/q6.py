from ec import *
import networkx as nx


def solve(part):
    data = parse_lines(part)
    G = nx.DiGraph()
    G_inv = nx.DiGraph()

    all_items = []
    for line in data:
        item, ingrs = line.split(':')
        ingrs = ingrs.split(',')
        all_items.append(item)
        for ingr in ingrs:
            G.add_edge(item, ingr)
            G_inv.add_edge(ingr, item)

    if part == 1:
        return len(nx.descendants(G, 'NULL'))
    elif part == 2:
        return len(nx.descendants(G_inv, 'NULL'))
    else:
        return sum(1 for item in all_items if len(nx.descendants(G, item) & {'NULLv1', 'NULLv2', 'NULLv3'}) > 1)

if __name__ == '__main__':
    setquest(6)

    print('part1:', solve(1))
    print('part2:', solve(2))
    print('part3:', solve(3))
