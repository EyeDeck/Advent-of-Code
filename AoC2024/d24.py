import copy
import operator

import networkx as nx
from pyvis.network import Network

from aoc import *


def run_sim(logic, wires):
    while logic:
        to_pop = []
        for i, entry in logic.items():
            op, a, b, out = entry
            if a in wires:
                logic[i][1] = wires[a]
            if b in wires:
                logic[i][2] = wires[b]
            if isinstance(a, int) and isinstance(b, int):
                wires[out] = logic_map[op](a, b)
                to_pop.append(i)
        for i in to_pop:
            del logic[i]
    return wires


def get_wires_starting_with(wires, c):
    return {k: v for k, v in wires.items() if k[0] == c}


def wires_to_int(wires):
    return sum(v << get_ints(k)[0] for k, v in wires.items())


def p1():
    return wires_to_int(get_wires_starting_with(run_sim(copy.deepcopy(logic_data), copy.deepcopy(wire_data)), 'z'))


def p2():
    wires = copy.deepcopy(wire_data)

    swaps = [
        ['nwq', 'z36'],
        ['z18', 'fvw'],
        ['mdb', 'z22'],
        ['wpq', 'grf'],
    ]

    swap_map = {k: v for k, v in swaps} | {v: k for k, v in swaps}

    logic = copy.deepcopy(logic_data)
    for i, gate in logic.items():
        if gate[3] in swap_map:
            gate[3] = swap_map[gate[3]]

    x_wires = get_wires_starting_with(wires, 'x')
    y_wires = get_wires_starting_with(wires, 'y')

    input_x = wires_to_int(x_wires)
    input_y = wires_to_int(y_wires)

    G = nx.DiGraph()
    gate_cts = {'XOR': 0, 'AND': 0, 'OR': 0}
    for i, gate in logic.items():
        op, a, b, out = gate
        gate_node = op + str(gate_cts[op])
        gate_cts[op] += 1
        G.add_edge(a, gate_node, weight=(1.5 if a[0]=='x' else (1.7 if op=='XOR' else 1)))
        G.add_edge(b, gate_node, weight=(1.5 if b[0]=='x' else (1.7 if op=='XOR' else 1)))
        G.add_edge(gate_node, out, weight=(1.5 if out[0]=='z' else 1))

    net = Network(notebook=False, directed=True, bgcolor='#222222', font_color='white', width='100%', height='100vh',
                  cdn_resources='remote')

    print('Calculating graph...', end='\r', flush=True)
    pos = nx.kamada_kawai_layout(G, scale=5000)
    # pos = nx.forceatlas2_layout(G)
    # pos = nx.spiral_layout(G, equidistant=True, resolution=30000)
    # pos = nx.arf_layout(G, scaling=1000.0)

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
        x, y = position
        net.add_node(
            node,
            label=(re.sub(r'\d', '', node) if node[0] in 'XAO' else node),
            x=int(x), y=int(y),
            physics=False,
            shape='ellipse',
            color=(node_colors[node[0]] if node[0] in node_colors else node_colors[None]),
        )

    for source, target in G.edges():
        net.add_edge(source, target)

    net.write_html('d24_graph_visualization.html')

    real_in = input_x + input_y
    real_out = wires_to_int(get_wires_starting_with(run_sim(logic, wires), 'z'))

    assert real_in == real_out, 'gates are still buggy'

    return ','.join(sorted([x for xs in swaps for x in xs]))


setday(24)

with open_default() as file:
    wires_raw, logic_raw = file.read().split('\n\n')

wire_data = {k: int(v) for k, v in [line.split(': ') for line in wires_raw.split('\n')]}
logic_data = {i: [g[1], g[0], g[2], g[4]] for i, g in enumerate([line.split() for line in logic_raw.split('\n')])}

logic_map = {'XOR': operator.xor, 'AND': operator.and_, 'OR': operator.or_}

print('part1:', p1())
print('part2:', p2())
