# Environment
_B = 4

def size(num):
    return len(str(num))

class Word(object):

    word = None

    def __init__(self, w):
        if w < 0:
            raise Exception("Error: Negative input")

        if size(w) > _B:
            raise Exception("Error: Overflow")

        self.word = w

    def __str__(self):
        return str(self.word)

    def __int__(self):
        return self.word


