# Casino++ [200]

**python3 casino++.py**

保護機制。原始碼和Casino完全相同，但NX打開後不能再用name裡塞shellcode的方式直接執行。
 

一開始看到 PIE 沒開，以為直接把atoi function 改成 system 的位置就可以拿到 shell 了，但程式跑了一下後想到 ASLR 和 PIE 好像是不同的。在gdb 外跑的程式位置還是隨機的。所以要跑system 的前提是一定要 leak 出 libc base。

從上一題知道 change number 的地方可以改 GOT table 兩次。我們一次連線要做到 leak base + atoi 改成system 好像不太夠用。所以第一步要讓程式不斷的跑迴圈讓我們可以蓋無數次。通過上一題的經驗知道 put 的 GOT table 可以蓋成任何我們要的下一段位置。上次蓋成 name的地址跑沒NX的shell；這次雖然不能跑name但蓋回 casino的plt address還是可以。執行後果然又回到casino lottery。如果蓋回main\_plt則就可以全部重來一次。

最重要的leak libc base 要 puts + libc\_start\_main 的位置。Gdb追了很多次，change number 應該是唯一可以蓋記憶體的洞。剩下可以蓋的函式又要rdi 是可控的才有辦法leak。所以所有的puts和printf就都派不上用場。之後想到我可以蓋到所有函式的table那就直接把一個rdi可控的函式蓋成puts不就好了。像是srand 或 atoi 的 rdi 都是有辦法控制到的，srand 可以用 name 的overflow，atoi則是直接輸入。蓋的目標是puts\_plt 所以需要兩次才能蓋完。兩次中不會不使用到的 srand 較適合，之前先把seed 蓋成libc\_start\_main的address，然後srand table address 蓋成 puts\_plt 就會leak 出資料了。跑的時候發現程式又掛了，gdb 追下去才想到puts早就被我蓋掉了，之前提到的puts\_plt改成printf\_plt就行了。

最後的操作和之前的想法一至，拿到的libc\_start\_main address 減掉0x21ab0 加上 0x4f440 是 system的位置。蓋 atoi 時由於前半段都一樣，只需要用一次蓋後8 bits。下次 read\_int 時輸入 /bin/sh就拿到shell 了。

流程大致如下
1. seed 蓋成 libc\_main\_start 
2. puts 蓋成 casino\_plt
3. srand 蓋成 printfi\_plt 
4. atoi 蓋成 system
5. 輸入 /bin/sh


`FLAG{Y0u_pwned_me_ag4in!_Pwn1ng_n3v3r_di4_!}`
