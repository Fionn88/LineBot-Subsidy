# LineBot for subsidy search

![image](https://github.com/Fionn88/LineBot-Subsidy/blob/main/%E6%9E%B6%E6%A7%8B%E5%9C%96.png)

## LineID：@044ejumg

- [v1.0.X](https://hub.docker.com/repository/docker/mona666/linebot-subsidy/general)
  - 輸入特定津貼
  - 輸入「津貼查詢」
 
### Getting Stated


#### 在本機端運行
- 在專案資料夾內建立一個檔名為 .env 檔案，內容如下
- 將 LINE_CHANNEL_ACCESS_TOKEN,LINE_CHANNEL_SECRET 內容變更為建立 LibeBot 時取得的 Token

```
LINE_CHANNEL_SECRET = "{replace_me}"
LINE_CHANNEL_ACCESS_TOKEN = "{replace_me}"
# Log Level "production" is info, else is debug
profile = "development"
PORT = 8001
```
#### 在專案資料夾內執行檔案

```
python3 main.py
```

#### 使用 Docker 運行
```
docker run -e LINE_CHANNEL_ACCESS_TOKEN="YOUR LINE CHANNEL ACCESS TOKEN" \
-e LINE_CHANNEL_SECRET="YOUR LINE CHANNEL SECRET" \
-e PORT="8001" \
-e PROFILE="development" \
-p {本機開的port}:8001 -d \
ghcr.io/fionn88/linebot-subsidy:latest
```

## TODO

- [ ] 後端讀取資料庫
- [ ] 爬蟲程式寫入DB
- [ ] 個人資訊 功能
  - [ ] 使用者輸入個人資訊，DB儲存
  - [ ] 推薦津貼給使用者
- [ ] 可使用模糊查詢
