import sys
import logging
from itertools import groupby
from functools import cmp_to_key


def p1():
    acc = 0
    for i, (a, b) in enumerate(data_p1):
        logging.debug('\n== Pair %s ==', i+1)  # '\na:%s\n  b:%s', i + 1, a, b)
        result = rwalk(a, b) == -1
        logging.debug(f"result: {'in the right order' if result else 'not'}")
        if result:
            acc += i + 1
    return acc


def rwalk(a, b, depth=0):
    padding = depth * '  '
    logging.debug('%s- Compare %s vs %s', padding, a, b)

    if type(a) == type(b):              # same type
        if isinstance(a, int):              # both ints
            if a == b:
                return 0
            else:
                result = -1 if a <= b else 1
                logging.debug('%s %s (int <= int): %s | %s', padding, result, a, b)
                return result
        else:                               # both lists
            for x, y in zip(a, b):
                result = rwalk(x, y, depth+1)
                if result != 0:
                    logging.debug('%s %s (zip)', padding, result)
                    return result
            if len(a) == len(b):
                return 0
            else:
                result = -1 if len(a) < len(b) else 1
                logging.debug('%s %s (list/list length)', padding, result)
                return result
    else:                               # different type (presumably list/int)
        if isinstance(b, list):
            a = [a]
        else:
            b = [b]
        result = rwalk(a, b, depth+1)
        if result != 0:
            logging.debug('%s %s (list/int): %s | %s', padding, result, a, b)
            return result

    return 0


def p2():
    data_p2.sort(key=cmp_to_key(rwalk))
    return (data_p2.index(div[0]) + 1) * (data_p2.index(div[1]) + 1)


day = 13
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

logger = logging.getLogger()
logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.DEBUG)
if '-d' not in sys.argv:
    logger.disabled = True

whitelist = {str(i) for i in range(10)} | {'[', ']', ',', ' ', '\n'}

with open(f) as file:
    data = [line.strip() for line in file if set(line) <= whitelist]

data_p1 = [[eval(packet) for packet in list(g)] for k, g in groupby(data, lambda x: x != '') if k]

data_p2 = [eval(packet) for packet in data if packet != '']
div = [[2]], [[6]]
data_p2.extend(div)

print(f'part1: {p1()}')
logger.disabled = True
print(f'part2: {p2()}')
