import binascii
import math
import serial
import sys
import time

from random import choice

p = 1
_B = 2**p

N = 0x77b3ce7f6114022ec5affbe9073510714681b8ea710c126ecdff65057a35b1db
E = 0x10001
D = 0x39200a3027f8108299bd3e8f1aed6c06bbbb26977b689af6810777fc10b05da1
n = 255

# M is not allowed to be even
# Hardcoded for _B = 4
# MUS = [None, 3, None, 1]
MUS = [None, 1]


BIT_LENGTH = 256


MESSAGE = sys.argv[1][:BIT_LENGTH / 8]

ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
)

ser.isOpen()

time.sleep(2)


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


def mod_exp(M, exponent):
    # M = int(binascii.hexlify(M),16)

    # These 3 lines are still kind of hard
    r = 2**(255 * p)
    M_bar = (M * r) % N
    x_bar = r % N

    # print "M_bar: ", M_bar
    # print "x_bar: ", x_bar

    def dump(n, bit_length=BIT_LENGTH):
        s = format(n, '0{}x'.format(bit_length / 4))
        return s.decode('hex')

    ser.write(dump(n, bit_length=8))  # TODO uncomment me to send the length
    # print repr(dump(n, bit_length=8))
    # TODO uncomment me to send the length
    ser.write(dump(exponent.bit_length() - 1, bit_length=8))
    # print repr(dump(exponent.bit_length() - 1, bit_length=8))
    ser.write(dump(x_bar))
    # print repr(dump(x_bar))  # 435, 0x01b3
    ser.write(dump(M_bar))
    # print repr(dump(M_bar))  # 571, 0x023b
    ser.write(dump(exponent))
    # print repr(dump(exponent))  # 300, 0x012c
    ser.write(dump(N))
    # print repr(dump(N))  # 589, 0x024d
    val = None
    val = ser.read(size=BIT_LENGTH / 8)
    if val:
        return binascii.hexlify(val).decode('hex')

    return None


def encrypt(M):
    return mod_exp(int(binascii.hexlify(M), 16), E)


def decrypt(C):
    return mod_exp(int(binascii.hexlify(C), 16), D)

CIPHER = encrypt(MESSAGE)
print 'encrypted:', CIPHER
print 'decrypted:', decrypt(CIPHER)

# hex_M = binascii.hexlify(MESSAGE)
# M = int(hex_M, 16)
# print '^^^ should be ^^^', hex(pow(M, E, N))

# A = 199
# B = 300
# M = 589
# nA = int(math.ceil(A.bit_length() / float(p)))
# nB = int(math.ceil(B.bit_length() / float(p)))
# nM = int(math.ceil(M.bit_length() / float(p)))
# n = max(nA, max(nB, nM))
# print n

# print "----- Mon exp ------"
# print mod_exp(A, B, M, n); # a ^ b mod M
# print "^^ should be" , pow(A, B, M);

# SEND TO FPGA


# def dump(n, bit_length=256):
#     s = format(n, '0{}x'.format(bit_length / 4))
#     return s.decode('hex')

# dn = dump(M)
# print bin(M)
# print '%0256x' % M
# print repr(dn)
# print len(dn)

# Need to change to M_bar and X_bar
# r = 2**(n * p)
# M_bar = (A * r) % M
# X_bar = r % M

# parameter RX_MP_COUNT = 0;
# parameter RX_E_IDX = 1;
# parameter RX_XBAR = 2;
# parameter RX_MBAR = 3;
# parameter RX_E = 4;
# parameter RX_N = 5;

# ser.write(dump(n, bit_length=8)) # TODO uncomment me to send the length
# print n
# ser.write(dump(B.bit_length() - 1, bit_length=8)) # TODO uncomment me to send the length
# print B.bit_length() - 1
# ser.write(dump(X_bar))
# print X_bar  # 435, 0x01b3
# ser.write(dump(M_bar))
# print binascii.hexlify(dump(M_bar)), len(binascii.hexlify(dump(M_bar)))
# print M_bar  # 571, 0x023b
# ser.write(dump(B))
# print B  # 300, 0x012c
# ser.write(dump(M))
# print M  # 589, 0x024d
# val = None
# while True:
#     val = ser.read(size=4)
#     if val:
#         print binascii.hexlify(val)

# ser.close()
