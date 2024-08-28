# auto-unlock-server

This is a script for unlocking the auto-lock of an apartment using [Switch Bot's Bot](https://www.switchbot.jp/products/switchbot-bot). \
It triggers when the room's intercom sounds, performs pass-phrase authentication, and presses the unlock button. \
It is intended to be used in combination with [Auto Unlock App](https://github.com/nglcobdai/auto-unlock-app).

|                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **License**     | ![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Environment** | ![Ubuntu](https://img.shields.io/badge/-Ubuntu_22.04_LTS-fad9c1.svg?logo=ubuntu&style=flat) <br> ![Docker](https://img.shields.io/badge/-Docker_v26.0.2-0055a4.svg?logo=docker&style=flat) ![Docker Compose](https://img.shields.io/badge/-Docker_Compose_v2.22.0-0055a4.svg?logo=docker&style=flat) <br> ![CUDA](https://img.shields.io/badge/-CUDA_12.5-a4d17c.svg?logo=nvidia&style=flat) ![Python](https://img.shields.io/badge/-Python_3.10-F9DC3E.svg?logo=python&style=flat) |
| **Technology**  | ![Poetry](https://img.shields.io/badge/-Poetry-2c2d72.svg?logo=python&style=flat) ![FastAPI](https://img.shields.io/badge/-FastAPI-80cbc4.svg?logo=fastapi&style=flat) ![MongoDB](https://img.shields.io/badge/-MongoDB-2e5235.svg?logo=mongodb&style=flat) <br> ![OpenAI-Whisper](https://img.shields.io/badge/-OpenAI_Whisper-e40084.svg?logo=openai&style=flat) ![SwitchBot API](https://img.shields.io/badge/-SwitchBot_API_v1.1-fc6203.svg?logo=SwitchBot&style=flat)          |
|                 |

## Requirements

- Docker and docker-compose are required. The versions are as follows.

  - `Docker`: `v26.0.2`
  - `Docker Compose`: `v2.22.0`

- CUDA is required.

- Whisper model is used. Please refer to the official [github](https://github.com/openai/whisper) for the device requirements.

## Getting Started

### 1. Clone & Prepare .env

```sh
$ git clone -b v1.1.1 https://github.com/nglcobdai/auto-unlock-server.git
$ cd auto-unlock-server
```

### 2. Create .env & Set Environment Variables

#### copy .env.example to .env

```sh
$ cp .env.example .env.prod
```

#### edit .env.prod

You need to edit the following items

| Key                 | Description              | Reference                                                                                     |
| ------------------- | ------------------------ | --------------------------------------------------------------------------------------------- |
| `SWITCH_BOT_TOKEN`  | Switch Bot Token         | [Switch Bot](https://support.switch-bot.com/hc/ja/articles/12822710195351-トークンの取得方法) |
| `SWITCH_BOT_SECRET` | Switch Bot Secret        | [Switch Bot](https://support.switch-bot.com/hc/ja/articles/12822710195351-トークンの取得方法) |
| `UNLOCK_BOT_ID`     | Bot ID for Unlock button | Refer to the output of `python server/src/switch_bot.py`                                      |
| `CALL_BOT_ID`       | Bot ID for Call button   | Refer to the output of `python server/src/switch_bot.py`                                      |
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
$ docker exec -it auto-unlock-server-prod-1 uvicorn server.main:server --host 0.0.0.0 --port 8000
```

### 5. Access

Open other terminal and move to the project directory.

```sh
$ cd auto-unlock-server
```

#### Trigger Call Bot

```sh
$ curl --noproxy 127.0.0.1 -X POST http://127.0.0.1:8000/v1.1/unlock
```

#### Trigger Unlock Bot

```sh
$ curl --noproxy 127.0.0.1 -X POST -F "file=@./sample/test.wav" http://127.0.0.1:8000/v1.1/unlock
```
