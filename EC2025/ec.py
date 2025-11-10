import sys

INF = sys.maxsize

_QUEST = None


def setquest(n):
    global _QUEST
    assert isinstance(n, int), 'quest must be int, not %s' % (type(n),)
    assert n > 0, 'you forgot to set the quest again!'
    assert _QUEST is None, 'setquest() multiple times'
    _QUEST = n


class open_default(object):
    def __init__(self, n):
        if len(sys.argv) > 1:
            self.fn = sys.argv[1]
        else:
            self.fn = f'q{_QUEST}_{n}.txt'

    def __enter__(self):
        self.file = open(self.fn)
        return self.file

    def __exit__(self, *args):
        self.file.close()


def parselines(n, func=None):
    with open_default(n) as file:
        if func:
            return [func(line.strip()) for line in file]
        else:
            return [line.strip() for line in file]


def parsedouble(n):
    with open_default(n) as file:
        return file.read().split('\n\n')