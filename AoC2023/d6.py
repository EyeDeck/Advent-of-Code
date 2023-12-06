from aoc import *

def p1():
    races = []
    times = [int(i) for i in data[0].split(':')[1].strip().split()]
    dists = [int(i) for i in data[1].split(':')[1].strip().split()]
    for i in range(len(times)):
        races.append((times[i], dists[i]))

    m_acc = 1
    for race in races:
        time, dist = race
        acc = 0
        for i in range(time):
            if check_win(i, time, dist):
                acc += 1
        m_acc *= acc
    return m_acc

def check_win(hold, time, dist):
    return (hold + ((time - hold - 1) * hold)) > dist

def p2():
    time = int(''.join(data[0].split(':')[1].split()))
    dist = int(''.join(data[1].split(':')[1].split()))
    print(time, dist)

    search_min = 0
    search_max = time
    while True:
        middle = (search_min + search_max) // 2
        wins = check_win(middle, time, dist)
        if wins:
            search_min = middle + 1
        else:
            search_max = middle - 1
        print(middle, wins, search_min, search_max)
        if search_min >= search_max:
            break
    upper = search_min
    upper += 2
    while not check_win(upper, time, dist):
        print(upper, check_win(upper, time, dist))
        upper -= 1
    print('upper', upper)

    search_min = 0
    search_max = time
    while True:
        middle = (search_min + search_max) // 2
        wins = check_win(middle, time, dist)
        if wins:
            search_max = middle - 1
        else:
            search_min = middle + 1
        print(middle, wins, search_min, search_max)
        if search_min >= search_max:
            break
    lower = search_max
    lower -= 2
    while not check_win(lower, time, dist):
        print(lower, check_win(lower, time, dist))
        lower += 1
    print('lower', lower)

    return upper-lower+1


setday(6)

data = parselines()

print('part1:', p1() )
print('part2:', p2() )
