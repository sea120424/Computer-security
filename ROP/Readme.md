# ROP [50]

**python3 rop.py**

gets 可以 overflow 但沒有留後門或關 NX ，但程式將整個 libc load 進來，可以找到很多 ROP 串出開 shell 的指令。


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

`FLAG{ROo0o0o0o0o0o0o0o00P}`
