# shellc0de [50]

程式有給原始碼，shellc0de檔案會做下列四件事。
1. 宣告陣列shellc0de 並初始化為 0xcc
2. 讀使用者輸入到 shellc0de
3. 檢查裡面是否有 ‘\x00’, ‘\x05’, ‘\x0f’
4. 執行shellc0de

建構時可以直接pwntools asm 進行開檔，讀檔和寫至終端機。但用了syscall所以建構的shellcode 會包含不合法的 ‘\x0f\x05’。一開始嘗試使用xor的方法迴避，shellcode全體xor 一個特定值使shellcode合法，再寫一個decoder放在xor 的shellcode 之前，但可是技藝不精一值沒有成功。最後用了pwnlib.encoders的函式可以直接編碼成迴避特殊字元的shellcode。而得到FLAG

`FLAG{5hellc0d1ng\_f0r\_5yscal1\_:P}`

