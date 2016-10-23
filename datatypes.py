# Environment
_B = 4

def size(num):
    return num.bit_length()

def binary(i):
    return format(i, '04b')

def breakup(i, s):
    for j in xrange(len(i), 0, -s):
        if j < s:
            yield i[:j]
        else:
            yield i[j-s:j]


class Word(object):

    word = None

    def __init__(self, w, base=10):
        w = int(str(w), base) # Make sure w is an int
        if w < 0:
            raise Exception("Error: Negative input")

        if size(w) > _B:
            raise Exception("Error: Overflow with w: {}".format(w))

        self.word = w

    def __str__(self):
        return binary(self.word)

    def __int__(self):
        return self.word


class Nat(object):

    nat = []

    def __init__(self, n):
        n = int(n)
        num = binary(n)
        print num
        self.nat = [Word(x, 2) for x in breakup(num, _B)]
