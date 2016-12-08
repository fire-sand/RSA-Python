import binascii
import math
import serial
import sys
import time

# RSA Modulus
N = 0x77b3ce7f6114022ec5affbe9073510714681b8ea710c126ecdff65057a35b1db

# Encryption Key
E = 0x10001

# Decryption Key
D = 0x39200a3027f8108299bd3e8f1aed6c06bbbb26977b689af6810777fc10b05da1

# RSA bit length for FPGA
BIT_LENGTH = 256


ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
)

assert ser.isOpen()


def mod_exp(M, exponent):
    """
    Calculates M^exponent mod N
    where M is an integer.
    """

    n = max(M.bit_length(), max(exponent.bit_length(), N.bit_length()))

    # Convert to Montgomery space
    r = 2**n
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


def main():
    message = sys.argv[1][:BIT_LENGTH / 8]

    print 'Encrypting: %s with \nRSA Encryption Key: (%d, %d)...' % (message, E, N)

    t = time.time()
    ciphertext = encrypt(message)
    encryption_time = time.time() - t

    print 'Ciphertext:', ciphertext

    time.sleep(1)

    print 'Decrypting: %s with \nRSA Decryption Key: (%d, %d)...' % (message, D, N)
    t = time.time()
    plaintext = decrypt(ciphertext)
    decryption_time = time.time() - t
    print 'Recovered plaintext:', plaintext

    print 'Encryption took', encryption_time
    print 'Decryption took', decryption_time


if __name__ == '__main__':
    main()
