from ec import *


def p1():
    data = parse_lines(1)
    t_data = defaultdict(int)
    for line in data:
        i, q, p, t = [int(x.split('=')[1]) for x in line.split()]
        print(i,q,p,t)
        t_data[i] += t

    acc = 0
    for i, k in enumerate(sorted(t_data, key=t_data.get)):
        print(k, t_data[k])
        acc += (i+1) * t_data[k]

    return acc


def p2():
    data = parse_lines(2)
    t_data = defaultdict(lambda: [100, 0])
    for line in data:
        i, q, p, t = [int(x.split('=')[1]) for x in line.split()]
        print(i,q,p,t)
        t_data[i][0] -= 1
        t_data[i][1] += t

    acc = 0
    for i, k in enumerate(sorted(t_data, key=t_data.get)):
        print(k, t_data[k])
        acc += (i+1) * t_data[k][1]

    return acc


def p3():
    data = parse_lines(3)
    data = [[int(x.split('=')[1]) for x in line.split()] for line in data]

    data.sort(key=lambda x: x[3])
    data.sort(key=lambda x: x[2])
    data.sort(key=lambda x: x[1])

    print(data)

    q_times_running = defaultdict(int)
    last_q = 0
    for line in data:
        print(f'id={line[0]} quest={line[1]} part={line[2]} time={line[3]}')
        i, q, p, t = line
        if last_q != q:
            q_times_running = defaultdict(int)
        last_q = q
        line[3] += q_times_running[i]
        q_times_running[i] += t
        print(q_times_running)

    data.sort(key=lambda x: x[3])
    data.sort(key=lambda x: x[2])
    data.sort(key=lambda x: x[1])

    print('after adjustment...')
    for line in data:
        print(f'id={line[0]} quest={line[1]} part={line[2]} time={line[3]}')

    t_data = defaultdict(int)
    last_q = 0
    last_p = 0
    last_t = INF
    remaining = 0
    index = 0
    for line in data:
        # print(f'id={line[0]} quest={line[1]} part={line[2]} time={line[3]}')
        i, q, p, t = line
        if q != last_q or p != last_p:
            print(f'\nQuest {q}, Part {p}:')
            remaining = p * 50
            index = 0
            last_t = INF
        index += 1
        if last_t == t:
            pass
        elif last_t < t:
            remaining = (p * 50) - (index-1)

        points = max(0,remaining)
        t_data[i] += points
        if points > 0:
            print(f'id={i}, time={t}, points={points}')

        last_q, last_p, last_t = q, p, t

    print('\nFinal Ranking:')
    acc = 0
    last_i = 0
    last_v = 0
    for i, v in enumerate(sorted(t_data.values(), reverse=True)):
        if v != last_v:
            last_i = i

        checksum_add = (last_i + 1) * v
        acc += checksum_add

        last_v = v

        print(f'{last_i+1}. points={v}, (added {checksum_add}, running={acc})')

    return acc


if __name__ == '__main__':
    setquest(4)

    print('part1:', p1())
    print('part2:', p2())
    print('part3:', p3())
