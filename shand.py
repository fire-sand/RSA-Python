import math
import serial
import time

from random import choice

p = 1
_B = 2**p

# M is not allowed to be even
# Hardcoded for _B = 4
# MUS = [None, 3, None, 1]
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

        print P

    return P

def mod_exp(M, e, n, length):
    # n_ = Word(self._mod_inverse(n))
    # n_nat = Nat(n)

    # These 3 lines are still kind of hard
    r = 2**(length * p)
    M_bar = (M * r) % n
    x_bar = r % n
    print "M_bar: ", M_bar
    print "x_bar: ", x_bar

    for ei in bin(e)[2:]:
        print x_bar, " * ", x_bar, " mod ", n
        x_bar = mon_pro(x_bar, x_bar, n, length)
        print "x_bar * x_bar mod n_nat =", x_bar
        if ei == '1':
            x_bar = mon_pro(M_bar, x_bar, n, length)
            print "Mbar * x_bar =", x_bar
    return mon_pro(x_bar, 1, n, length)

# rand_max = 1000000
# all_rand = xrange(1, rand_max)
# odd_rand = xrange(1, rand_max, 2)
# for _ in xrange(1000):
# A = choice(all_rand)
# B = choice(all_rand)
# M = choice(odd_rand)

# A = 216
# B = 123
# M = 589

# nA = int(math.ceil(A.bit_length() / float(p)))
# nB = int(math.ceil(B.bit_length() / float(p)))
# nM = int(math.ceil(M.bit_length() / float(p)))
# n = max(nA, max(nB, nM))
# P = mon_pro(A, B, M, n)
# print n, P
# assert (P * _B**n) % M == (A * B) % M

A = 199
B = 300
M = 589
nA = int(math.ceil(A.bit_length() / float(p)))
nB = int(math.ceil(B.bit_length() / float(p)))
nM = int(math.ceil(M.bit_length() / float(p)))
n = max(nA, max(nB, nM))
print n
# P = mon_pro(A, B, M, n)
# print P
# assert (P * _B**n) % M == (A * B) % M

print "----- Mon exp ------"
print mod_exp(A, B, M, n); # a ^ b mod n
print "^^ should be" , pow(A, B, M);

# SEND TO FPGA

ser = serial.Serial(
    port='/dev/cu.usbmodem1411',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

ser.isOpen()

time.sleep(2)


def dump(n):
    s = '%064x' % n
    # if len(s) & 1:
    # s = '0' + s
    return s.decode('hex')

# dn = dump(M)
# print bin(M)
# print '%0256x' % M
# print repr(dn)
# print len(dn)

ser.write(dump(A))
ser.write(dump(B))
ser.write(dump(M))

val = None
while True:
    val = ser.readline()
    if val:
        print val

ser.close()
