from pwn import *
from Crypto.Util.number import *

r = remote('edu-ctf.csie.org', 10192)
r.recvuntil('> ')
r.sendline('1')
q = r.recvline()
c = int(q[4:-1])
q = r.recvline()
e = int(q[4:-1])
q = r.recvline()
n = int(q[4:-1])
a = inverse(16, n)
m = 0
b = 0
i = 0
f = 0

while True:
    r.sendlineafter('> ', '2')
    r.sendline(str(pow(a,i*e,n)*c%n))
    q = r.recvline()
    lsb = (int(q[4:-1]) - (a*b)%n) % 16
    if lsb == 0:
        f += 1
        if f == 10:
            break
    else:
        f = 0
    b = (a*b + lsb) % n
    m = 16**i*lsb+m
    print(m)
    i += 1

print(m)
print(long_to_bytes(m))

