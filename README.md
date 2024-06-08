# python

## Getting Started

### 1. Clone & Prepare .env

```sh
$ git clone git@github.com:nglcobdai/auto-unlock-server.git
$ cd auto-unlock-server
```

### 2. Create .env & Set Environment Variables

#### copy .env.example to .env

```sh
$ cp .env.example .env.prod
```

#### edit .env.prod

下記項目を編集する必要がある(en)
You need to edit the following items

| Key                 | Description              | Reference                                                                                     |
| ------------------- | ------------------------ | --------------------------------------------------------------------------------------------- |
| `SWITCH_BOT_TOKEN`  | Switch Bot Token         | [Switch Bot](https://support.switch-bot.com/hc/ja/articles/12822710195351-トークンの取得方法) |
| `SWITCH_BOT_SECRET` | Switch Bot Secret        | [Switch Bot](https://support.switch-bot.com/hc/ja/articles/12822710195351-トークンの取得方法) |
| `UNLOCK_BOT_ID`     | Bot ID for Unlock button | `python app/show_bot_list.py`                                                                 |
| `CALL_BOT_ID`       | Bot ID for Call button   | `python app/show_bot_list.py`                                                                 |
| `MONGODB_USER_NAME` | MongoDB User Name        | Any value can be set                                                                          |
| `MONGODB_USER_PWD`  | MongoDB User Password    | Any value can be set                                                                          |
| `DATADRIVE`         | Data Drive               | MongoDB information storage directory                                                         |
| `SECRET_PHRASE`     | Secret Phrase            | Set any password to unlock                                                                    |

### 3. Docker Build & Run

```sh
$ docker-compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
```

### 4. Server Start

```sh
$ docker exec -it auto-unlock-server-prod-1 uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. Access

```sh
$ curl --noproxy 127.0.0.1 -X POST http://127.0.0.1:8000/api/v1.0/unlock
```
