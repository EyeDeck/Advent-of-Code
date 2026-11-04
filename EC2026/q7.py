from ec import *
import networkx as nx


def p1():
    data = parse_lines(1)

    G = nx.DiGraph()
    for line in data:
        i, energy, cons = [l.strip(',') for l in line.split(' ')]
        i = int(i.split('=')[1])
        energy = int(energy.split('=')[1])
        cons = [int(c) for c in cons.split('=')[1].split(',')]
        print(i,energy,cons)

        for edge in cons:
            G.add_edge(i,edge)
        G.nodes[i]['energy'] = energy
        print('e', i, G.nodes[i]['energy'])

    print(G)
    most, _ = max(G.out_degree, key=lambda x: x[1])
    print(most)

    def r_dfs(G, node, depth):
        G.nodes[node]['energy'] += depth

        if depth == 0:
            return

        for neighbor in G.neighbors(node):
            r_dfs(G, neighbor, depth-1)

    r_dfs(G, most, 5)

    print(G.nodes(data='energy'))

    return sum(e for i,e in G.nodes(data='energy'))


def p2():
    data = parse_lines(2)

    G = nx.DiGraph()
    for line in data:
        i, energy, cons = [l.strip(',') for l in line.split(' ')]
        i = int(i.split('=')[1])
        energy = int(energy.split('=')[1])
        cons = [int(c) for c in cons.split('=')[1].split(',')]
        print(i,energy,cons)

        for edge in cons:
            G.add_edge(i,edge)
        G.nodes[i]['energy'] = energy
        print('e', i, G.nodes[i]['energy'])

    print(G)
    most, _ = max(G.out_degree, key=lambda x: x[1])
    print(most)

    def r_dfs(G, node, depth):
        G.nodes[node]['energy'] += depth

        if depth == 0:
            return

        for neighbor in G.neighbors(node):
            r_dfs(G, neighbor, depth-1)

    r_dfs(G, most, 10)

    print(G.nodes(data='energy'))

    return sum(e for i,e in G.nodes(data='energy'))


def p3():
    data = parse_lines(3)

    G = nx.DiGraph()
    for line in data:
        i, energy, cons = [l.strip(',') for l in line.split(' ')]
        i = int(i.split('=')[1])
        energy = int(energy.split('=')[1])
        cons = [int(c) for c in cons.split('=')[1].split(',')]
        print(i,energy,cons)

        for edge in cons:
            G.add_edge(i,edge)
        G.nodes[i]['energy'] = energy
        print('e', i, G.nodes[i]['energy'])

    def tick(G, q):
        new_q = defaultdict(lambda: defaultdict(int))

        for node in sorted(q):
            energies = q[node]
            for energy, ct in energies.items():
                # print(node, energies)
                print(f"cloud {node} received {ct} {('impulse' if ct == 1 else 'impulses')} with strength {energy} +{energy*ct} (energy {G.nodes[node]['energy']} -> {G.nodes[node]['energy'] + energy*ct})")
                G.nodes[node]['energy'] += energy * ct
                if energy > 0:
                    for neighbor in G.neighbors(node):
                        new_q[neighbor][energy-1] += ct

        print([i for i in G.nodes()])

        to_remove = set()
        for node in G.nodes():
            # print(node,'...')
            if G.nodes[node]['energy'] > 1_000_000:
                print(node, 'exploded!')
                for neighbor in G.neighbors(node):
                    new_q[neighbor][10] += 1
                to_remove.add(node)

        for node in to_remove:
            G.remove_node(node)
            if node in new_q:
                new_q.pop(node)
        # print('removed', to_remove)
        print('q', new_q)

        return new_q

    best = 0


    # for node in [2]:
    for node in G.nodes():
        print('starting with', node)
        q = defaultdict(lambda: defaultdict(int))
        q[node][10] += 1
        g_copy = G.copy()
        print('start q', q)
        stage = 1
        while q:
            print(f'\nStage {stage}:')
            q = tick(g_copy, q)
            stage += 1

        best = max(best, sum(e for i,e in g_copy.nodes(data='energy', default=0)))

    return best

if __name__ == '__main__':
    setquest(7)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
