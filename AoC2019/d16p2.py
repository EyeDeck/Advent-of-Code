import sys
# import numpy as np


#inp = [int(c) for c in '80871224585914546619083218645595']

# erase board
# print('\x1b[200B\x1b[200C\x1b[1J\x1b[1;1H')  # down 200, right 200, erase 1,1->cursor, set cursor 1,1

# cursor up
# print('\x1b[{};1B'.format(up))



# get_pattern_for_returns = {}
# def get_pattern_for(pattern, index, length):
#     t = (pattern, index, length)
#     if t in get_pattern_for_returns:
#         return get_pattern_for_returns[t]
#     else:
#         r = get_pattern_for_internal(pattern, index, length)
#         get_pattern_for_returns[t] = r
#         return r
#
#
# def get_pattern_for_internal(pattern, index, length):
#     start = [item for sublist in [[v]*index for v in pattern] for item in sublist]
#     intermediate = start
#     while len(intermediate) < length + 1:
#         intermediate.extend(start)
#     return intermediate[1:length+1]


def run_fft(message):
    last = message.copy()
    for i in range(100):
        new = last[:]
        for j in range(inp_len):
            k = j
            step = j + 1
            calced = 0

            while k < inp_len:
                calced += sum(last[k:k+step])
                k += 2*step

                calced -= sum(last[k:k+step])
                k += 2 * step
            new[j] = abs(calced) % 10

        last = new
    return last

f = 'd16.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(c) for c in open(f).read()]
inp_len = len(inp)
pattern = (0, 1, 0, -1)
print('inp =', inp)

# for i in range(1):
#      inp[i] = 0
# print(inp)

p1 = run_fft(inp)
# print(p1)
p1 = int(''.join([str(c) for c in p1[:8]]))
print(p1)

p2_inp = inp*10000
# p2 = p2[int(''.join([strinp[:7]))]
p2_inp = p2_inp[sum([v*pow(10, i) for i,v in enumerate(reversed(inp[:7]))]):]
# inp2_len = len(p2_inp)
#
# for i in range(100):
#     for j in range(inp2_len-2, -1, -1):
#         p2_inp[j] += p2_inp[j + 1]
#         p2_inp[j] %= 10

# p2 = run_fft(p2_inp)
# p2index = [v*pow(10, i) for i,v in enumerate(reversed(p2_inp[:8]))]
# print(sum(p2index))
