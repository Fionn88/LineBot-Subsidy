# 🏛️ LINEBot_For_Subsidy_Search 🏛️

- The interface is in Mandarin.目前只支援繁體中文

![image](https://github.com/Fionn88/LineBot-Subsidy/blob/main/readme_assests/architecture_show.png)

## 🏛️ LineID：@044ejumg

![image](https://github.com/Fionn88/LineBot-Subsidy/blob/main/readme_assests/invite_code.png)

## 🏛️ App demo and features

- General features:
![image](https://github.com/Fionn88/LineBot-Subsidy/blob/main/readme_assests/product_intro.png)

![image](https://github.com/Fionn88/LineBot-Subsidy/blob/main/readme_assests/detail_feature.png)
 
### Getting Stated


- [X] 津貼類別地點選單


#### 在本機端運行
- 在專案資料夾內建立一個檔名為 .env 檔案，內容如下
- 將 LINE_CHANNEL_ACCESS_TOKEN,LINE_CHANNEL_SECRET 內容變更為建立 LibeBot 時取得的 Token
- 這裡的DB是使用MySQL

```
LINE_CHANNEL_SECRET = "{replace_me}"
LINE_CHANNEL_ACCESS_TOKEN = "{replace_me}"
PORT = "8001"
DB_HOST = "example_host"
DB_PORT = "3306"
DB_USER = "example_user"
DB_PASSWORD = "example_password"
DB_SCHEMA = "example_schema"
DB_TABLE = "example_table"
TEAM_EMAIL = "example@gmail.com"
```
#### Use Host Run

```
poetry install
```

```
poetry run python3 main.py
```

#### Use Docker Run
```
docker run -e LINE_CHANNEL_ACCESS_TOKEN="YOUR LINE CHANNEL ACCESS TOKEN" \
-e LINE_CHANNEL_SECRET="YOUR LINE CHANNEL SECRET" \
-e PORT="{Container Port}" \
-e DB_HOST="YOUR DB HOST" \
-e DB_PORT="YOUR DB PORT" \
-e DB_USER="YOUR DB USER" \
-e DB_PASSWORD="YOUR DB USER PASSWORD" \
-e DB_SCHEMA="YOUR DB USER SCHEMA" \
-e DB_TABLE="YOUR DB USER TABLE" \
-e TEAM_EMAIL="YOUR EMAIL" \
-p {Host Port}:{Container Port} \ 
--network={same as mysql container network and you can connect mysql using the mysql container name => env: DB_HOST} --name fastapi-dev \
-d ghcr.io/fionn88/linebot-subsidy-fastapi:v1.0.2
```

#### Our Data Structure

| serial_no | name | category | organization_name | url | content | condition_list |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| VARCHAR(20) | VARCHAR(90) | TEXT | TEXT | TEXT | TEXT | TEXT |


## 🏛️ TODO

### 功能相關
- [x] 「津貼查詢」後端基本分類 Return LineBot
  - [X] (津貼分類後)後端讀取資料庫
- [x] 使用者直接輸入「完整津貼名稱」，後端讀取資料庫
- [x] 爬蟲程式寫入DB
  - [X] 補上津貼分類
- [ ] LineBot前端選項篩選與回覆
- [ ] 優化回覆津貼條件和內容
- [ ] 可使用模糊查詢
- [ ] 個人資訊 功能
  - [ ] 使用者輸入個人資訊，DB儲存
  - [ ] 推薦津貼給使用者


### 流程相關
- [X] 增加CI/CD Build Image
- [X] 佈署至Fly.io
