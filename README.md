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
docker-compose build --no-cache
docker-compose up -d
```

### 4. Server Start

```sh
$ docker exec -it auto-unlock-server-project-1 uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Access

```sh
$ curl --noproxy 127.0.0.1 -X POST http://127.0.0.1:8000/api/unlock
```
