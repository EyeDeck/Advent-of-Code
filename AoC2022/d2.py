import sys

LOSS = 0
DRAW = 3
WIN = 6

scores = {
    ('A', 'X'): 1 + DRAW,
    ('B', 'X'): 1 + LOSS,
    ('C', 'X'): 1 + WIN,
    ('A', 'Y'): 2 + WIN,
    ('B', 'Y'): 2 + DRAW,
    ('C', 'Y'): 2 + LOSS,
    ('A', 'Z'): 3 + LOSS,
    ('B', 'Z'): 3 + WIN,
    ('C', 'Z'): 3 + DRAW,
}

conversion = {
    ('A', 'X'): ('A', 'Z'),
    ('B', 'X'): ('B', 'X'),
    ('C', 'X'): ('C', 'Y'),
    ('A', 'Y'): ('A', 'X'),
    ('B', 'Y'): ('B', 'Y'),
    ('C', 'Y'): ('C', 'Z'),
    ('A', 'Z'): ('A', 'Y'),
    ('B', 'Z'): ('B', 'Z'),
    ('C', 'Z'): ('C', 'X'),
}


day = 2
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [tuple(line.strip().split(' ')) for line in file]

print(f'part1: { sum(scores[line] for line in data) }')
print(f'part2: { sum(scores[conversion[line]] for line in data) }')
