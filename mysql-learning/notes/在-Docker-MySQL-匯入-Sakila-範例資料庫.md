# 在 Docker MySQL 匯入 Sakila 範例資料庫

本篇說明如何把 MySQL 官方的 Sakila 範例資料庫，匯入由 `mysql-learning/compose.yaml` 建立的 MySQL 8.4 容器。

Sakila 模擬 DVD 出租店的資料，包含電影、演員、顧客、庫存、租借及付款紀錄，適合用來練習 SQL 查詢。

參考資料：[MySQL 官方 Sakila 安裝說明](https://dev.mysql.com/doc/sakila/en/sakila-installation.html)

---

## 安裝流程

整個流程分成五步：

1. 下載並解壓縮 Sakila。
2. 啟動 MySQL 容器。
3. 匯入資料庫結構。
4. 匯入範例資料。
5. 驗證安裝結果。

官方提供的兩個 SQL 檔必須依序執行：

- `sakila-schema.sql`：建立 `sakila` database、資料表、View、Stored Procedure 和 Trigger。
- `sakila-data.sql`：把電影、演員及租借紀錄等範例資料寫入已建立的資料表。

---

## 1. 進入專案目錄

開啟終端機，進入 `mysql-learning`：

```bash
cd /Users/steve.tsao/projects-practice/python-course/mysql-learning
```

後續指令都假設目前位於此目錄。

## 2. 下載並解壓縮 Sakila

從 MySQL 官方網站下載 ZIP 壓縮檔：

```bash
curl -LO https://downloads.mysql.com/docs/sakila-db.zip
```

解壓縮：

```bash
unzip sakila-db.zip
```

確認解壓縮後的檔案：

```bash
ls sakila-db
```

應該會看到：

```text
sakila-data.sql
sakila-schema.sql
sakila.mwb
```

`sakila.mwb` 是 MySQL Workbench 的資料模型，不需要匯入 MySQL。

## 3. 啟動 MySQL 容器

```bash
docker compose up -d
```

查看容器狀態：

```bash
docker compose ps
```

確認 `mysql-learning` 的狀態為 `Up (healthy)`。如果顯示 `health: starting`，代表 MySQL 還在初始化，可以稍後再檢查一次。

## 4. 匯入資料庫結構

先執行 `sakila-schema.sql`：

```bash
docker compose exec -T mysql \
  sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' \
  < sakila-db/sakila-schema.sql
```

這條指令依序做以下工作：

1. `< sakila-db/sakila-schema.sql` 從 Mac 本機讀取 SQL 檔。
2. `docker compose exec -T mysql` 在 Compose 的 `mysql` service 內執行命令。
3. `sh -c` 讓容器內的 Shell 展開 `MYSQL_ROOT_PASSWORD` 環境變數。
4. `mysql -uroot` 使用 root 帳號連線 MySQL。
5. MySQL client 執行 SQL，建立名為 `sakila` 的 database 及其結構。

### `-T` 是什麼？

`docker compose exec` 預設會配置虛擬終端機（TTY），讓使用者可以在容器內進行互動操作。例如，以下指令會開啟一個可互動的 Shell：

```bash
docker compose exec mysql bash
```

但是，匯入 Sakila 時不是由使用者逐行輸入 SQL，而是透過 `<` 把整個 SQL 檔送進容器：

```text
sakila-schema.sql
        ↓
Shell 的輸入重新導向 <
        ↓
容器內的 MySQL client
        ↓
MySQL Server
```

因此，指令使用 `-T` 停用 TTY，讓 SQL 檔能直接作為 MySQL client 的標準輸入（Standard Input，stdin）：

```bash
docker compose exec -T mysql ... < sakila-schema.sql
```

可以這樣區分：

- 需要在容器內互動操作：通常不加 `-T`。
- 要從檔案或 Pipe 輸入資料：加上 `-T`。

`-T` 和 Docker 指令中常見的 `-t` 意義相反：

- `-t`：配置 TTY。
- `-T`：停用 TTY。

這裡使用 root，是因為 `MYSQL_USER` 建立的一般帳號通常只有 `MYSQL_DATABASE` 指定之 database 的權限，不一定能建立新的 `sakila` database。

成功時通常不會顯示訊息。

## 5. 匯入範例資料

資料庫結構建立完成後，再執行 `sakila-data.sql`：

```bash
docker compose exec -T mysql \
  sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' \
  < sakila-db/sakila-data.sql
```

這一步會把範例資料寫入剛建立的 `sakila` database。成功時通常也不會顯示訊息。

---

## 驗證安裝結果

### 確認 database 存在

```bash
docker compose exec mysql \
  sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;"'
```

輸出中應包含：

```text
sakila
```

### 查看 tables 和 views

```bash
docker compose exec mysql \
  sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SHOW FULL TABLES FROM sakila;"'
```

### 確認電影資料筆數

```bash
docker compose exec mysql \
  sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SELECT COUNT(*) AS film_count FROM sakila.film;"'
```

預期結果：

```text
film_count
1000
```

### 查詢前五部電影

```bash
docker compose exec mysql \
  sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SELECT film_id, title, release_year FROM sakila.film LIMIT 5;"'
```

---

## 進入互動式 MySQL Client

安裝完成後，可以直接進入 `sakila` database 練習 SQL：

```bash
docker compose exec mysql \
  sh -c 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" sakila'
```

進入後執行：

```sql
SHOW TABLES;

SELECT *
FROM actor
LIMIT 10;
```

離開 MySQL client：

```sql
exit;
```

---

## `MYSQL_DATABASE` 與 `sakila` 的關係

`compose.yaml` 中的設定：

```yaml
MYSQL_DATABASE: ${MYSQL_DATABASE}
```

只會在 MySQL 第一次初始化空白 Named Volume 時，自動建立 `.env` 指定的 database。它不會限制 MySQL server 只能擁有一個 database。

匯入 Sakila 後，同一個 MySQL server 可以同時包含：

```text
${MYSQL_DATABASE}
sakila
mysql
performance_schema
sys
```

`mysql_data` Named Volume 會保存這些資料。執行以下指令只會移除容器和 Compose 網路，資料仍然保留：

```bash
docker compose down
```

以下指令則會連同 Named Volume 一起刪除，所有 MySQL 資料都會消失：

```bash
docker compose down -v
```

除非確定要清空整個 MySQL 環境，否則不要加上 `-v`。

---

## 完整邏輯

先從官方網站下載兩個 SQL 檔，再啟動 Docker 中的 MySQL。接著先匯入 `sakila-schema.sql` 建立資料庫骨架，再匯入 `sakila-data.sql` 寫入範例資料。最後檢查 `sakila.film` 是否有 1,000 筆資料。

這套操作假設 Docker、Docker Compose、`curl` 和 `unzip` 已安裝，且 `.env` 中的 `MYSQL_ROOT_PASSWORD` 設定正確。它會把 Sakila 加入現有 MySQL server，不會取代 `MYSQL_DATABASE` 原本建立的 database。
