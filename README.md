# python

## Getting Started

### 1. Clone & Prepare .env

```sh
$ git clone git@github.com:nglcobdai/auto-unlock-server.git
$ cd auto-unlock-server
```

### 2. Create .env

- copy .env.example to .env

```sh
$ cp .env{.example,}
```

### 3. Docker Build & Run

```sh
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Server Start

```sh
$ docker exec -it auto-unlock-server-prod-1 uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. Access

```sh
$ curl --noproxy 127.0.0.1 -X POST http://127.0.0.1:8000/api/v1.0/unlock
```
