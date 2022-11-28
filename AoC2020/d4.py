import sys
import re


def validate_passport(p):
    for key in 'byr iyr eyr hgt hcl ecl pid'.split():
        if key not in p:
            return False
    return True


def validate_passport2(p):
    if not validate_passport(p):
        return False

    byr = int(p['byr'])
    if byr < 1920 or byr > 2002:
        return False

    iyr = int(p['iyr'])
    if iyr < 2010 or iyr > 2020:
        return False

    eyr = int(p['eyr'])
    if eyr < 2020 or eyr > 2030:
        return False

    hgt_type = p['hgt'][-2:]
    if hgt_type not in {'in', 'cm'}:
        return False

    hgt = int(p['hgt'][:-2])
    if hgt_type == 'in':
        if hgt < 59 or hgt > 76:
            return False
    else:
        if hgt < 150 or hgt > 193:
            return False

    if len(re.findall('(#[0-9a-f]{6})', p['hcl'])) != 1:
        return False

    if p['ecl'] not in 'amb blu brn gry grn hzl oth'.split():
        return False

    if len(re.findall('(^[0-9]{9}$)', p['pid'])) != 1:
        return False

    return True


f = 'd4.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.replace('\n', ' ') for line in file.read().split('\n\n')]
passports = [{thing[0]:thing[1] for thing in [entry.split(':') for entry in line.split()] if len(thing) == 2} for line in data]

p1 = 0
for passport in passports:
    if validate_passport(passport):
        p1 += 1
print(f'part1: {p1}')

p2 = 0
for passport in passports:
    if validate_passport2(passport):
        p2 += 1
print(f'part2: {p2}')
