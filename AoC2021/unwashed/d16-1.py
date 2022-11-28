import sys
import re
from math import prod


def parse(packet):
    version = int(packet[:3], 2)
    type_id = int(packet[3:6], 2)
    if type_id == 4:
        s = []
        offset = 6
        while True:
            datum = packet[offset:offset + 5]
            s.append(datum[1:])
            offset += 5
            if datum[0] == '0':
                break
        v = int(''.join(s), 2)
        return (version, type_id), v, offset
    else:
        length_type_id = packet[6]
        subpackets_parsed = []
        offset = 0
        if length_type_id == '0':
            header_len = 22
            data_len = int(packet[7:header_len], 2)
            subpackets = packet[header_len:header_len + data_len]
            while offset < len(subpackets):
                t, val, l = parse(subpackets[offset:])
                subpackets_parsed.append((t, val))
                offset += l
        else:
            header_len = 18
            subpacket_number = int(packet[7:header_len], 2)
            for i in range(subpacket_number):
                t, val, l = parse(packet[header_len + offset:])
                subpackets_parsed.append((t, val))
                offset += l
        offset += header_len
        return (version, type_id), subpackets_parsed, offset


def p1():
    struct = parse(bin_data)
    all_headers = re.findall('\((\d+, \d+)\)', str(struct))
    return sum([int(x.split(', ')[0]) for x in all_headers])


def evaluate(d):
    packet_id = d[0][1]
    subpackets = d[1:][0]
    return ops[packet_id](subpackets)


def p2():
    struct = parse(bin_data)
    return evaluate([struct[0], struct[1]])


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
    lambda d: 1 if evaluate(d[0]) > evaluate(d[0]) else 0,
    lambda d: 1 if evaluate(d[0]) < evaluate(d[1]) else 0,
    lambda d: 1 if evaluate(d[0]) == evaluate(d[1]) else 0,
    lambda d: [evaluate(p) for p in d],
]

day = 16
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().strip()
    bin_data = ''.join([cnv[c] for c in data])

print(f'part1: {p1()}')
print(f'part2: {p2()}')