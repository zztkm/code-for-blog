# Go * Oracle example

## Prerequisites

- [Go](https://golang.dev)
- [Zig](https://ziglang.org)
- [Docker](https://docs.docker.com)

## Up and running

```sh
make up
```

## Init oracle

exec bash in container
```sh
docker exec -it <container name|id> /bin/bash
```

access sysdba
```sh
sqlplus sys/sys as sysdba
```

create user
```sh
SQL> create user demo identified by demo default tablespace users temporary tablespace temp;
SQL > grant connect, resource to demo
```

troubleshooting: if you get ORA-01034: ORACLE not available. see [ORA-01034: ORACLE not availableの対処方法 | ねこブログ](https://nekosoftware.wordpress.com/2011/05/19/ora-01034-oracle-not-available%E3%81%AE%E5%AF%BE%E5%87%A6%E6%96%B9%E6%B3%95/)
