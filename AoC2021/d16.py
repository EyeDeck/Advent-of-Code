import sys
from math import prod


def parse(packet, o=0, depth=0):
    # print(f'{packet[o:o+100]}...offset:{o},depth:{depth}')
    version = int(packet[o:o + 3], 2)
    type_id = int(packet[o + 3:o + 6], 2)
    if type_id == 4:
        s = []
        o += 6
        while True:
            n = packet[o + 1:o + 5]
            s.append(n)
            o += 5
            if packet[o-5] == '0':
                break
        v = int(''.join(s), 2)
        return version, type_id, v, o
    else:
        o += 6
        length_type_id = packet[o]
        o += 1
        children = []
        if length_type_id == '0':
            header_len = 15
            data_len = int(packet[o:o + header_len], 2)
            o += header_len
            end = o + data_len
            while o < end:
                v, t, val, o = parse(packet, o, depth + 1)
                children.append((v, t, val))
        else:
            header_len = 11
            subpacket_number = int(packet[o:o + header_len], 2)
            o += header_len
            for i in range(subpacket_number):
                v, t, val, o = parse(packet, o, depth + 1)
                children.append((v, t, val))
        return version, type_id, children, o


def tally_ver(d):
    n = d[0]
    if not isinstance(d[2], int):
        for thing in d[2]:
            n += tally_ver(thing)
    return n


def p1():
    struct = parse(bin_data)
    # print(struct)
    return tally_ver(struct)


def evaluate(d):
    version, packet_id, subpackets = d
    # print(version, packet_id, subpackets)
    return ops[packet_id](subpackets)


def p2():
    struct = parse(bin_data)
    return evaluate(struct[:3])


cnv = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
       '4': '0100', '5': '0101', '6': '0110', '7': '0111',
       '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
       'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}


ops = [
    lambda d: sum(ops[8](d)),
    lambda d: prod(ops[8](d)),
    lambda d: min(ops[8](d)),
    lambda d: max(ops[8](d)),
    lambda d: d,
    lambda d: 1 if evaluate(d[0]) > evaluate(d[1]) else 0,
    lambda d: 1 if evaluate(d[0]) < evaluate(d[1]) else 0,
    lambda d: 1 if evaluate(d[0]) == evaluate(d[1]) else 0,
    lambda d: [evaluate(p) for p in d]
]

day = 16
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

if f[-4:] == '.txt':
    with open(f) as file:
        data = file.read().strip()
else:
    data = f
bin_data = ''.join([cnv[c] for c in data])

print(f'part1: {p1()}')
print(f'part2: {p2()}')
