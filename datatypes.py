# Environment
WORD_SIZE = 2
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

    def _mon_pro(self, a, b, n_0, n):
        self.words = []

        S = len(n)

        t = Nat(size=(2 * S + 1))
        for i in xrange(S):
            c = Word(0)
            for j in xrange(S):
                # Broke up this addition to handle separate carries
                c1, s = a.words[j].mul(b.words[i])
                c2, s = t.words[i + j].add(s)
                c3, s = s.add(c)

                t.words[i + j] = s

                # Handle the carries
                _, c = c1.add(c2)
                _, c = c.add(c3)

            t.words[i + S] = c

        for i in xrange(S):
            c = Word(0)
            _, m = t.words[i].mul(n_0)  # mod 2^w is the same as ignoring carry
            for j in xrange(S):

                # Broke up this addition to handle separate carries
                c1, s = m.mul(n.words[j])
                c2, s = t.words[i + j].add(s)
                c3, s = s.add(c)

                t.words[i + j] = s

                # Handle the carries
                _, c = c1.add(c2)
                _, c = c.add(c3)

            for j in xrange(i + S, 2 * S):
                c, s = t.words[j].add(c)
                t.words[j] = s

        t.words[2 * S] = c

        u = Nat(size=(S + 1))
        for j in xrange(S + 1):
            u.words[j] = Word(int(t.words[j + S]))

        # Didn't implement comparison/subtraction yet
        u_int = int(u)
        n_int = int(n)
        if u_int >= n_int:
            return Nat(u_int - n_int)
        else:
            return Nat(u_int)

    def mod_exp(self, M, e, n):
        n_ = (1 / float(n)) % r
        M_bar = (M * r) % n
        x_bar = r % n
        for bit in bin(e)[2:]:
            x_bar = self._mon_pro(x_bar, x_bar, n_, r)
            if bit == '1':
                x_bar = self._mon_pro(M_bar, x_bar, n_, r)
        return self._mon_pro(x_bar, Nat(1), n_, r)
