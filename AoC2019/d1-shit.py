import sys
import os
import re
import numpy as np
import heapq
import copy
import string
import collections
# deque, defaultdict

from PIL import Image
from operator import itemgetter

# inputHandle = open("d1.txt")
# inp = inputHandle.read()
# inputHandle.close()

inp = open("d1.txt").readlines()
# inp.split()
print(inp)

base = [int(i)//3-2 for i in inp]
basefuel = sum(base)
print("p1:", basefuel)

extra = 0
for v in base:
    while (v := v//3-2) > 0:
        extra += v

print("p2:", basefuel + extra)
