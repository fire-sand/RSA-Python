# Environment
WORD_SIZE = 8
HALF_WORD_SIZE = WORD_SIZE / 2
LOWER_HALF_WORD_MASK = (1 << HALF_WORD_SIZE) - 1
UPPER_HALF_WORD_MASK = LOWER_HALF_WORD_MASK << HALF_WORD_SIZE


def size(num):
    return num.bit_length()


def binary(i):
    return format(i, '0{}b'.format(WORD_SIZE))


def breakup(i, s):
    for j in xrange(len(i), 0, -s):
        if j < s:
            yield i[:j]
        else:
            yield i[j - s:j]


class Word(object):

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

    def mul(self, other):
        a = self.word
        b = other.word

        a_l = a & LOWER_HALF_WORD_MASK
        b_l = b & LOWER_HALF_WORD_MASK
        x = a_l * b_l
        s0 = x & LOWER_HALF_WORD_MASK

        a_h = a >> HALF_WORD_SIZE
        x_h = x >> HALF_WORD_SIZE
        x = a_h * b_l + x_h
        s1 = x & LOWER_HALF_WORD_MASK
        s2 = x >> HALF_WORD_SIZE

        b_h = b >> HALF_WORD_SIZE
        x = s1 + a_l * b_h
        s1 = x & LOWER_HALF_WORD_MASK

        x_h = x >> HALF_WORD_SIZE
        x = s2 + a_h * b_h + x_h
        s2 = x & LOWER_HALF_WORD_MASK
        s3 = x >> HALF_WORD_SIZE

        prod = s1 << HALF_WORD_SIZE | s0
        c = s3 << HALF_WORD_SIZE | s2

        return (Word(c), Word(prod))


class Nat(object):

    powers = [2**i for i in xrange(WORD_SIZE + 1)]

    def __init__(self, n=0, size=0):
        self.words = []
        if n:
            n = int(n)
            num = binary(n)
            self.words = [Word(x, 2) for x in breakup(num, WORD_SIZE)]

        if size or size > len(self.words):
            for _ in xrange(len(self.words), size):
                self.words.append(Word(0))

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

    def __int__(self):
        ret = 0
        for w in reversed(self.words):
            ret <<= WORD_SIZE
            ret += int(w)
        return ret

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

    def rsh(self, n):
        for _ in xrange(min(n, len(self))):
            self.words.pop(0)

        return self

    def _pad_words(self, n):
        for _ in xrange(len(self.words), n):
            self.words.append(Word(0))

    def _mon_pro(self, a, b, n_0, n):
        self.words = []

        s = len(n)
        a._pad_words(s)
        b._pad_words(s)

        self._pad_words(2*s + 1)
        t = self
        for i in xrange(s):
            C = Word(0)
            for j in xrange(s):
                # Broke up this addition to handle separate carries
                C1, S = a.words[j].mul(b.words[i])
                C2, S = t.words[i + j].add(S)
                C3, S = S.add(C)

                t.words[i + j] = S

                # Handle the carries
                _, C = C1.add(C2)
                _, C = C.add(C3)

            t.words[i + s] = C

        for i in xrange(s):
            C = Word(0)
            _, m = t.words[i].mul(n_0)  # mod 2^w is the same as ignoring carry
            for j in xrange(s):

                # Broke up this addition to handle separate carries
                C1, S = m.mul(n.words[j])
                C2, S = t.words[i + j].add(S)
                C3, S = S.add(C)

                t.words[i + j] = S

                # Handle the carries
                _, C = C1.add(C2)
                _, C = C.add(C3)

            for j in xrange(i + s, 2 * s):
                C, S = t.words[j].add(C)
                t.words[j] = S

        t.words[2 * s] = C

        u = t.rsh(s)

        # Didn't implement comparison/subtraction yet
        u_int = int(u)
        n_int = int(n)
        if u_int >= n_int:
            ret = Nat(u_int - n_int)
        else:
            ret = Nat(u_int)

        self.words = ret.words
        return self

    def _mod_inverse(self, x):
        y = [0, 1]
        w = WORD_SIZE
        for i in xrange(2, w + 1):
            if self.powers[i - 1] < ((x * y[i - 1]) % self.powers[i]):
                y.append(y[i - 1] + self.powers[i - 1])
            else:
                y.append(y[i - 1])

        return (y[w] ^ (self.powers[w] - 1)) + 1

    def mod_exp(self, M, e, n):
        n_ = Word(self._mod_inverse(n))
        n_nat = Nat(n)

        # These 3 lines are still kind of hard
        r = 2**(len(n_nat) * WORD_SIZE)
        M_bar = Nat((M * r) % n)
        x_bar = Nat(r % n)

        for ei in bin(e)[2:]:
            x_bar = Nat()._mon_pro(x_bar, x_bar, n_, n_nat)
            if ei == '1':
                x_bar = Nat()._mon_pro(M_bar, x_bar, n_, n_nat)

        return self._mon_pro(x_bar, Nat(1), n_, n_nat)
