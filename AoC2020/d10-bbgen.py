import random
rand = random.Random(0)  # set seed
with open("d10bb.txt", "w") as f:
    n = 0
    for _ in range(100_000):
        n += 1 + rand.randint(0, 1) * 2
        f.write(str(n) + "\n")
