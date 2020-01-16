import random

#cipher = open('cipher', 'rb').read()
#print(cipher, len(cipher))

def deOp1(p, s):
    return sum([i * j for i, j in zip(s, p)]) % 256

def deOp2(m, k):
    return bytes([i ^ j for i, j in zip(m, k)])

def deOp3(c, p):
    m = ['\0'] * len(c)
    for i in range(16):
        m[p[i]] = c[i]
    return bytes(m)
    #return bytes([m[p[i]] for i in range(len(m))])

def deOp4(c, s):
    m = []
    for i in c:
        for index, item in enumerate(s):
            if item == i:
                m.append(index)
                break
    return bytes(m)
    return bytes([s[x] for x in m])

'''
Linear Feedback Shift Register
'''
def deStage0(m):
    random.seed('oalieno')
    p = [int(random.random() * 256) for i in range(16)]
    s = [int(random.random() * 256) for i in range(16)]
    c = b''
    for x in m:
        k = deOp1(p, s)
        c += bytes([x ^ k])
        s = s[1:] + [k]
    return c

'''
Substitution Permutation Network
'''
def deStage1(m):
    random.seed('oalieno')
    k = [int(random.random() * 256) for i in range(16)]
    p = [i for i in range(16)]
    random.shuffle(p)
    s = [i for i in range(256)]
    random.shuffle(s)

    c = m
    for i in range(16):
        c = deOp4(c, s)
        c = deOp3(c, p)
        c = deOp2(c, k)
        #c = op2(c, k)
        #c = op3(c, p)
        #c = op4(c, s)
    return c

def decrypt(m, key):
    stage = [deStage0, deStage1]
    for i in map(int, f'{key:08b}'):
        m = stage[i](m)
    return m

cipher = open('cipher', 'rb').read()
for key in range(256):
    print(decrypt(cipher, key))

