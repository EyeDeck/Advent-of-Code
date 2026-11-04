from ec import *
import networkx as nx


def solve(part, start_energy, explosion_point):
    data = parse_lines(part)

    G = nx.DiGraph()
    for line in data:
        i, energy, cons = [l.strip(',') for l in line.split(' ')]
        i = int(i.split('=')[1])
        energy = int(energy.split('=')[1])
        cons = [int(c) for c in cons.split('=')[1].split(',')]
        # print(i, energy, cons)

        for edge in cons:
            G.add_edge(i,edge)
        G.nodes[i]['energy'] = energy

    def tick(G, q):
        new_q = defaultdict(lambda: defaultdict(int))

        for node in sorted(q):
            energies = q[node]
            for energy, ct in energies.items():
                if verbose:
                    print(f"cloud {node} received {ct} {('impulse' if ct == 1 else 'impulses')} with strength {energy} +{energy*ct} (energy {G.nodes[node]['energy']} -> {G.nodes[node]['energy'] + energy*ct})")
                G.nodes[node]['energy'] += energy * ct
                if energy > 1:
                    for neighbor in G.neighbors(node):
                        new_q[neighbor][energy-1] += ct

        if explosion_point < INF and any(1 for node in G.nodes() if G.nodes[node]['energy'] > explosion_point):
            if verbose:
                print('Explosions after this stage:')
            to_remove = set()
            for node in G.nodes():
                if G.nodes[node]['energy'] > explosion_point:
                    if verbose:
                        print(f"{node} exploded at energy {G.nodes[node]['energy']}")
                    for neighbor in G.neighbors(node):
                        new_q[neighbor][start_energy] += 1
                        if verbose:
                            print(f"  new impulse with strength {start_energy}: cloud {node} -> cloud {neighbor}")
                    to_remove.add(node)

            for node in to_remove:
                G.remove_node(node)
                if node in new_q:
                    new_q.pop(node)

        return new_q

    best = 0

    for node in G.nodes() if part == 3 else [max(G.out_degree, key=lambda x: x[1])[0]]:
        if verbose:
            print(f"Detailed propagation for starting cloud {node}:")
        q = defaultdict(lambda: defaultdict(int))
        q[node][start_energy] += 1
        g_copy = G.copy()
        stage = 1
        while q:
            if verbose:
                print(f'\nStage {stage}:')
            q = tick(g_copy, q)
            stage += 1

        best = max(best, sum(e for i,e in g_copy.nodes(data='energy', default=0)))

    return best


if __name__ == '__main__':
    setquest(7)

    print('part1:', solve(1, 5, INF))
    print('part2:', solve(2, 10, INF))
    print('part3:', solve(3, 10, 1_000_000))
