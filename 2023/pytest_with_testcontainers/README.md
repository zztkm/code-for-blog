# pytest-with-testcontainers


## Requirements

- Docker (Docker Compose)
- [Rye](https://rye-up.com/)

## Run dev server

```bash
# up db
make up

# install dependencies
rye sync --no-lock

# run dev server (hot reload)
rye run dev
```

When you want to migrate the development database, please edit the `schema.sql`, confirm the changes with following command.

```bash
make migrate-dry
```

If everything is fine, please go ahead and execute make migrate.

```bash
make migrate
```

## Run test

```bash
# init database image
make image

# run tests
rye run test
```

## Generate model

```bash
# up db
make up

# generate model
make model
```

## Note

現実的な運用
- コンテナイメージはできるだけマイグレーション済のものを使うほうが良い
- マイグレーション済のイメージをつくるには、Dockerfile を書いてやる必要がある。
