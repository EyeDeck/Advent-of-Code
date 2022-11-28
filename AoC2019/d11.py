import copy
import sys
from collections import defaultdict
from operator import itemgetter
import numpy as np


# Accepts [[layer, options], ...]
#   layer is a list or array of positional values, or dict where contents (x,y):value, e.g.:
#       [[0,1],[2,3]]      = '0 1\n2 3'
#       {(0,0):0, (1,1):2} = '0  \n2  '
#   options is a dict:
#       'map': map of values: 'output string', e.g. {0:'~', 1:'#', 'default':' '}
#       'swap_axes': True or False
#       'rotate': 0, 90, 180, or 270
#       'flip_v': True or False
#       'flip_h': True or False
# Layers are rendered with first layer at bottom, second layer on top of that, etc
# Returns a printable string
def render_gen(layers):
    bounds = None
    # don't mutate to mutate
    layers = copy.deepcopy(layers)
    # first, get the bounds of what we have to render
    # also apply transformations while we're at it
    for i, layer in enumerate(layers):
        this_layer = layers[i][0]
        options = layers[i][1]

        layer_bounds = None
        if isinstance(this_layer, list):
            layers[i][0] = this_layer = np.array(this_layer)
        if isinstance(this_layer, np.ndarray):
            if 'swap_axes' in options:
                np.swapaxes(this_layer, 0, 1)
            if 'rotate' in options:
                np.rot90(this_layer, options['rotate'])
            if ('flip_v' in options and options['flip_v']) or ('flip_ud' in options and options['flip_ud']):
                np.flip(this_layer, 0)
            if ('flip_h' in options and options['flip_h']) or ('flip_lr' in options and options['flip_lr']):
                np.flip(this_layer, 1)

            layer_bounds = ((0,0), this_layer.shape)
            print(layer_bounds)
        elif isinstance(this_layer, dict):
            for key in this_layer.copy().keys():
                if not isinstance(key, tuple):
                    del this_layer[key]

            if 'swap_axes' in options:
                layers[i][0] = this_layer = {(k[1], k[0]): v for k, v in this_layer}

            layer_bounds = get_dict_bounds(this_layer)

            offset = (abs(min(layer_bounds[0][0], 0)), abs(min(layer_bounds[0][1], 0)))
            if 'rotate' in options:
                layers[i][0] = this_layer = {(k[1], bounds[1][0] - k[0]):v for k,v in this_layer.items()}  # close

                layer_bounds = get_dict_bounds(this_layer)

            if ('flip_v' in options and options['flip_v']) or ('flip_ud' in options and options['flip_ud']):
                layers[i][0] = this_layer = {(layer_bounds[1][0] - k[0] + layer_bounds[0][0], k[1]): v for k, v in this_layer.items()}

            if ('flip_h' in options and options['flip_h']) or ('flip_lr' in options and options['flip_lr']):
                layers[i][0] = this_layer = {(k[0], layer_bounds[1][1] - k[1] + layer_bounds[0][1]): v for k, v in this_layer.items()}


            print(layer_bounds)

        if bounds:
            bounds = [(min(bounds[0][0], layer_bounds[0][0]), min(bounds[0][1], layer_bounds[0][1])),
                      (max(bounds[1][0], layer_bounds[1][0]), max(bounds[1][1], layer_bounds[1][1]))]
        else:
            bounds = layer_bounds
        print(layer_bounds)
    print(bounds)

    # now fill the array based on input + given rules
    offset = (abs(min(bounds[0][0], 0)), abs(min(bounds[0][1], 0)))
    out_arr = np.full((bounds[1][0] + offset[0], bounds[1][1] + offset[1]), fill_value=' ', dtype=str)
    for this_layer in layers:
    print(out_arr)


def get_dict_bounds(d):
    k = d.keys()
    return ((min(k, key=itemgetter(0))[0], min(k, key=itemgetter(1))[1]),
            (max(k, key=itemgetter(0))[0], max(k, key=itemgetter(1))[1]))


def render(board, dim, overlay=None):
    if overlay is None:
        overlay = {}
    to_str = []
    for y in range(dim[0]):
        for x in range(dim[1]):
            if (x, y) in overlay:
                to_str.append('#' if overlay[(x, y)] == 1 else '.')
            else:
                to_str.append(board[y][x])
            to_str.append(" ")
        to_str.append("\n")
    return "".join(to_str)


