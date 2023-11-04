-- refs: https://hub.docker.com/r/gvenzl/oracle-xe Initialization scripts
ALTER SESSION SET CONTAINER=XEPDB1

create user test identified by test quota unlimited on users;

grant connect, resource to test;

