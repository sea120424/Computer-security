# EDU 2019 election [300]

**python3 election.py**

題目中有兩個明顯的 buffer overflow 的漏洞。首先，先看 main 函式的內容。註冊時使用者可以記錄一段長度為0xb8的token。如下
```
char token[0xb8] = {0};
...
case 2:
read( 0 , token , sizeof( token ) );
...
```

但是驗證時卻可以輸入長度0xc8驗證。這雖然不是直接的印出資訊但是可以讓我們用爆搜的方式將 $rbp之後16bytes一位一位地leak出來。後面的剛好是8bytes的canary和old rbp address。於是canary 和 pie\_base 就被洩漏了。
```
char buf[0xc8]; // global varible
int len = read( 0 , buf , sizeof( buf ) );
    if( memcmp( buf , token , len ) ){
             puts( "Invalid token." );
             break;
    }
```

接下來是第二個 overflow 的漏洞 voting() 函式中宣告的msg大小為0xe0，但根據每多一票可以多說一個字的規則我們最多可以在msg中輸入0xff (uint8\_t 上限) 的內容。我們能有用控制的部分為 0xe0 + 0x08(canary) + 0x08(old rbp ) + 0x08 (return address)。

為了要達到 remote shell 需要先知道 libc\_base的值，但只能蓋到return address。一開始想到利用 stack migration 的方式，將stack 搬到一個我能控制的位置。在只有 pie\_base 已知的情況下，我只能選擇使用 buf 的空間。一如往常的串ROP chain 拿libc\_base。

pop\_rdi
libc\_start\_main
puts\_plt
main\_plt

雖然可以達到目的但stack會被蓋爛，導致之後使用 printf 函式會出現問題。系統呼叫 printf 時用gdb往下追發現她會呼叫一個子函式 \_\_IO\_vprintf\_interna 裡面有一個指令：
```
mov DWORD PTR [rbp - 0x4b8], eax
```

導致一個使如果 $rsp 位置不夠好(在可寫區段的最開頭)，在經過函式 mov rbp, rsp 後一定會發生寫入不可寫位置的問題。

最後我放棄了這條路，但我發現了執行檔中提供了 pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret 的 gadget ，而return address 後的下一位剛好是我可控的區域 (msg)內於是到那個地方串 ROP chain。

payload = b'\x00' * 0x38
payload += p64(pop\_rdi)
payload += p64(libc\_start\_main)
payload += p64(puts\_plt)
payload += p64(ret)
payload += p64(main\_plt + 318)

串完之後總算leak 出 libc 並且保證程式之後可以正常運行。上述 ROP 中，ret是為了對齊，否則會報未對齊的錯誤。

第二輪的voting我已經得到開shell 所需的資訊了，我認為stack pivoting依舊是一個方法，但基於懶惰的原因，我直接使用 one gadget，rsp部分的限制都在可控的範圍，所以直接把msg送的資料前端改成 \x00後one gadget 收尾。

