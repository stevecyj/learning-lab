-- 查詢目前 SQLite 資料庫中的所有資料表名稱
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;

-- 查詢 IMDB 的前 5 筆演員資料
select *
from movies
limit 5;

-- 查詢 COVID-19 的前 5 筆確診資料
select *
from geographics
limit 5;

-- 排序
select title,
       runtime
from movies
order by runtime;

-- 連接鍵與主鍵相連接
select movies.title, release_info.country, release_info.released_on
from release_info
         join movies on release_info.movie_id = movies.id
where movies.id = 1
  and release_info.country = 'Taiwan';

-- meta data
select *
from pragma_table_info('movies');
