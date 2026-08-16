# MySQL 帳號權限與 DataGrip 控制台操作筆記

記錄在 Docker MySQL 8.4 LTS 環境下，使用 DataGrip Query Console 設定帳號權限（`GRANT ALL PRIVILEGES`）與控制 `autocommit` 的具體步驟與排錯整理。

---

## 環境配置

MySQL 運行於 Docker 容器內，透過 `compose.yaml` 讀取同目錄下的 `.env`：

```1:5:mysql-learning/.env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=practice
MYSQL_USER=steve
MYSQL_PASSWORD=password
```

- 目標資料庫：`practice`
- 管理員帳號：`root` / `root`
- 預設使用者：`steve` / `password`
- 自建練習帳號：`dba`

---

## MySQL 使用者身分機制：`'user'@'host'`

MySQL 的帳號身分由「使用者名稱」與「允許連線的主機（Host）」共同組成：

| 身分形式 | 意義 | 適用場景 |
| :--- | :--- | :--- |
| `'dba'@'localhost'` | 僅限從 MySQL 容器內部本機連線 | 在 Docker 容器內開終端機直接登入 |
| `'dba'@'%'` | 允許從任何外部 IP 連線 | 從 Mac 本機的 DataGrip 或後端程式連入容器 |

### 常見連線失敗原因

DataGrip 運行在 Mac 本機，透過連接埠 `3306:3306` 連進 Docker 容器。對容器內的 MySQL 而言，這是外部網路連線，只會比對 `'dba'@'%'` 的權限。

如果只建立了 `'dba'@'localhost'`，DataGrip 連線時會直接回傳 `Access denied for user 'dba'@'...'`。要讓本機 DataGrip 正常連線，帳號與權限必須指定為 `'dba'@'%'`。

---

## 帳號建立與授權指令

### 完整授權語法

```sql
GRANT ALL PRIVILEGES
ON practice.*
TO 'dba'@'%';
```

- `GRANT ALL PRIVILEGES`：授予讀寫（`SELECT`, `INSERT`, `UPDATE`, `DELETE`）、結構異動（`CREATE`, `ALTER`, `DROP`）與管理權限。
- `ON practice.*`：指定權限範圍為 `practice` 資料庫下的所有資料表與檢視表（全域權限則寫為 `ON *.*`）。
- `TO 'dba'@'%'`：將權限賦予允許外部連線的 `dba` 帳號。

---

## DataGrip 實作步驟

1. 以 `root` 或 `steve` 連線進入 DataGrip，在目標連線上按 `F4` 開啟 **Query Console**。
2. 建立外部連線帳號並設定密碼：
   ```sql
   CREATE USER 'dba'@'%' IDENTIFIED BY '自訂密碼';
   ```
3. 授予 `practice` 資料庫權限並刷新快取：
   ```sql
   GRANT ALL PRIVILEGES ON practice.* TO 'dba'@'%';
   FLUSH PRIVILEGES;
   ```
4. 驗證權限：
   ```sql
   SHOW GRANTS FOR 'dba'@'%';
   ```

---

## 帳號排查與管理指令

### 查詢現有使用者與允許連線的 Host

```sql
SELECT user, host FROM mysql.user;
```

如果清單中 `dba` 的 host 只有 `localhost`，表示缺少外部連線設定，需要補建 `'dba'@'%'`。

### 刪除帳號

```sql
DROP USER 'dba'@'localhost';
DROP USER 'dba'@'%';
```

### 修改密碼

```sql
ALTER USER 'dba'@'%' IDENTIFIED BY '新密碼';
FLUSH PRIVILEGES;
```

---

## 交易控制與 autocommit 設定

MySQL 預設開啟自動提交（`autocommit = 1`），每行資料異動（`INSERT`, `UPDATE`, `DELETE`）執行後會立刻寫入硬碟，無法透過 `ROLLBACK` 復原。若要手動控制交易，需關閉自動提交。

### 1. 查詢 autocommit 狀態

