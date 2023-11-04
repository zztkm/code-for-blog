.PHONY: updb
updb:
	docker-compose up -d oracle

.PHONY: upapi
upapi:
	docker-compose up -d --build --force-recreate app

.PHONY: restartapi
restartapi:
	docker-compose restart app

.PHONY: down
down:
	docker-compose down

.PHONY: ps
ps:
	docker-compose ps

.PHONY: logs
logs:
	docker-compose logs -f -t app

.PHONY: build
build:
	CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC="zig cc -target x86_64-linux" CXX="zig c++ -target x86_64-linux" go build -trimpath -o portal main.go
