# UAF [50]

**python3 uaf.py**
**ubuntu 16.04, libc-2.23**

use after free 的利用。一開始的msgbox free 調之後最後又呼叫了裡面的函式。可以宣告一樣的 size 拿回那塊 malloc 後 leak 裡面的內容(function pointer) 後改寫成 system

`FLAG{U5e_af7er_freeeeeeee_yeeeeeeee}`

