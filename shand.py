import math

p = 2
_B = 2**p

# M is not allowed to be even
# Hardcoded for _B = 4
MUS = [None, 3, None, 1]


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
        P = (A * bt + P + qt * M) >> p

    return P


A = 216
B = 123
M = 311

nA = int(math.ceil(A.bit_length() / float(p)))
nB = int(math.ceil(B.bit_length() / float(p)))
nM = int(math.ceil(M.bit_length() / float(p)))
n = max(nA, max(nB, nM))
P = mon_pro(A, B, M, n)
print P
print(P * _B**n) % M == (A * B) % M
