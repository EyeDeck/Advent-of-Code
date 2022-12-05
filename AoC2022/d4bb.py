import random

random.seed(20221204)

with open('d4bb.txt', 'w', newline='\n') as f:
    for i in range(100000):
        rs = [random.randint(0, 1000000000000000000000000000) for _ in range(4)]
        l,r = sorted(rs[:2]), sorted(rs[2:])
        f.write(f'{l[0]}-{l[1]},{r[0]}-{r[1]}\n')
