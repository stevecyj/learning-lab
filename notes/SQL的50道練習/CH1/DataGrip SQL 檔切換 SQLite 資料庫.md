---
created: 2026-08-20
tags:
  - SQL
  - SQLite
  - DataGrip
---

# DataGrip SQL 檔切換 SQLite 資料庫

## 問題情境

專案中有一個 `50-1.sql`，並設定了兩個 SQLite data source：

- `imdb.db`
- `covid19.db`

希望把查詢保存在同一個 SQL 檔案中，並決定查詢要在哪一個 SQLite 資料庫執行。

## 方法一：在 DataGrip 切換 SQL 檔的 data source

SQLite 沒有 MySQL 的 `USE database_name;`。SQL 要送到哪個資料庫，是由 DataGrip 綁定在這個 SQL 檔上的 data source 決定。

打開 `50-1.sql` 後，在 **SQL 程式碼編輯區本身頂端的工具列**，找到顯示 `No data source`、`imdb.db` 或 `covid19.db` 的下拉選單：

- 選 `imdb.db` 後，查詢 IMDB 的資料表。
- 選 `covid19.db` 後，查詢 COVID-19 的資料表。

這不是 DataGrip 整個視窗、Database Explorer 或查詢結果區的右上角，而是 `50-1.sql` 編輯區內的工具列。

如果工具列沒有顯示，可以打開 **Sessions** tool window，在其中找到 `50-1.sql`，對檔名按右鍵，再選 **Switch Data Source**。

### IMDB 範例

```sql
SELECT *
FROM movies
LIMIT 10;
```

### COVID-19 範例

```sql
SELECT *
FROM confirmed
LIMIT 10;
```

SQL 查詢會保存在 `50-1.sql`；SQL 檔與 data source 的關聯則由 DataGrip 保存，不會以 `USE` 指令寫入檔案。

## 方法二：同一次連線查詢兩個 SQLite 檔案

如果 `50-1.sql` 已經連到 `imdb.db`，IMDB 會是 `main`。可以再用 `ATTACH DATABASE` 掛載 COVID-19：

```sql
ATTACH DATABASE
    '/Volumes/data/Projects-practice/tibame/learning-lab/notes/SQL的50道練習/CH1/assets/covid19.db'
    AS covid19;
```

掛載後，用 `資料庫別名.資料表` 指定查詢來源：

```sql
-- IMDB
SELECT *
FROM main.movies
LIMIT 10;

-- COVID-19
SELECT *
FROM covid19.confirmed
LIMIT 10;
```

> [!warning]
> `ATTACH DATABASE` 是針對目前連線執行。相同連線已經掛載 `covid19` 時，再次執行同一條 `ATTACH`，會出現 `database covid19 is already in use`。建立新連線後則需要重新執行。

## 目前資料表

### IMDB

- `actors`
- `directors`
- `movies`
- `movies_actors`
- `movies_directors`
- `mpas`
- `release_info`

### COVID-19

- `confirmed`
- `deaths`
- `geographics`
- `iso_codes`

## 官方文件

- [DataGrip：Data source attachment](https://www.jetbrains.com/help/datagrip/run-sql-files.html#data-source-attachment)
- [SQLite：ATTACH DATABASE](https://www.sqlite.org/lang_attach.html)
