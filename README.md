# LineBot for subsidy search

![image](https://github.com/Fionn88/LineBot-Subsidy/blob/main/%E6%9E%B6%E6%A7%8B%E5%9C%96.png)

## LineID：@044ejumg
 
### Getting Stated


#### 在本機端運行
- 在專案資料夾內建立一個檔名為 .env 檔案，內容如下
- 將 LINE_CHANNEL_ACCESS_TOKEN,LINE_CHANNEL_SECRET 內容變更為建立 LibeBot 時取得的 Token

```
LINE_CHANNEL_SECRET = "{replace_me}"
LINE_CHANNEL_ACCESS_TOKEN = "{replace_me}"
PORT = 8001
```
#### 在專案資料夾內執行檔案

```
poetry install
```

```
poetry run python3 main.py
```

#### 使用 Docker 運行
```
docker run -e LINE_CHANNEL_ACCESS_TOKEN="YOUR LINE CHANNEL ACCESS TOKEN" \
-e LINE_CHANNEL_SECRET="YOUR LINE CHANNEL SECRET" \
-e PORT="8001" \
-p {本機對外開的port}:8001 -d \
ghcr.io/fionn88/linebot-subsidy-fastapi:latest
```

## TODO

- [ ] 「津貼查詢」後端基本分類 Return LineBot
  - [ ] (津貼分類後)後端讀取資料庫
- [ ] 使用者直接輸入「完整津貼名稱」，後端讀取資料庫
- [x] 爬蟲程式寫入DB
  - [ ] 補上津貼分類 
- [ ] 個人資訊 功能
  - [ ] 使用者輸入個人資訊，DB儲存
  - [ ] 推薦津貼給使用者
- [ ] 可使用模糊查詢
