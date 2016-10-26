# Environment
WORD_SIZE = 4
HALF_WORD_SIZE = WORD_SIZE / 2
LOWER_HALF_WORD_MASK = (1 << HALF_WORD_SIZE) - 1
UPPER_HALF_WORD_MASK = LOWER_HALF_WORD_MASK << HALF_WORD_SIZE


def size(num):
    return num.bit_length()


def binary(i):
    return format(i, '04b')


def breakup(i, s):
    for j in xrange(len(i), 0, -s):
        if j < s:
            yield i[:j]
        else:
            yield i[j - s:j]


class Word(object):

    word = None

    def __init__(self, w, base=10):
        w = int(str(w), base)  # Make sure w is an int
        if w < 0:
            raise Exception("Error: Negative input")

        if size(w) > WORD_SIZE:
            raise Exception("Error: Overflow with w: {}".format(w))

        self.word = w

    def __str__(self):
        return binary(self.word)

    def __int__(self):
        return self.word

    def __nonzero__(self):
        return bool(self.word)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.word == other.word
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(self.word)

    def add(self, other):
        a = self.word
        b = other.word

        a_l = a & LOWER_HALF_WORD_MASK
        b_l = b & LOWER_HALF_WORD_MASK
        lower = a_l + b_l
        lower_carry = lower >> HALF_WORD_SIZE
        lower = lower & LOWER_HALF_WORD_MASK

        a_h = a >> HALF_WORD_SIZE
        b_h = b >> HALF_WORD_SIZE
        upper = a_h + b_h + lower_carry

        c = upper >> HALF_WORD_SIZE
        s = (upper & LOWER_HALF_WORD_MASK) << HALF_WORD_SIZE | lower
        return (Word(c), Word(s))


class Nat(object):

    words = []

    def __init__(self, n=0):
        n = int(n)
        num = binary(n)
        self.words = [Word(x, 2) for x in breakup(num, WORD_SIZE)]

    def __len__(self):
        return len(self.words)

    def __str__(self):
        return str([str(n) for n in self.words])

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.words == other.words
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(self.words))

    def add(self, x, y):
        m = len(x)
        n = len(y)

        if m < n:
            return self.add(y, x)

        self.words = []

        carry = Word(0)
        for i in xrange(n):
            tmp_carry, tmp_sum = x.words[i].add(y.words[i])
            carry, tmp_sum = carry.add(tmp_sum)
            carry = carry or tmp_carry
            self.words.append(tmp_sum)

        for i in xrange(n, m):
            carry, s = carry.add(x.words[i])
            self.words.append(s)

        if carry:
            self.words.append(carry)

        return self
