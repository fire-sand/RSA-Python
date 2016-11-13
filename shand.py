import math

from random import choice

p = 1
_B = 2**p

# M is not allowed to be even
# Hardcoded for _B = 4
MUS = [None, 3, None, 1]
# Hardcoded for _B = 2
MUS = [None, 1]


def mon_pro(A, B, M, n):
    P = 0

    a0 = A & (_B - 1)
    m0 = M & (_B - 1)
    mu = MUS[m0]
    for i in xrange(n):
        # Get t'th word of B
        bt = (B >> (i * p)) & (_B - 1)

        # Get 0'th word of P
        p0 = P & (_B - 1)

        # Calculate qt
        qt = (mu * (a0 * bt + p0)) & (_B - 1)

        # Calculate new value of P
        # divide by _B is the same as shift right by p
        # print "big: ", A
        # print "small; ", bt
        # print "big: ", M
        # print "small: ", qt
        P = (A * bt + P + qt * M) >> p
        # print P

    return P

def mon_exp(M, e, n):
    r = 2 ** ((int(math.log(n, 2)) + 1) * p)
    M_bar = M * r % n;
    x_bar = r % n;
    print "M_bar: ", int(M_bar)
    print "x_bar: ", int(x_bar)

    for ei in bin(e)[2:]:
        print int(x_bar), " * ", int(x_bar), " mod ",(int(n));
        x_bar = mon_pro(x_bar, x_bar, n, 10)
        print "x_bar * x_bar mod n_nat =", int(x_bar)
        if ei == '1':
            print int(M_bar), " * ", int(x_bar), " mod ",(int(n));
            x_bar = mon_pro(M_bar, x_bar, n, 10)
            print "Mbar * x_bar =", int(x_bar)

    return mon_pro(x_bar, 1, n, 10)

# rand_max = 1000000
# all_rand = xrange(1, rand_max)
# odd_rand = xrange(1, rand_max, 2)
# for _ in xrange(1000):
# A = choice(all_rand)
# B = choice(all_rand)
# M = choice(odd_rand)

A = 435
B = 435
M = 589

nA = int(math.ceil(A.bit_length() / float(p)))
nB = int(math.ceil(B.bit_length() / float(p)))
nM = int(math.ceil(M.bit_length() / float(p)))
n = max(nA, max(nB, nM))
print n
P = mon_pro(A, B, M, n)
print P
assert (P * _B**n) % M == (A * B) % M

print "----- Mon exp ------"
n = 589
a = 199
b = 300
print mon_exp(a, b, n); # a ^ b mod n
print "^^ should be" , pow(a,b,n);
