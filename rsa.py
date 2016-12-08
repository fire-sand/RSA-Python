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

print ser.isOpen()

# time.sleep(2)


def mod_exp(M, exponent):
    """
    Calculates M^exponent mod N
    where M is an integer.
    """

    # Convert to Montgomery space
    r = 2**(255 * p)
    M_bar = (M * r) % N
    x_bar = r % N

    def dump(n, bit_length=BIT_LENGTH):
        s = format(n, '0{}x'.format(bit_length / 4))
        return s.decode('hex')

    ser.write(dump(n, bit_length=8))
    ser.write(dump(exponent.bit_length() - 1, bit_length=8))
    ser.write(dump(x_bar))
    ser.write(dump(M_bar))
    ser.write(dump(exponent))
    ser.write(dump(N))

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
