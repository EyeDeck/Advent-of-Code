from aoc import *

setday(25)

states = defaultdict(dict)
state = None
steps = None

with open_default() as file:
    chunks = [[line.strip().strip(':.').split() for line in chunk.split('\n')] for chunk in file.read().split('\n\n')]
    state = chunks[0][0][-1]
    steps = int(chunks[0][1][-2])

    for chunk in chunks[1:]:
        chunk_state = {}
        st = chunk[0][-1][0]
        for n in (1,5):
            b = int(chunk[n][-1])
            v = int(chunk[n+1][-1])
            dir = 1 if chunk[n+2][-1] == 'right' else -1
            n_st = chunk[n+3][-1]
            chunk_state[b] = (v,dir,n_st)
        states[chunk[0][-1]] = chunk_state


tape = defaultdict(int)
pointer = 0

for step in range(steps):
    action = states[state][tape[pointer]]
    tape[pointer] = action[0]
    pointer += action[1]
    state = action[2]

print(sum(i for i in tape.values()))