def intcode(p, args):
    p['error'] = 0
    while True:
        ptr = p['pointer']
        rb = p['relative_base']

        op = get_op(p, ptr)
        if op is None:
            p['error'] = 1
            return None
        # print(opcodes[op[0]][0], op)

        if op[0] == 1:  # add
            write_val(p, op[3], get_val(p, op[1]) + get_val(p, op[2]))
        elif op[0] == 2:  # mul
            write_val(p, op[3], get_val(p, op[1]) * get_val(p, op[2]))
        elif op[0] == 3:  # input
            if len(args):
                v = args.pop(0)
            else:
                v = int(input('Input:'))
            write_val(p, op[1], v)
        elif op[0] == 4:  # output
            p['pointer'] = ptr + len(op)
            return get_val(p, op[1])
        elif op[0] == 5:  # jump if true
            if get_val(p, op[1]) != 0:
                p['pointer'] = get_val(p, op[2])
                continue
        elif op[0] == 6:  # jump if false
            if get_val(p, op[1]) == 0:
                p['pointer'] = get_val(p, op[2])
                continue
        elif op[0] == 7:  # less than
            write_val(p, op[3], 1 if get_val(p, op[1]) < get_val(p, op[2]) else 0)
        elif op[0] == 8:  # equals
            write_val(p, op[3], 1 if get_val(p, op[1]) == get_val(p, op[2]) else 0)
        elif op[0] == 9:
            p['relative_base'] = rb + get_val(p, op[1])
        elif op[0] == 99:
            return None

        p['pointer'] = ptr + len(op)


def get_op(p, ptr):
    op = [p[ptr] % 100]

    if op[0] not in opcodes:
        return None

    ln = opcodes[op[0]][1]
    modes = [int(i) for i in str(p[ptr] // 100)[::-1]]
    modes.extend([0 for _ in range(ln - len(modes) - 1)])

    for i in range(1, ln):
        op.append((p[ptr + i], modes[i - 1]))
    return op


def get_val(program, pointer):
    if pointer[1] == 0:
        return program[pointer[0]]
    elif pointer[1] == 1:
        return pointer[0]
    else:
        return program[program['relative_base'] + pointer[0]]


def write_val(program, pointer, val):
    if pointer[1] == 0:
        program[pointer[0]] = val
    # elif pointer[1] == 1:
    #    program[0] = val
    else:
        program[program['relative_base'] + pointer[0]] = val


opcodes = {
    1: ('add         ', 4),
    2: ('mul         ', 4),
    3: ('input       ', 2),
    4: ('output      ', 2),
    5: ('jmp_if_true ', 3),
    6: ('jmp_if_false', 3),
    7: ('less_than   ', 4),
    8: ('equals      ', 4),
    9: ('mod_rel_base', 2),
    99: ('stop        ', 1)
}


def step_robot(program, state):
    out = []
    args = [state[state['pos']]]
    for i in range(0, 2):
        cur = intcode(program, args)
        if cur is None:
            return None
        out.append(cur)
    state[state['pos']] = out[0]  # write to board
    state['angle'] = next_state[state['angle']][out[1]]
    state['pos'] = (state['pos'][0] + step[state['angle']][0], state['pos'][1] + step[state['angle']][1])
    return out


next_state = {
    '<': ['v', '^'],
    '^': ['<', '>'],
    '>': ['^', 'v'],
    'v': ['>', '<']
}

step = {
    '<': (-1, 0),
    '^': [0, 1],
    '>': [1, 0],
    'v': [0, -1]
}

f = 'd11.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(i) for i in open(f).read().split(',')]
inp = defaultdict(int, {i: inp[i] for i in range(0, len(inp))})

state = defaultdict(int)
state['pos'] = (0, 0)
state['angle'] = '^'
p1_program = copy.deepcopy(inp)
while step_robot(p1_program, state) is not None:
    pass
print('p1:', len(state) - 2)


state = defaultdict(int)
state['pos'] = (0,0)
state[state['pos']] = 1
state['angle'] = '^'
p2_program = copy.deepcopy(inp)
while step_robot(p2_program, state) is not None:
    pass
board = [['.' for _ in range(0,50)] for _ in range(0,5)]
# print(state)
print_map = defaultdict(str, {
    0: ' ',
    1: '#'
})
print(render_gen([[board, print_map], [state, print_map]]))
