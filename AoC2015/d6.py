import sys
import re
import numpy as np
from collections import defaultdict  # defaultdict(int)
from PIL import Image, ImageDraw, ImageFont


def p1():
    lights = np.ndarray((1000, 1000), dtype=bool)
    # lights[0,0] = True
    # print(lights)
    # print(lights[1:1])
    for lct, line in enumerate(data):
        x1, y1 = (int(n) for n in line[-3].split(','))
        x2, y2 = (int(n) for n in line[-1].split(','))
        if line[0] == 'turn':
            v = False
            if line[1] == 'on':
                v = True
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    lights[i, j] = v

        elif line[0] == 'toggle':
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    lights[i, j] = not lights[i, j]

        if draw_p1:
            img = Image.fromarray(lights)
            draw = ImageDraw.Draw(img)
            draw.text(xy=(0, 0), text=' '.join(line) + f'  sum:{np.sum(lights)}', fill='red') #, font=fnt)
            img.save('d6\\' + str(lct).zfill(4) + '.png')
    return np.sum(lights)


def p2(scale=4):
    lights = np.ndarray((1000, 1000), dtype=np.int8)
    # lights[0,0] = True
    # print(lights)
    # print(lights[1:1])
    for lct, line in enumerate(data):
        x1, y1 = (int(n) for n in line[-3].split(','))
        x2, y2 = (int(n) for n in line[-1].split(','))
        if line[0] == 'turn':
            v = -scale
            if line[1] == 'on':
                v = scale
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    lights[i, j] = max(0, lights[i, j] + v)

        elif line[0] == 'toggle':
            for i in range(x1, x2+1):
                for j in range(y1, y2+1):
                    #lights[i, j] = not lights[i, j]
                    lights[i, j] += scale*2

        if draw_p2:
            img = Image.fromarray(lights, 'L')
            draw = ImageDraw.Draw(img)
            draw.text(xy=(0, 0), text=' '.join(line) + f'  sum:{np.sum(lights)}', fill='red') #, font=fnt)
            img.save('d6\\' + str(lct).zfill(4) + '.png')
    return np.sum(lights) // scale


f = 'd6.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip().split(' ') for line in file]

draw_p1 = '--draw-p1' in sys.argv
draw_p2 = '--draw-p2' in sys.argv

print(f'part1: {p1()}')
print(f'part2: {p2(1)}')
