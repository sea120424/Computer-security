from pwn import *
from Crypto.Util.number import *

host = 'edu-ctf.csie.org'
port = 10191
#r = process('./server.py')
r = remote(host, port)

r.sendlineafter('> ', '1')
c = r.recvuntil('\n')
c = int(c[4:].decode())
e = r.recvuntil('\n')
e = int(e[4:].decode())
n = r.recvuntil('\n')
n = int(n[4:].decode())
print('c = ', c)
print('e = ', e)
print('n = ', n)

def pollard(n):
    a = 2
    b = 2
    while 1:
        a = pow(a, b, n)
        p = GCD(a-1, n)
        if 1 < p < n:
            return p
        b += 1

p = pollard(n)
q = n // p
d = inverse(e, (p-1) * (q-1) )
m = pow(c, d, n)
print(long_to_bytes(m))

r.interactive()
