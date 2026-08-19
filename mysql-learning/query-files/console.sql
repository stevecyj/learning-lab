set persist autocommit =0;
set persist autocommit =1;
select @@global.autocommit;

select @@autocommit;

create database bookstore;
drop database bookstore;
show databases;