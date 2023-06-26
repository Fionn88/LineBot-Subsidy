# LineBot for subsidy search

![image](https://github.com/Fionn88/LineBot-Subsidy/blob/main/%E6%9E%B6%E6%A7%8B%E5%9C%96.png)

## LineID：@044ejumg

- [v1.0.X](https://hub.docker.com/repository/docker/mona666/linebot-subsidy/general)
  - 輸入特定津貼
  - 輸入「津貼查詢」
 
### Latest Version: v1.0.1

- 2023/06/26
  - 版本：v1.0.1
  - 功能：增加使用者如輸入「E政府」沒有出現的津貼，將會回覆告知
 
### Getting Stated
```
docker run -e LINE_CHANNEL_ACCESS_TOKEN="YOUR LINE CHANNEL ACCESS TOKEN" -e LINE_CHANNEL_SECRET="YOUR LINE CHANNEL SECRET" -p {本機開的port}:8001 -d mona666/linebot-subsidy:{VERSION}
```

## TODO

- [ ] 後端讀取資料庫
- [ ] 爬蟲程式寫入DB
- [ ] 個人資訊 功能
  - [ ] 使用者輸入個人資訊，DB儲存
  - [ ] 推薦津貼給使用者
- [ ] 可使用模糊查詢
