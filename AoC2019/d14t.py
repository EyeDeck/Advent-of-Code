from collections import defaultdict
import itertools
import math
from hashlib import md5
import msvcrt
#import numpy as np
import os.path
import re
import sys


def get_input(filename=None):
  if not filename:
    filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
  with open(filename) as fp:
    input = fp.read().rstrip()

  reactions = {}
  for line in input.split('\n'):
    match = re.search(r'^((?:\d+ [A-Z]+, )*\d+ [A-Z]+) => (\d+) ([A-Z]+)$', line)
    output_amount = int(match.group(2))
    output = match.group(3)
    inputs = []
    for input in match.group(1).split(', '):
      input_amount, input = input.split(' ')
      inputs.append((int(input_amount), input))
    reactions[output] = (output_amount, inputs)
  return reactions



def part1(reactions):
  return calc_ore(reactions, 'FUEL', 1)


if __name__ == '__main__':
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('input', nargs='?', metavar='input.txt')
  args = parser.parse_args()
  input = get_input(args.input)
  print(input)
