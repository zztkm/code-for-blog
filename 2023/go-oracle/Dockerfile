FROM golang:1.21-bullseye as build
WORKDIR /app
COPY go.mod .
COPY go.sum .
# install zig
RUN go install github.com/mattn/zig-update@latest
RUN zig-update x86_64-linux /zig || RET $? || true
RUN go version && \
    go mod download
COPY . .
RUN CGO_ENABLED=1 GOOS=linux GOARCH=amd64 CC="/zig/zig cc -target x86_64-linux" CXX="/zig/zig c++ -target x86_64-linux" go build -trimpath -o portal main.go

FROM oraclelinux:8-slim
RUN  microdnf install oracle-instantclient-release-el8 && \
     microdnf install oracle-instantclient-basic oracle-instantclient-devel oracle-instantclient-sqlplus && \
     microdnf clean all
COPY --from=build /app/portal /go/bin/portal

ENTRYPOINT ["/go/bin/portal"]
