"""
Binary Number Class

Reference: https://docs.python.org/2.7/reference/datamodel.html#emulating-numeric-types

"""


class binary (object):
    val = None

    def __init__(self, i):
        self.val = i

    # Comparison

    def __lt__(self, other):
        return self.val < other.val

    def __le__(self, other):
        return self.val <= other.val

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return self.val != other.val

    def __gt__(self, other):
        return self.val > other.val

    def __ge__(self, other):
        return self.val >= other.val

    # Math

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __div__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __divmod__(self, other):
        pass

    def __pow__(self, other[, modulo]):
        pass

    # Shifting

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    # Logical Operations

    def __and__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __or__(self, other):
        pass

    # Item Selection

    def __getitem__(self, index):
        pass

    def __setitem__(self, index, value):
        pass

    def __delitem__(self, index):
        pass
