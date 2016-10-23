from datatypes import _B, Word, breakup, Nat

print "_B size is: {}".format(_B)

# Test Word

w1 = Word(0)
assert w1.word == 0
assert str(w1) == '0000'
assert int(w1) == 0
assert type(w1) == Word

# print list(breakup('1234567890', 4))

# Test Nat

n1 = Nat(0)
print [str(n) for n in n1.nat]

n1 = Nat(894)
print [str(n) for n in n1.nat]
