import sys
import re
from math import *


def parse_packet(packet):
    # print('\ncalled with:', packet)
    version = int(packet[:3],2)
    type_id = int(packet[3:6],2)
    # print('ver, type:', version, type_id)
    if type_id == 4:
        s = ""
        offset = 6
        while True:
            datum = packet[offset:offset + 5]
            s += datum[1:]
            offset += 5
            if datum[0] == '0':
                break
        v = int(s, 2)
        # print('int', s, v, offset)
        return (version, type_id), v, offset
    else:  # operator
        length_type_id = packet[6]
        subpackets_parsed = []
        offset = 0

        if length_type_id == '0':
            total_length = int(packet[7:7+15], 2)
            subpackets = packet[22:22+total_length]
            # print('subpackets:', subpackets)
            i = 0
            while True:
                i += 1
                t, val, l = parse_packet(subpackets[offset:])
                # print('t, val, l', t, val, l)
                subpackets_parsed.append((t, val))
                offset += l
                # print(i, 'offset is', offset)
                if offset == len(subpackets):
                    break
            offset += 7 + 15
        else:
            subpacket_number = int(packet[7:7+11], 2)
            subpacket = packet[18:]
            # print('subpacket_number count', subpacket_number)
            for i in range(subpacket_number):
                # print('subpacket', i, '...')
                t, val, l = parse_packet(subpacket[offset:])
                # print(f'IS IT HERE? i={i} t={t}, val={val}, l={l}')
                subpackets_parsed.append((t, val))
                offset += l
            # print('parsed for return...', subpackets_parsed)
            offset += 7 + 11
        return (version, type_id), subpackets_parsed, offset



def try_example(id, datum):
    print('\n\nEXAMPLE', id)
    t, val, l = parse_packet(binify(datum))
    print(t, val)


def p1():
    # try_example('0', 'D2FE28')
    # try_example('1', '38006F45291200')
    # try_example('2', 'EE00D40C823060')
    # try_example('list 1', '8A004A801A8002F478')
    # try_example('list 2', '620080001611562C8802118E34')
    # try_example('list 3', 'C0015000016115A2E0802F182340')
    # try_example('list 4', 'A0016C880162017C3686B18A3D4780')
    # try_example('real', bin_data)
    struct = parse_packet(bin_data)
    all_headers = re.findall('\((\d+, \d+)\)', str(struct))
    # print(all_headers)
    return sum([int(x.split(', ')[0]) for x in all_headers])


def evaluate(d):
    print('\ncalled with:', d)

    version, packet_id  = d[0]
    # print(version, packet_id, '\n')
    data = d[1:][0]
    # for p in data:
    #     print(p)

    match packet_id:
        case 0:
            asdf = [evaluate(p) for p in data]
            print('sum', asdf)
            return sum(asdf)
        case 1:
            return prod([evaluate(p) for p in data])
        case 2:
            return min([evaluate(p) for p in data])
        case 3:
            return max([evaluate(p) for p in data])
        case 4:
            print('literal', data, 'return:', data)
            return data
        case 5:
            return 1 if evaluate(data[0]) > evaluate(data[1]) else 0
        case 6:
            return 1 if evaluate(data[0]) < evaluate(data[1]) else 0
        case 7:
            return 1 if evaluate(data[0]) == evaluate(data[1]) else 0


def p2():
    struct = parse_packet(bin_data)
    return evaluate([struct[0], struct[1]])


cnv = {'0': '0000', '1': '0001', '2': '0010', '3': '0011',
       '4': '0100', '5': '0101', '6': '0110', '7': '0111',
       '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
       'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}


def binify(d):
    return ''.join([cnv[c] for c in d])


day = 16
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = file.read().strip()
    # print('data', data, '\n')
    bin_data = binify(data)

print(f'part1: {p1()}')
print(f'part2: {p2()}')
