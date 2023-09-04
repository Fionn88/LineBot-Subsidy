# Install

## Run locally
- Create a file named '.env' within the project directory with the following contents:
- Replace the contents of LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET with the tokens obtained during the creation of the LineBot.
- Here, the DB is using MySQL.

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
## Use Host Run

```
poetry install
```

```
poetry run python3 main.py
```

## Use Docker Run
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
-d ghcr.io/fionn88/linebot-subsidy-fastapi:v1.0.3
```

## Our Data Structure

| serial_no | name | category | organization_name | url | content | condition_list |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| VARCHAR(20) | VARCHAR(90) | TEXT | TEXT | TEXT | TEXT | TEXT |