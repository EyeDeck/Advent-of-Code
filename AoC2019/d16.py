import sys
# import numpy as np


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


def run_fft_naive(message, pattern):
    inp_len = len(message)
    last = message.copy()
    for i in range(100):
        new = [0 for _ in range(inp_len)]
        for j in range(len(message)):
            this_pattern = get_pattern_for_internal(pattern, j+1, inp_len)
            calced = 0
            for k in range(inp_len):
                # print('\t', k, new)# , this_pattern)
                # input()
                # next_int = str()[-1:]
                # print('next_int', next_int)
                calced += last[k]*this_pattern[k]
                # print(calced)
            new[j] = int(str(calced)[-1:])
            # print('\t', new)
            # input()
        last = new
        # print(str(i).zfill(3), '=', last)
    return last


def run_fft_for(message, index):
    inp_len = len(message)
    last = message.copy()
    for i in range(100):
        new = last[:]
        for j in range(inp_len-2, index-1, -1):
            # input(new[-20:])
            new[j] = (last[j] + last[j+1]) % 10
            # print(j, inp_len, new[j])

            # if j >= inp_len//2:
            #      print(calced, this_components)
            # new[j] = abs(calced) % 10
            # print(new[j])
        last = new
        # print(str(i).zfill(3), '=', last)
    return last


def run_fft_for_last_half(message, index):
    inp_len = len(message)
    assert index > inp_len // 2
    last = message.copy()

    for i in range(100):
        # print(i)
        #new = last[:]
        new = [0]*inp_len
        new[-1] = last[-1]
        # print(last)
        for j in range(inp_len-2, index-1, -1):
            # input()
            new[j] = (new[j] + (last[j] + new[j+1])) % 10
            # print(last[j], last[j+1], new[-20:])
            # input()
            # print(j, inp_len, new[j])

            # if j >= inp_len//2:
            #      print(calced, this_components)
            # new[j] = abs(calced) % 10
            # print(new[j])
        last = new
        # print(str(i).zfill(3), '=', last)
    return last


f = 'd16.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

inp = [int(c) for c in open(f).read()]
pattern = (0, 1, 0, -1)
print('inp =', inp)

# for i in range(1):
#      inp[i] = 0
# print(inp)

p1 = run_fft_naive(inp, pattern)
print(p1)
p1 = int(''.join([str(c) for c in p1[:8]]))
print(p1)

#p2 = run_fft_for_last_half(inp, len(inp)//2+3)
#sys.exit()

p2_inp = inp*10000
# p2 = p2[int(''.join([strinp[:7]))]
p2_index = sum([v*pow(10, i) for i,v in enumerate(reversed(inp[:7]))])
print(p2_index)
p2 = run_fft_for_last_half(p2_inp, p2_index)
# print(p2)
# print(p2[p2_index:p2_index+8])
print(int(''.join([str(c) for c in p2[p2_index:p2_index+8]])))

