from datatypes import _B, Word

print "_B size is: {}".format(_B)

# Test Word

w1 = Word(0)
assert w1.word == 0
assert str(w1) == '0'
assert int(w1) == 0
assert type(w1) == Word

w2 = Word(12345)
