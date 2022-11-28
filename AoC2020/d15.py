import sys


def get_at(num):
    last_times = {v: k+1 for k, v in enumerate(data)}
    last_spoken = data[-1]
    for i in range(len(data), num):
        to_say = 0 if last_spoken not in last_times else i-last_times[last_spoken]
        last_times[last_spoken] = i
        last_spoken = to_say
    return last_spoken


data = '9,3,1,0,8,4'
if len(sys.argv) > 1:
    data = sys.argv[1]

data = [int(i) for i in data.split(',')]

print(f'part1: {get_at(2020)}')
print(f'part2: {get_at(30000000)}')
