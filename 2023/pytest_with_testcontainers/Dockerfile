FROM mysql:8.2

COPY my.cnf /etc/mysql/conf.d/my.cnf
COPY schema.sql /docker-entrypoint-initdb.d/01_create_schema.sql