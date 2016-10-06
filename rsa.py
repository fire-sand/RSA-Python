import hashlib

p = 0xfc6e1048c5dacd074e21ac83f4c3ee79c5df5f15c6272e226f2edf0e3b04a98df5aae23f54b79a166c6c9e6d5e37b6ab56adfad71e7dd856ac15059f0fe2f90eda03aff0511f01ea3a6a0bac921f9378cbe76cab669f315ce11302fc9907e226bce5c9f62cf50f5afa66ed1b52ac1b3d211b637190feade24a3074f36a0e4e23
q = 0xf4fa8f3fbc110afc181cbe2e1090dff9352eab964aa3cf17027d30f4c60be843dc25f50b37146b2d42aad58f87a1a789fe433cda77d6a3f3994d5f76510e8c4e66ea4856d21c6d11200c15582566e938cb5790929c4ffa76b6d8d7c643c8adea1f93c8de81c9a88d2c5082755b29883c42a35b38c8515d937ff6802ea1d14949
e = 0x10001
n = 0xf18ff84197460d9e7fdd494f48c4cadb96eeee61bdae5b245fe090da9dc74d8e682cc0588a06fc8dae5f4ec9c8eafa0be35aaa4ef3ab12cb7a9528859a2b3d3f29c0d0b3e5ef1f86a7829081f8618b3f5cc43e2d13500b15081f3582afde29f93afa4c75ccbfae76de2a450b7e4d28eb9204df1ac299b2921b131f5ca8d65e95d57101d1f250070c9f10d84330e3f7775d51a9e65106845251c59577415168433ceccbcc8cbabf9d51a8bbff0901fd26261bf5eba8b8ead797266d8ce7d7097adb9d5296482eced88bfc70ae0a62bf4eb35d861297ed46926fd971d9c9f9d9e655ad16b58270238eee17afd78c3765aa0a67dae01afc782b31dce1c31fef42fb
d = 0xeb865f1cbcbcfdec6b693be044e8338e35349352d3599bddf4698572d2618fb9e8d2b15be2807b603d030a53ee454535b020276bc1632c791ef52dc44e1418ac6c2e668ef102dc6f33063795b1b291cd5ecaac80d092bbab6ef6d6faac34e621ee223bc8a3b0c50f7b0025bfd60eaf763831edc22eb9230617c5e64f370384c59791a11b4fad2ebb441ecfdbba67e42b35100fc100fdc97434944dad923465a1c238488735178eb474b04850652d6703103e27a9816350f313251ac847cba2ac26b5104d988e7f0ab10deebffe5d69c9bbaffde39fbdbe201372c15d0631ba9e9c84e0f1a616180b4ddc07efd145e9cbfbc36910f4dc04463f6f7edf732af031


def pow_mod(a, b, c):
    ret = 1
    while b:
        if b & 1:
            ret = ret * a % c
        b >>= 1
        a = a * a % c
    return ret


def sign(m):
    h = int(hashlib.sha256(m).hexdigest(), 16)
    return pow_mod(h, d, n)


def verify(m, s):
    h = int(hashlib.sha256(m).hexdigest(), 16)
    return h == pow_mod(s, e, n)


def main():
    m = "hello world"
    for i in xrange(100):
        s = sign(m)
        verify(m, s)
    print verify(m, s)
    print verify(m[:-1], s)


if __name__ == '__main__':
    main()