```sql
-- 查詢當前連線（Session）
SELECT @@autocommit;
SELECT @@SESSION.autocommit;

-- 查詢伺服器全域預設值（Global）
SELECT @@GLOBAL.autocommit;

-- 使用 SHOW VARIABLES
SHOW VARIABLES LIKE 'autocommit';
```

- `1`（ON）：自動提交。
- `0`（OFF）：手動提交（異動需手動執行 `COMMIT` 才會寫入）。

---

### 2. 設定 autocommit 的 4 種方式與生命週期

| 設定方式 | 指令 | 影響範圍 | 失效條件 |
| :--- | :--- | :--- | :--- |
| 單次連線 (Session) | `SET autocommit = 0;` | 僅當前 Console 視窗 | 關閉視窗或斷線 |
| 記憶體全域 (Global) | `SET GLOBAL autocommit = 0;` | 之後建立的新連線（既有連線不變） | Docker 容器重啟 |
| 持久化設定 (Persist) | `SET PERSIST autocommit = 0;` | 寫入硬碟檔 `mysqld-auto.cnf`，全域生效 | 執行 `RESET PERSIST` |
| 容器啟動參數 | `command: --autocommit=0` | 寫入 `compose.yaml` | 修改設定檔 |

> `SET PERSIST` 會將設定寫入掛載的 Docker Volume（`mysql_data`），即使執行 `docker compose down` 再啟動，設定仍會保留。清除持久化設定指令為 `RESET PERSIST autocommit;`。

---

### 3. 排查：為什麼設定了全域 0，當前連線查詢仍為 1？

- **執行依據以 Session 為準**：只要 `@@SESSION.autocommit` 是 1，即使 `@@GLOBAL.autocommit` 是 0，語法執行後依然會立刻提交。
- **舊連線不更新**：`SET GLOBAL` 或 `SET PERSIST` 只影響新連線，已開啟的 Console 仍維持建立時的數值。
- **DataGrip 驅動預設覆蓋**：DataGrip 預設為 `Tx: Auto`，連線時 JDBC 驅動會主動執行 `SET autocommit = 1` 覆蓋伺服器設定。

**解法**：在 DataGrip Console 右上角將模式切換為 **`Tx: Manual`**，或在 Console 手動執行 `SET autocommit = 0;`。若要讓整組 Data Source 預設手動提交，可至連線屬性（Properties）-> **Options** -> 將 **Transaction control** 改為 **`Manual`**。

---

### 4. 關閉自動提交後的標準流程

```sql
-- 1. 執行資料變更（尚未寫入硬碟）
INSERT INTO practice.students (name, age) VALUES ('Alice', 20);

-- 2A. 確認無誤，提交寫入
COMMIT;

-- 2B. 發生錯誤，撤銷異動
ROLLBACK;
```

---

### 5. Python 程式碼中的交易機制（PEP 249）

Python 資料庫套件（如 `PyMySQL`、`mysqlclient`、`sqlite3`）遵循 PEP 249 規範，建立連線時會自動將連線設為 `autocommit = 0`。

因此開發後端時不需要改動 MySQL 伺服器的全域設定，只要在程式碼中撰寫標準交易結構：

```python
try:
    cursor.execute("UPDATE accounts SET balance = balance - 1000 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 1000 WHERE id = 2")
    conn.commit()
    print("交易成功")
except Exception as e:
    conn.rollback()
    print(f"交易失敗，已復原：{e}")
finally:
    cursor.close()
    conn.close()
```

---

## 各環境使用建議

| 環境 | 建議設定 | 原因 |
| :--- | :--- | :--- |
| **MySQL 伺服器** | `autocommit = 1` | 維持出廠預設，避免連線因未提交交易而鎖定資源。 |
| **Python 後端** | 程式碼控制（預設 `autocommit = 0`） | 依循 `try...commit...except rollback` 保護商業邏輯。 |
| **DataGrip 查詢** | `Tx: Auto` | 點選介面與查詢資料時操作最直接。 |
| **DataGrip 測試語法** | `Tx: Manual` 或 `SET autocommit = 0;` | 測試 `UPDATE` 或 `DELETE` 時可手動驗證與 `ROLLBACK`。 |
