import sys

f = 'd8.txt'
width = 25
length = 6
if len(sys.argv) > 1:
    f = sys.argv[1]
if len(sys.argv) > 3:
    width = int(sys.argv[2])
    length = int(sys.argv[3])

inp = open(f).read()

size = width * length
ln = len(inp) // size
layers = []
for i in range(0, ln):
    layers.append([p for p in inp[(i*size):((i+1)*size)]])
best = []
best_ct = 1000000
for layer in layers:
    zeros = layer.count('0')
    if zeros < best_ct:
        best = layer
        best_ct = zeros

print(best.count('1') * best.count('2'))

board = [c for c in '.' * size]

for layer in reversed(layers):
    for i, pixel in enumerate(layer):
        if pixel == '0':
            board[i] = ' '
        if pixel == '1':
            board[i] = '#'

render = []
for i, pixel in enumerate(board):
    render.append(pixel)
    if (i+1) % width == 0:
        render.append('\n')
print(''.join(render))
