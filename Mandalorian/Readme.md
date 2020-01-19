# Mandalorian [200]

**python3 Mandalorian.py**

這題是很直白的 LSB oracle attack。可以直接按照講義上的演算法完成。但是題目有一些變化，原本上課內容教導leak 1 bit 的方法，但本題可以一次leak出4 bits。所以解法上要進行依些修改。

寫本題時，適逢BambooCTF的期間，剛好有一題密碼學題目和本題類似，於是部分參考該題writeup的解法。


當新獲得的oracle 足夠大時會回傳 0 (也有機率本來的oracle 就是 0)。所以如果有連續獲得0的情況。則可認為得到所有的明文了。

Reference:
https://github.com/kuruwa2/ctf-writeups/tree/master/BambooFox%20CTF/oracle


`FLAG{Youg0tTH3Fl4GIHavesPoKEN}`

