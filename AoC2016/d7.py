from aoc import *


def p1():
    def has_abba(s):
        return bool(re.findall(r"((\w)(?!\2)(.)\3\2)", s))

    def check_tls(s):
        for ht in re.findall(r'\[.*?]', s):
            # print(s, ht, '\n')
            if has_abba(ht):
                return False
        return has_abba(re.sub(r"\[.*?]", "|", s))

    return len([True for s in data if check_tls(s)])


def p2():
    def get_babs(s):
        r = []
        for ht in re.findall(r'\[.*?]', s):
            r.extend([m[0] for m in re.findall(r"(?=((\w)(?!\2).\2))", ht)])
        return r

    def get_abas(s):
        return [m[0] for m in re.findall(r"(?=((\w)(?!\2).\2))", re.sub(r"\[.*?]", "|", s))]

    def check_ssl(s):
        abas = get_abas(s)
        babs = get_babs(s)
        # print(f"{s}\n{abas}\n{babs}\n")
        for aba in abas:
            if aba[1] + aba[0] + aba[1] in babs:
                return True
        return False

    return len([True for s in data if check_ssl(s)])


day = 7
f = f'd{day}.txt'
if len(sys.argv) > 1:
    f = sys.argv[1]

with open(f) as file:
    data = [line.strip() for line in file]

# a perfect problem for a bunch of evil regex >:)
print(f'part1: {p1()}')
print(f'part2: {p2()}')
