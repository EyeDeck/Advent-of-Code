import hashlib


def p1(salt):
    for i in range(1000000000):
        s = salt + str(i)
        md5 = hashlib.md5()
        md5.update(s.encode())
        out = md5.hexdigest()
        if out[0:5] == '00000':
            print(out)
            print(s)
            return i


def p2(salt):
    for i in range(1000000000):
        s = salt + str(i)
        md5 = hashlib.md5()
        md5.update(s.encode())
        out = md5.hexdigest()
        if out[0:6] == '000000':
            print(out)
            print(s)
            return i


salt = 'yzbqklnj'

print(p1(salt))
print(p2(salt))
