# Cathub Party [100]

**python3 cathub\_party.py**

老師上課有提示這是一題 padding oracle 的題目，所以大致上就按照講義上的步驟打出來。首先要處理encode的問題，題目的 cookie中有一個FLAG的項目，這是要進行padding oracle的部分。如果送出的FLAG不合法，網頁會回傳” What the flag?! CHEATER!!! get out of here.”，否則會回傳CAT PARTY!!!!!!。
 

先用 url decode後用base64 decode即可拿到真正加密過的FLAG，之後要先確認block size。方法就是依序送出最後一個bytes，最後兩個bytes…以此類推，檢查程式到哪處可以被判斷為合法。最後結果是32。也就是block size為16。

確定block size後就用padding oracle爆出FLAG 的明文。我的解法是從最後每次取兩個block，當第一個block被暴力破解完後再向前拿一個當第一個block。原本的第一個block放到第二個。

實際時作方法為依序將最後N個bytes和某一個數字(i) XOR 後和block2做一些操作會變成 0xN。代表明文相對應的位置 XOR i = 0xN，即可求出明文。之後要擴張合法padding的範圍。將原本的0xN變成0xN+1，後再向前一位數重複進行。大致上如下：
```
while padding_num <= 16:
        for j = 0:255
			b1 <- block1
			b1[-padding_num] ^= j
			if legal(b1+block2):
				block1 <- b1[:-padding_num]
				index <- 0: padding_num
                    	block1 += b1[i] ^ (padding_num) ^ (padding_num+1)
```

途中遇到了一個小問題，padding的最後一位數無法無法輸出，推測是因為我一次只傳兩個block讓全部只有padding的空輸入過不了檢查。於是改成一次傳3個block進去就行了。

註解：執行時就開 –W ignore 參數，不然會被Warning淹沒。

`FLAG: FLAG{EE0DF17A410C90F86E88471346B6DA77E8C878200B37E60C53E9A56913211465}`

