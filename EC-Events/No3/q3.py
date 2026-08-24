from ec import *


def p1():
    data = parse_lines(1)
    nodes = []
    for line in data:
        node = {}
        for raw in line.split(','):
            l, r = raw.split('=')
            l = l.strip()
            node[l] = r
        nodes.append(node)

    root = nodes[0]
    # print(nodes)

    def dfs(src, visit_order, tgt):
        if src == tgt:
            return src

        if type(src) is str:
            return False

        l, r = src['leftSocket'], src['rightSocket']
        if type(l) is str:
            if l == tgt:
                return (src, 0)
        else:
            result = dfs(l, visit_order, tgt)
            if result:
                return result

        visit_order.append(src['id'])

        if type(r) is str:
            if r == tgt:
                return (src, 1)
        else:
            result = dfs(r, visit_order, tgt)
            if result:
                return result

        return False

    for node in nodes[1:]:
        visit_order = []
        result = dfs(root, visit_order, node['plug'])
        if result:
            attach_node, side = result
            if side == 0:
                attach_node['leftSocket'] = node
            else:
                attach_node['rightSocket'] = node
            node['plug'] = attach_node
            # print(attach_node, side)

    # print(root)
    visit_order = []
    dfs(root, visit_order, None)
    # print(visit_order)

    acc = 0
    for i, v in enumerate(visit_order):
        acc += (i+1) * int(v)

    return acc


def p2():
    data = parse_lines(2)
    nodes = []
    for line in data:
        node = {}
        for raw in line.split(','):
            l, r = raw.split('=')
            l = l.strip()
            node[l] = r
        nodes.append(node)

    root = nodes[0]
    # print(nodes)

    def dfs(src, visit_order, tgt, tgt_color, tgt_shape):
        if src == tgt:
            return src

        if type(src) is str:
            return False

        l, r = src['leftSocket'], src['rightSocket']
        if type(l) is str:
            if l == tgt:
                return (src, 0, 1)

            l_sp = l.split(' ')
            if l_sp[0] == tgt_color or l_sp[1] == tgt_shape:
                return (src, 0, 0)
        else:
            result = dfs(l, visit_order, tgt, tgt_color, tgt_shape)
            if result:
                return result

        visit_order.append(src['id'])

        if type(r) is str:
            if r == tgt:
                return (src, 1, 1)
            r_sp = r.split(' ')

            if r_sp[0] == tgt_color or r_sp[1] == tgt_shape:
                return (src, 1, 0)
        else:
            result = dfs(r, visit_order, tgt, tgt_color, tgt_shape)
            if result:
                return result

        return False

    for node in nodes[1:]:
        visit_order = []
        result = dfs(root, visit_order, node['plug'], *node['plug'].split(' '))
        if result:
            attach_node, side, bond = result
            if side == 0:
                attach_node['leftSocket'] = node
            else:
                attach_node['rightSocket'] = node
            node['plug'] = attach_node
            # print(attach_node, side)

    # print(root)
    visit_order = []
    dfs(root, visit_order, None, None, None)
    # print(visit_order)

    acc = 0
    for i, v in enumerate(visit_order):
        acc += (i+1) * int(v)

    return acc

def p3():
    data = parse_lines(3)
    nodes = []
    for line in data:
        node = {}
        for raw in line.split(','):
            l, r = raw.split('=')
            l = l.strip()
            node[l] = r
            node['lweak'], node['rweak'] = None, None
        nodes.append(node)

    root = nodes[0]
    # print(nodes)

    def dfs(src, visit_order, tgt, tgt_color, tgt_shape, skip_until):
        # print(f'  dfs {src}, {visit_order}, {tgt}, {tgt_color}, {tgt_shape}, {skip_until}')
        # print('skip_until (read):', skip_until)
        if src == tgt:
            return src

        if type(src) is str:
            return False

        l, r = src['leftSocket'], src['rightSocket']
        lweak, rweak = src['lweak'], src['rweak']

        can_attach = len(skip_until) == 0

        if type(l) is str:
            if l == tgt and can_attach:
                return (src, 0, 1)

            if lweak is None:
                if can_attach:
                    l_sp = l.split(' ')
                    if l_sp[0] == tgt_color or l_sp[1] == tgt_shape:
                        # print(f'L {l_sp[0]} == {tgt_color} or {l_sp[1]} == {tgt_shape}')
                        return (src, 0, 0)
            else:
                result = dfs(lweak, visit_order, tgt, tgt_color, tgt_shape, skip_until)
                if result:
                    return result
        else:
            result = dfs(lweak or l, visit_order, tgt, tgt_color, tgt_shape, skip_until)
            if result:
                return result

        visit_order.append(src['id'])

        can_attach = len(skip_until) == 0

        # print('at that spot...')
        if type(r) is str:
            # print('it\'s a string')
            # print('we can attach')
            if r == tgt and can_attach:
                return (src, 1, 1)

            # print(r, tgt)

            if rweak is None:
                if can_attach:
                    r_sp = r.split(' ')
                    # print('rweak is None; ', r_sp, tgt_color, tgt_shape, r_sp[0] == tgt_color, )
                    if r_sp[0] == tgt_color or r_sp[1] == tgt_shape:
                        # print(f'R {r_sp[0]} == {tgt_color} or {r_sp[1]} == {tgt_shape}')
                        return (src, 1, 0)
            else:
                result = dfs(rweak, visit_order, tgt, tgt_color, tgt_shape, skip_until)
                if result:
                    return result
        else:
            result = dfs(rweak or r, visit_order, tgt, tgt_color, tgt_shape, skip_until)
            if result:
                return result

        if len(skip_until) > 0 and src == skip_until[0]:
            skip_until.pop(0)

        return False

    for node in nodes[1:]:
        # print('\nstarting node', node)
        # used as a messy pointer
        skip_until = []

        while node:
            # print('looking for attach point for node ', node)
            visit_order = []
            result = dfs(root, visit_order, node['plug'], *node['plug'].split(' '), skip_until)
            if result:
                attach_node, side, bond = result
                if bond == 1:
                    # print(f'forming strong bond {attach_node['id']}<->{node['id']}, {side}, {bond}')
                    if side == 0:
                        attach_node['leftSocket'] = node
                        if attach_node['lweak'] is not None:
                            skip_until.append(node)
                            # print('skip_until (write):', skip_until)
                            node = attach_node['lweak']
                            attach_node['lweak'] = None
                            # print(f'displaced weak bond {node['id']}--looking for new attach node')
                        else:
                            node = None
                    else:
                        attach_node['rightSocket'] = node
                        if attach_node['rweak'] is not None:
                            skip_until.append(node)
                            # print('skip_until (write):', skip_until)
                            node = attach_node['rweak']
                            attach_node['rweak'] = None
                            # print(f'displaced weak bond {node['id']}--looking for new attach node')

                        else:
                            node = None

                else:
                    # print(f'forming weak bond {attach_node['id']}<->{node['id']} , {side}, {bond}')
                    if side == 0:
                        # print('writing lweak bond')
                        attach_node['lweak'] = node
                    else:
                        # print('writing rweak bond')
                        attach_node['rweak'] = node
                    node = None

                # print(attach_node, side)

            # print('root:', root)
            # input()

    visit_order = []
    dfs(root, visit_order, None, None, None, [])
    # print(visit_order)

    acc = 0
    for i, v in enumerate(visit_order):
        acc += (i+1) * int(v)

    return acc

setquest(3)

print('part1:', p1())
print('part2:', p2())
print('part3:', p3())
