import sys
import numpy as np


#inp = [int(c) for c in '80871224585914546619083218645595']

# erase board
# print('\x1b[200B\x1b[200C\x1b[1J\x1b[1;1H')  # down 200, right 200, erase 1,1->cursor, set cursor 1,1

# cursor up
# print('\x1b[{};1B'.format(up))



get_pattern_for_returns = {}
def get_pattern_for(pattern, index, length):
    t = (pattern, index, length)
    if t in get_pattern_for_returns:
        return get_pattern_for_returns[t]
    else:
        r = get_pattern_for_internal(pattern, index, length)
        get_pattern_for_returns[t] = r
        return r


def get_pattern_for_internal(pattern, index, length):
    start = [item for sublist in [[v]*index for v in pattern] for item in sublist]
    intermediate = start
    while len(intermediate) < length + 1:
        intermediate.extend(start)
    return intermediate[1:length+1]


def run_fft(message, pattern):
    inp_len = len(message)
    last = message.copy()
    for i in range(100):
        new = [0 for _ in range(inp_len)]
        for j in range(len(message)):
            this_pattern = get_pattern_for_internal(pattern, j+1, inp_len)
            calced = 0
            for k in range(inp_len):
                # print(k, inp, this_pattern)
                # next_int = str()[-1:]
                # print('next_int', next_int)
                calced += last[k]*this_pattern[k]
                # print(calced)
            new[j] = int(str(calced)[-1:])
            # print(new[j])
        last = new
        print(i, '=', last)
    return last

f = 'd16.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(c) for c in open(f).read()]
pattern = (0, 1, 0, -1)

p1 = run_fft(inp, pattern)
p1 = int(''.join([str(c) for c in p1[:8]]))
print(p1)

p2_inp = []
for _ in range(10000):
    p2_inp.extend(inp)
    # print(p2_inp)
print('p2 calculated')

p2 = run_fft(p2_inp, pattern)
print(p2)
