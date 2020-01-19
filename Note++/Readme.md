# Note++ [400]

**python3 note++.py**

保護機制全開
 

題目提供一個Note的表單，我們可以通過表單下3個指令：
1. add：malloc一個表單，但大小不能超過0x78。然後我們可以為表單寫一個最多長度48的敘述。表單數量最大值為10。以下是表單的結構。每個新的表單會對應一個is\_freed 的參數被設為0。
```
struct Note{
    int is_freed;
    char *data;
    char description[48];
};
```

2. show：印出所有表單的內容，如果他的is\_freed是1會表單沒內容則跳過。
3. delete：刪除一個表單，清空malloc的內容，並且將對應的is\_freed設為1。
題目的漏洞主要有兩處，我最先看到的是read\_input 的漏洞
```
int read_input( char *buf , unsigned int size ){
    int ret = __read_chk( 0 , buf , size , size );
    if(ret <= 0){
        puts("read error");
        _exit(1);
    }
    if(buf[ret-1] == '\n'){
        buf[ret-1] = '\0';
    }
    return ret;
}
```

看上面的函式的實做其實是沒有漏洞的，但漏洞發生在新增時呼叫的方式。
```
notes[i].data = malloc( size );
read_input( notes[i].data , size - 1 );
```

size 本身的型別是 unsigned int。當size被減一時原本如果輸入size為0。已經malloc 0x20的空間變得可以輸入0xff的資料。可以用這個方式改變資料在後續位置的內容。

第二個漏洞和顯示有關，宣告時description只宣告48的長度。但輸入時使用的函式為：
```
scanf( "%48s" , notes[i].description );
```

scanf 的特性會讓輸入的下一個byte補上0x00。所以可以用此方法讓下個Note的is\_freed被覆寫成0。於是可以show出它的內容(如果有的話)。

首先多收集一些資訊。我想先leak出heap\_base的值(而且之後有用到)，於是簡單構造leak 的 payload 如下：
```
#add(Size, Note, description)
#delete(index)
add(0x18, 'aaaaaaaa', '00')
add(0x58, 'bbbbbbbb', '10')
add(0x58, 'bbbbbbbb', '10')
delete(0)
delete(1)
add(0x18, 'aaaaaaaa', 'd' * 48)
delete(2)
delete(1)
delete(0)
```

構造兩個大小一樣的note之前放一個修改is\_freed的Note。依序free第二個和第一個可以讓第一個Note中記錄前一個的位置，然後修改掉第一個is\_freed的值，即可用show指令把heap\_base+??? 打印出來。

但如果沒辦法得到libc\_base一樣做不到太多事。題目沒有太多的漏洞所以依舊要重malloc下手。如果能夠造出一個small bin 然後free掉他，他的內容會記錄main\_arena的位置，用上述的方式印出資料。也就是間接地透露出libc\_base。我們擁有輸入size = 0 修改0xff個bytes的能力，這件事就沒有那麼困難了。先看以下payload：
```
add(0x08, 'aaaa', 'zero')               # index = 2
add(0x68, 'bbbbbbbb', 'frist')
add(0x68, '\x00' * 0x18 + p64(0x51), 'second')
delete(2)
add_byte(0x0, b'\x00' * 0x18 + p64(0x91), 'note' )
delete(3)
delete(2)
```

先創造一個 0x20的Note用他來把下一個Note的大小設為smallbin。但直接強印設置會吃錯誤，他會檢查chunk到top chunk 的位置是否正確。所以之後要多設置一個假的位置。如下：0x51是我們設置的內容但這樣可以躲過top chunk 位置的檢查。
```
0x0000000000000000 0x0000000000000091	(index 2)
…
0x0000000000000000 0x0000000000000071	(index 3)
0x0000000000000000 0x0000000000000001
0x0000000000000000 0x0000000000000051
```

得到libc\_base後就可以朝 \_\_malloc\_hook 寫資料了，這段就不贅述了，用 -0x03的方式讓位置檢查合法後找一個one\_gadget塞到malloc\_hook中。然後malloc資料後就……crash了。當前沒有任何一個one\_gadget符合constraint。於是進入了卡關階段。

我開始想有沒有其他的方式可以RCE。看了看free的函式。
```
free( notes[idx].data );
```

如果我data裡面放 /bin/sh，然後把free蓋成system不是就可以拿到shell嗎？但 \_\_free\_hook前面一片平坦，這樣無法躲過檢查。而GOT table那邊也沒有可寫入的權限。(現在想了想我也不知道pie\_base)。最後想到double free 的方式。

這題有一個is\_freed 的檢查，構造double free 雖然麻煩了點但還是可以做到。構造完成後我直接用gdb追下去，到malloc\_printerr函式中發現剛好有一個one\_gadget的constraint是符合的，於是有點僥倖的拿到了shell。


`FLAG{Heap_exp1oit4ti0n_15_fun}`
