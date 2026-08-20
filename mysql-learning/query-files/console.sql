set persist autocommit =0;
set persist autocommit =1;
select @@global.autocommit;

select @@autocommit;

create database bookstore;
drop database bookstore;
show databases;

-- 顯示表格參照資訊
select table_name, column_name, constraint_name, referenced_table_name,
referenced_column_name
from information_schema.key_column_usage
where referenced_table_schema = 'bookstore_test' and table_name = 'book';


-- ALTER TABLE
select detabase();

use bookstore_test;
  -- 表格更名
  alter table book rename to books;

  -- 新增欄位
  alter table books add column language varchar(40);

  -- 欄位更名
  alter table books rename column language to languages;

  -- 修改/刪除欄位預設值
  alter table books alter column languages set default 'chinese';
  alter table books alter column languages drop default;

  -- 修改欄位類型
  alter table books modify languages varchar(20);

  -- 刪除欄位
  alter table books drop column languages;

  -- 建立fk
  alter table books add constraint fk_book_publisher
  foreign key (publisher_id) references publisher (publisher_id);

  -- 移除fk
  alter table books drop foreign key fk_book_publisher;

  -- 欄位改為不可/可為空值
  alter table books modify author varchar(200) not null;
  alter table books modify author varchar(200) null;