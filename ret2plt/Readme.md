# ret2plt [50]

**python3 ret2plt.py**

和 ROP 幾乎一樣的程式碼但 load libc 的方式改成 dynamic 所以 ROP 變得很少且使用了system 輸出。
但我們知道某些函式的位置在 plt table 中可以利用。
用 get\_plt 把資訊(sh)寫到一個可寫區域後用 system\_plt call 一樣可以拿shell。

`FLAG{ret2222222222222222222p1t}`
