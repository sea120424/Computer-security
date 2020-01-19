# Computer-security
Writeup of NTU Computer Security Course

- [ ] [HW0x00] Pwn - shellc0de
- [ ] [HW0x00] Reverse - m4chine
- [ ] [HW0x00] Crypto - encrypt
- [ ] [HW0x00] Misc - Winmagic
- [ ] [  LAB ] Reverse - What The Hell
- [ ] [HW0x01] Reverse - Back to the Future
- [ ] [HW0x02] Reverse - IDAmudamudamuda
- [ ] [  LAB ] Web - sushi
- [ ] [  LAB ] Web - me0w
- [ ] [  LAB ] Web - No Password
- [ ] [HW0x03] Web - Unexploitable
- [ ] [HW0x03] Web - Safe R/W
- [ ] [  LAB ] Web - Sh3ll Upload3r
- [ ] [  LAB ] Web - EasyPeasy
- [ ] [  LAB ] Pwn - bof
- [ ] [  LAB ] Pwn - how2orw
- [ ] [HW0x05] Pwn - Casino
- [ ] [  LAB ] Web - XXE
- [ ] [HW0x06] Web - Tinyurl
- [ ] [  LAB ] Pwn - ROP
- [ ] [  LAB ] Pwn - ret2plt
- [ ] [  LAB ] Pwn - ret2libc
- [ ] [HW0x07] Pwn - Casino++
- [ ] [  LAB ] Pwn - UAF
- [ ] [  LAB ] Pwn - Note
- [ ] [HW0x08] Pwn - EDU 2019 election
- [ ] [HW0x08] Pwn - Note++
- [ ] [HW0x09] Crypto - Cathub Party
- [ ] [  LAB ] Crypto - StarWars
- [ ] [HW0x0A] Crypto - Mandalorian


紀錄一下各種看資訊的方法
```
readelf -s /lib/x86_64-linux-gnu/libc-2.27.so | grep system 
# system在libc-2.27 中的位置(其他函式)

objdump -d <binary> 
# 列出binary 中 static 函式的位置 

objdump -R <binary> 
# 列出binary 中 dynamic 函式的位置 

ROPgadget --binary <binary>
# 列出binary 中所有 ROPgadget (要安裝ROPgadget)

one_gadget libc
# 列出 libc 中所有 one_gadget (要安裝one_gadget)
```

