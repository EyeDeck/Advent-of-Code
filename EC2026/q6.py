from ec import *
import networkx as nx


def p1():
    data = parse_lines(1)
    G = nx.DiGraph()

    for line in data:
        item, ingrs = line.split(':')
        ingrs = ingrs.split(',')
        print(item, ingrs)
        for ingr in ingrs:
            G.add_edge(item, ingr)
    print(nx.descendants(G, 'NULL'))

    return len(nx.descendants(G, 'NULL'))


def p2():
    data = parse_lines(2)
    G = nx.DiGraph()

    for line in data:
        item, ingrs = line.split(':')
        ingrs = ingrs.split(',')
        print(item, ingrs)
        for ingr in ingrs:
            G.add_edge(ingr, item)
    print(nx.descendants(G, 'NULL'))

    return len(nx.descendants(G, 'NULL'))


def p3():
    data = parse_lines(3)
    G = nx.DiGraph()

    all_items = []
    for line in data:
        item, ingrs = line.split(':')
        ingrs = ingrs.split(',')
        print(item, ingrs)
        for ingr in ingrs:
            G.add_edge(item, ingr)
        all_items.append(item)

    acc = 0
    for item in all_items:
        if len(set(nx.descendants(G, item)) & {'NULLv1', 'NULLv2', 'NULLv3'}) > 1:
            acc += 1

    return acc


if __name__ == '__main__':
    setquest(6)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
