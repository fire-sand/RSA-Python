import sys

from datatypes import WORD_SIZE, Word, breakup, Nat
from random import randint

print "_B size is: {}".format(WORD_SIZE)

# Test Word

w1 = Word(0)
assert w1.word == 0
assert str(w1) == '0000'
assert int(w1) == 0
assert type(w1) == Word

# print list(breakup('1234567890', 4))

# Test Nat

n1 = Nat(0)
print n1

n1 = Nat(894)
print n1

w1 = Word(0xF)
w2 = Word(0xF)

c, s = w1.add(w2)
print c, s


for _ in xrange(1000):
    z_nat = Nat()
    x, y = randint(0,10000000), randint(0,10000000)
    x_nat, y_nat = Nat(x), Nat(y)

    assert z_nat.add(x_nat, y_nat) == Nat(x + y)

x = Nat(100)
y = Nat(100)
z = Nat(101)
s = {x, y, z}
assert len(s) == 2
