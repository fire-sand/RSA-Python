import sys

from datatypes import WORD_SIZE, Word, breakup, Nat
from random import randint

print "WORD_SIZE size is: {}".format(WORD_SIZE)


for _ in xrange(1000):
    z_nat = Nat()
    x, y = randint(0, 10000000), randint(0, 10000000)
    x_nat, y_nat = Nat(x), Nat(y)

    assert int(x_nat) == x
    assert int(y_nat) == y
    assert z_nat.add(x_nat, y_nat) == Nat(x + y)
    assert int(z_nat) == x + y

x = Nat(100)
y = Nat(100)
z = Nat(101)
s = {x, y, z}
assert len(s) == 2


def mod_inverse(x, w):
    y = [0, 1]
    for i in xrange(2, w + 1):
        if pow(2, i - 1) < ((x * y[i - 1]) % pow(2, i)):
            y.append(y[i - 1] + pow(2, i - 1))
        else:
            y.append(y[i-1])

    return (y[w] ^ (2**w - 1)) + 1

def extended_gcd(a, b):
    """Returns x,y such that a*x + b*y = gcd(a,b).

    In our typical usage, gcd(a, b) should always be 1. Uses the extended
    euclidean algorithm as described here:
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        q = old_r / r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    if old_r != 1:
        raise Exception('invalid: gcd != 1')

    # TODO: check for more cases(?)
    if old_s < 0 and old_t > 0:
        print old_s, b
        print old_t, a
        old_s += b
        old_t -= a

    return old_s, old_t


def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y


def mon_pro(a, b, n_prime, n, r):
    t = a * b
    m = (t * n_prime) % r
    u = (t + m * n) / r
    return u - n if u >= n else u


# r_inv = 169
n = 589
a = 199
b = 300
n_nat = Nat(n)
r = 2**(len(n_nat)*WORD_SIZE)

# r_inv, n_inv = extended_gcd(r, n)
# print 'here', r_inv, n_inv
_, r_inv, n_inv = egcd(r, n)
n_inv = ((r * r_inv) - 1) / n

print 'n_inv', n_inv
n_0 = n_inv % 2**WORD_SIZE # mod_inverse(n, WORD_SIZE)

n_0 = mod_inverse(n, WORD_SIZE)
print n_0

n_0_nat = Word(n_0)
assert int(n_0_nat) == n_0
a_nat = Nat(a, size=len(n_nat))
b_nat = Nat(b, size=len(n_nat))


print 'expected:', mon_pro(a, b, n_inv, n, r)
print 'should be:', (a * b * r_inv) % n
print 'actual:', int(z._mon_pro(a_nat, b_nat, n_0_nat, n_nat))
print 'actual:', z._mon_pro(a_nat, b_nat, n_0_nat, n_nat)

print 'mod_exp:', int(z.mod_exp(a, b, n))
print 'mod_exp:', z.mod_exp(a, b, n)
