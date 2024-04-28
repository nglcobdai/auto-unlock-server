# python

## Getting Started

### 1. Clone & Prepare .env

```sh
$ git clone git@github.com:nglcobdai/auto-unlock.git
$ cd auto-unlock
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
$ docker exec -it auto-unlock-project-1 uvicorn main:app --host 0.0.0.0
```

### 5. Access

```sh
$ curl -X POST http://127.0.0.1:8000/api/unlock
```
