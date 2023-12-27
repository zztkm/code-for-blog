# pytest-with-testcontainers


## Run test

init database image
```bash
make image
```

```bash
# install dependencies
rye sync --no-lock

# run tests
rye run test
```

## model 生成

```bash
# install tool
rye install sqlacodegen

# up db
make up

# generate model
make model
```

## Note

現実的な運用
- コンテナイメージはできるだけマイグレーション済のものを使うほうが良い
- マイグレーション済のイメージをつくるには、Dockerfile を書いてやる必要がある。
