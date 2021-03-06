# IDAmudamudamuda [100]

先使用 `file` 指令看檔案的型態

```
KeyChecker.exe: PE32 executable (console)
```

和上一題一樣可以用 x32dbg debug 檔案。

1. 題目一開始要求輸入一個 seed，然後會執行一個函式。這個函式會做一系列操作，但和輸入的 seed 都沒什麼關係，因為 seed 存在 ebp+8 的位置所以只需要關注和這個位置相關的操作。
```
add edx, dword ptr ss : [ebp + 8]
```
這是唯一和seed有關的動作。

2. 繼續往下執行發現他正在逐一更改某一塊記憶體位置，之後這一塊記憶體會被用來當作函式呼叫。原本的值加上 seed 會成為新的值寫入記憶體。由於知道這是一個函式，他該擁有正常的函式開頭如下：

```
55   (push ebp)
8BEC (mov ebp, esp)
```
所以可以推斷seed = 16(其中一種解)，讓原本位置的 0x45 變成 0x55

3. 第二步要輸入 flag 值。執行時會用一個迴圈測試 flag 的長度是否等於32，如果成立則進入剛剛修改完的函式執行。他會將 flag 中的每一個值 add 0x23 然後 xor 0x66 後和一塊記憶體的值做比較。如果不同則中斷迴圈。可以寫個簡單的程式(我是直接算出來)來求得 flag 的真正值。

`FLAG{y3s!!y3s!!y3s!!0h_my_g0d!!}`
