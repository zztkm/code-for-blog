CURRENT_REVISION := $(shell git rev-parse --short HEAD)


.PHONY: image
image:
	docker build . -t udon-db:latest

.PHONY: up
up: image
	docker compose up -d

.PHONY: down
down:
	docker compose down

.PHONY: model
model:
	rye run sqlacodegen --generator declarative --outfile src/udonya/gen/sqlacodegen/models.py mysql+pymysql://mysql:mysql@localhost/db

.PHONY: dry
dry: $(GOBIN)/mysqldef
	mysqldef --user=mysql --password=mysql db --dry-run < schema.sql

.PHONY: migrate
migrate: $(GOBIN)/mysqldef
	mysqldef --user=mysql --password=mysql db < schema.sql

$(GOBIN)/mysqldef:
	go install github.com/sqldef/sqldef/cmd/mysqldef@latest
