import copy
import operator

import networkx as nx
from pyvis.network import Network

import matplotlib.pyplot as plt

from aoc import *


def p1():
    logic = copy.deepcopy(logic_data)
    wires = copy.deepcopy(wire_data)
    while logic:
        to_pop = []
        for i, entry in logic.items():
            op, a, b, out = entry
            if a in wires:
                logic[i][1] = wires[a]
            if b in wires:
                logic[i][2] = wires[b]
            if isinstance(a, bool) and isinstance(b, bool):
                wires[out] = op(a, b)
                to_pop.append(i)
                continue
        for i in to_pop:
            del logic[i]

    return wires_to_int(get_wires_starting_with(wires, 'z'))


def get_wires_starting_with(wires, c):
    return {k: v for k, v in wires.items() if k[0] == c}


def wires_to_int(wires):
    return sum((1 << i + 1 if wires[k] else 0) for i, k in enumerate(sorted(wires.keys(), reverse=True)))


# 0000000000000000010100101110001101110001011111001010000010101000
# 0000000000000000001100111011000111000100000011101111101010100110
def p2():
    logic = copy.deepcopy(logic_data)
    wires = copy.deepcopy(wire_data)

    x_wires = get_wires_starting_with(wires, 'x')
    y_wires = get_wires_starting_with(wires, 'y')

    input_x = wires_to_int(x_wires)
    input_y = wires_to_int(y_wires)
    print(input_x, input_y, input_x + input_y)

    print('x', x_wires)
    print('y', y_wires)
    while logic:
        to_pop = []
        for i, entry in logic.items():
            op, a, b, out = entry
            if a in wires:
                logic[i][1] = wires[a]
            if b in wires:
                logic[i][2] = wires[b]
            if isinstance(a, bool) and isinstance(b, bool):
                wires[out] = op(a, b)
                to_pop.append(i)
                continue
        for i in to_pop:
            del logic[i]

    real_in = input_x + input_y
    real_out = wires_to_int(get_wires_starting_with(wires, 'z'))
    print(format(real_in, '064b'))
    print(format(real_out, '064b'))
    # print(bin(real_out))


def p2():
    wires = copy.deepcopy(wire_data)

    swaps = [
        ['nwq', 'z36'],
        ['z18', 'fvw'],
        ['mdb', 'z22'],
        ['wpq', 'grf'],
    ]

    revmap = {k: v for k, v in swaps} | {v: k for k, v in swaps}
    print(revmap)

    logic = {
        i: [
            logic_map[g[1]],
            g[0],
            g[2],
            (revmap[g[4]] if g[4] in revmap else g[4])
        ] for i, g in enumerate([line.split() for line in logic_raw.split('\n')])}

    # print(logic==logic_data)

    x_wires = get_wires_starting_with(wires, 'x')
    y_wires = get_wires_starting_with(wires, 'y')

    input_x = wires_to_int(x_wires)
    input_y = wires_to_int(y_wires)
    print(input_x, input_y, input_x + input_y)

    G = nx.DiGraph()
    gate_cts = {'XOR': 0, 'AND': 0, 'OR': 0}
    for i, gate in logic.items():
        print(gate)
        op, a, b, out = gate
        op = logic_map_i[op]
        gate_node = op + str(gate_cts[op])
        gate_cts[op] += 1
        G.add_edge(a, gate_node)
        G.add_edge(b, gate_node)
        G.add_edge(gate_node, out)

    print(G)

    # nx.draw_kamada_kawai(G, with_labels=True)
    # # nx.draw_planar(G, with_labels=True)
    # # nx.draw_spectral(G, with_labels=True)  # useless
    # # nx.draw_spring(G, with_labels=True)  # useless
    # # nx.draw_shell(G, with_labels=True)
    # plt.show()

    net = Network(notebook=False, directed=True, bgcolor='#222222', font_color='white', width='100%', height='100vh', cdn_resources='remote')

    pos = nx.kamada_kawai_layout(G, scale=5000)
    # pos = nx.planar_layout(G, scale=100)

    node_colors = {
        'x': '#00FF90',
        'y': '#A1FF00',
        'z': '#FF0000',
        'X': '#0050FF',  # XOR
        'A': '#FF6A00',  # AND
        'O': '#FFDD00',  # OR
        None: '#00AEFF',
    }

    for node, position in pos.items():
        print(node)
        print(G[node])
        x, y = position
        net.add_node(
            node,
            label=(re.sub(r'\d', '', node) if node[0] in 'XAO' else node),
            x=x, y=y,
            physics=False,
            shape='ellipse',
            color=(node_colors[node[0]] if node[0] in node_colors else node_colors[None]),
        )

    for source, target in G.edges():
        net.add_edge(source, target)

    net.write_html('d24_graph_visualization.html')

    while logic:
        to_pop = []
        for i, entry in logic.items():
            op, a, b, out = entry
            if a in wires:
                logic[i][1] = wires[a]
            if b in wires:
                logic[i][2] = wires[b]
            if isinstance(a, bool) and isinstance(b, bool):
                wires[out] = op(a, b)
                to_pop.append(i)
                continue
        for i in to_pop:
            del logic[i]

    real_in = input_x + input_y
    real_out = wires_to_int(get_wires_starting_with(wires, 'z'))
    print(format(real_in, '064b'))
    print(format(real_out, '064b'))
    # print(bin(real_out))

    return ','.join(sorted([x for xs in swaps for x in xs]))


setday(24)

# data = parselines()
# data = parselines(get_ints)
# grid, inverse, unique = parsegrid()

with open_default() as file:
    wires_raw, logic_raw = file.read().split('\n\n')
# wires = {k:v=='1' for k,v in [wire for wire in ]}
wire_data = {k: v == '1' for k, v in [line.split(': ') for line in wires_raw.split('\n')]}
# print([line.split() for line in logic_raw.split('\n')])

logic_map = {'XOR': operator.xor, 'AND': operator.and_, 'OR': operator.or_}
logic_map_i = {v: k for k, v in logic_map.items()}
logic_data = {i: [logic_map[g[1]], g[0], g[2], g[4]] for i, g in
              enumerate([line.split() for line in logic_raw.split('\n')])}

# print(wires)
# print(logic)

verbose = '-v' in sys.argv or '--verbose' in sys.argv

print('part1:', p1())
print('part2:', p2())

# print('part1: %d\npart2: %d' % solve())
