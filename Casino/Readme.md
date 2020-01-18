# casino [100]

**python3 casino.py**

保護機制。NX 沒有開，程式可以直接執行輸入的shellcode
 
name 宣告的長度是 0x10，題目的read( 0 , name , 0x100 ); 可以產生overflow但因為name的宣告為全域變數所以蓋不到重要的位置。即使如此，還是可以塞下一段shellcode。

在 name 裡面塞 b” jhH\xb8/bin///sPj;XH\x89\xe71\xf6\x99\x0f\x05” (shellcraft.sh) ，name會蓋到後面的值，包括age和seed。age欄位為了不破壞寫好的shellcode要按照格式填入。我的例子是填入84908534。之後可以順利進入casino 函式。

caisno 中可以 overflow 的地方是Change the number? 時沒有對輸入的數字做檢查，可以蓋到陣列宣告範圍外的位置。除了向下覆蓋外還可以向上蓋GOT的位置。大部分的函式先前都已經呼叫過了，要覆蓋他們需要做兩次操作。一次將前段蓋成0，第二次將後半段蓋成0x6020f0(name的位置)。唯一在程式結束前有機會呼叫到的是種樂透後的put函式。

詳細流程如下：先用pwntool 送出shellcode後，輸入相對應的age，第一次樂透要蓋put GOT 的前段，第二次要答對樂透並蓋到後段。經過計算後方別需要的輸入分別為 -42, 0。-43, 0x6020f0。樂透的seed也是可控的(輸入shellcode後即固定)，如此可以成功用put執行到name的shellcode。

`FLAG{0verf1ow_1n_ev3rywhere!}`

