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
