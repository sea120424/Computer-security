# Tinyurl [300]

**python3 tinyurl.py**

隨意輸入網址後會給予一段縮網址，訪問後他會改與預覽標題，表示該服務器可能有SSRF的漏洞。程式源碼中可以印證
```
webpage = urllib.request.urlopen(req).read()
title = webpage.decode().split('<title>')[1].split('</title>')[0]
```

第一行會用 urlopen 請求 req 的內容( 即輸入的url )可以利用這一點請求內網的資訊。

內網是由 Redis 架設的資料庫，位置根據源碼在 port 6397 處。之後根據一個 python 的 bug 偽造請求的假標頭。

但會遇到Redis擋Host的檢查。解法根據下列的參考網址：使用?q 傳入Redis可以迴避掉Redis的檢查。順利的話可以控制內網
(https://bugs.python.org/issue35906?fbclid=IwAR3iaJOX97iAgmQZZ5v1Br6Z\_jeZZbHrwAteq0IK6JY4W2v3KCBJ3HjCpQQ)
```
urllib.request.urlopen('http://redis:6397/?q=HTTP/1.1\r\n[payload]')
```

控制Redis的payload則參考下列網址中的構造方式，payload放在參數q中[payload]的位置。
(https://blog.tonkatsu.info/ctf/2018/07/01/sctf-2018-quals.html?fbclid=IwAR0MgxCTcn5izSua4LjGE8YSboAaf8OyIOJDlE2lG2xFSGjEenQhaqE\_haQ #webcached)

整體payload中較重要的幾個參數為set seesion: cookie (之後會用到)和包成python class的 RCE 程式碼。之後會用反序列話的漏洞觸發這段RCE的code。

包成python class的 RCE 程式碼如下(和上述網頁幾乎相同)，之後再用pickle包裝。
```
class shell(object):
    def __reduce__(self):
        return (__import__('os').system, [RCE] )
str(pickle.dumps({'shell': shell()}))[2:-1]
```

到此反序列話的payload已經構造完成，剩下觸發反序列化的工作。源碼以不同的session(sid) 判斷不同次連線。所以可以用不同session的請求使第一次的payload序列化並執行RCE。

詳細流程如下：
1. 拿一個sid(隨便送個請求)
2. 構造pickle包裝的payload
3. 用剛剛的sid送出payload，拿到一個網址(tinyurl)
4. 用新連線觸發序列化，生成RCE code
5. 再用原本的sid執行被生成的RCE

