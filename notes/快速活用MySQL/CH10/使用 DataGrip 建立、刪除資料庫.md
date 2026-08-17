# 使用 DataGrip 建立與刪除資料庫

說明如何在 JetBrains DataGrip 中連線 MySQL，透過 GUI 介面與 Query Console 建立、管理與刪除資料庫（Schema），並解決新建資料庫未出現在導覽樹中的顯示設定問題。

---

## 這份指引在講什麼

本篇整理 DataGrip 管理 MySQL 資料庫的操作步驟。內容包含介面版面方位、GUI 與 SQL 兩種建庫與刪庫方式、字元編碼（`utf8mb4`）設定，以及 Schemas 顯示過濾機制的排除方法。

---

## 學完要會什麼

1. 辨識 DataGrip 主要介面區塊（Database Explorer、Query Console、執行結果面板）。
2. 理解 MySQL 中 `DATABASE` 與 `SCHEMA` 在 DataGrip 選單的對應關係。
3. 透過 GUI 視窗建立資料庫，並設定字元集與定序規則。
4. 使用 Query Console 撰寫 SQL 建立與刪除資料庫。
5. 透過 Schemas 過濾設定（Manage Shown Schemas / N of M）切換資料庫顯示狀態。
6. 理解刪除資料庫的不可逆風險與 `IF EXISTS` 防禦語法。

---

## 核心名詞與觀念

- **Database 與 Schema**：
  - 在 PostgreSQL 或 Oracle 中，Database 與 Schema 是包含關係。
  - 在 MySQL 中，`DATABASE` 與 `SCHEMA` 完全同義。
  - DataGrip 連線 MySQL 時，右鍵選單的 **`New | Schema`** 即對應建立 MySQL Database。
- **Database Explorer**：
  - DataGrip 左側主要的資料庫物件導覽面板（快速鍵：macOS `Cmd + 1` / Windows `Alt + 1`）。
- **Introspection（中繼資料載入）與 Schemas 過濾**：
  - DataGrip 預設只載入與解析勾選的資料庫，避免大型連線效能低落。
  - 連線節點旁的灰色標籤（如 `1 of 5`）表示當前載入的資料庫數量，未勾選者不會顯示在樹狀清單中。

---

## 畫面版面配置

```
+--------------------------------------------------------------------------------------+
| 頂部主選單列: File, Edit, View, Tools, Window...                                     |
+---------------------+----------------------------------------------------------------+
| 左側邊欄圖示        | 中央主工作區 (Query Console / SQL Editor)                      |
| [資料庫圓柱圖示]    |                                                                |
|                     |  - 撰寫與執行 SQL 語句 (Cmd + Enter / Ctrl + Enter)            |
| 展開之主要面板：    |  - CREATE DATABASE / DROP DATABASE                             |
| 【Database Explorer】|                                                                |
|  - Data Source 節點 |                                                                |
|    └ 灰色 [1 of 4]  +----------------------------------------------------------------+
|    └ practice       | 下方面板 (Services / Output / Result Grid)                     |
|    └ my_new_db      |  - 顯示 SQL 執行狀態、受影響列數與錯誤訊息                     |
+---------------------+----------------------------------------------------------------+
```

---

## 方法一：使用 GUI 介面操作

### 1. 建立資料庫（Create Schema）

#### 操作步驟：
1. **開啟左側面板**：
   - 點擊左側邊欄的資料庫圖示，或按 `Cmd + 1`（macOS）/ `Alt + 1`（Windows），展開 **Database Explorer**。
2. **開啟新增選單**：
   - 在 MySQL 連線節點（如 `Docker MySQL 8.4`）按右鍵。
   - 選擇 **`New` -> `Schema...`**。
   - （或選取連線節點後，點擊 Database Explorer 頂端的 **`+`** 號，選擇 **`Schema`**）。
3. **填寫設定對話框（Create Schema）**：
   - **Name**：輸入資料庫名稱（例如 `tibame_shop`）。
   - **Character set**：選擇 **`utf8mb4`**。
   - **Collate**：
     - MySQL 8.0 / 8.4+ 選擇 **`utf8mb4_0900_ai_ci`**。
     - MySQL 5.7 相容環境選擇 `utf8mb4_unicode_ci` 或 `utf8mb4_general_ci`。
4. **送出執行**：
   - 視窗下方會顯示生成的 DDL 語句（如 `CREATE SCHEMA tibame_shop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;`）。
   - 點擊右下角 **`OK`** 完成建立。

---

### 2. 刪除資料庫（Drop Schema / Database）

> [!CAUTION]
> 刪除資料庫會連同內部所有資料表與資料一併清除，無法復原。執行前請確認目標資料庫名稱。

#### 操作步驟：
1. **選取目標資料庫**：
   - 在左側 **Database Explorer** 中，展開連線節點並點選要刪除的資料庫名稱。
2. **觸發刪除**：
   - 按鍵盤 **`Delete`** 鍵（macOS：`Delete` 或 `Cmd + Delete`）。
   - 或在資料庫名稱上按右鍵，選擇 **`Drop...`**（部分介面版本顯示為 `Delete...` 或位於 `Object Actions | Drop...`）。
3. **確認刪除對話框（Confirm Drop）**：
   - 確認畫面上列出的資料庫名稱無誤。
   - 選項設定：
     - `Use IF EXISTS syntax`：建議勾選，避免物件不存在時報錯。
     - `Use DROP CASCADE syntax`：若有依賴物件需一併清理時可勾選。
   - 下方預覽區會顯示將執行的 SQL（`DROP SCHEMA `tibame_shop`;`）。
4. **確認執行**：
   - 點擊 **`OK`** 執行刪除，左側導覽樹中的該資料庫節點隨即移除。

---

## 方法二：使用 Query Console 執行 SQL

### 1. 開啟 Query Console
1. 選取左側連線節點或資料庫，按 **`F4`**。
2. 或在連線節點按右鍵，選擇 **`New` -> `Query Console`**。
3. 中央工作區即開啟 SQL 編輯分頁。

---

### 2. 建立資料庫語法

在 Console 輸入：

```sql
-- 基礎語法
CREATE DATABASE IF NOT EXISTS tibame_shop;

-- 指定字元集與定序規則（推薦）
CREATE DATABASE IF NOT EXISTS tibame_shop
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
```

- **`CREATE DATABASE`**：建立資料庫（在 MySQL 中亦可寫為 `CREATE SCHEMA`）。
- **`IF NOT EXISTS`**：若資料庫已存在則略過，不中斷後續腳本。
- **`CHARACTER SET utf8mb4`**：設定字元編碼支援完整 UTF-8（含中文與 Emoji）。
- **`COLLATE utf8mb4_0900_ai_ci`**：設定大小寫不敏感與重音不敏感的比對定序。

#### 執行方式：
1. 游標停留在該行 SQL。
2. 按 **`Cmd + Enter`**（macOS）或 **`Ctrl + Enter`**（Windows/Linux）。
3. 下方結果面板顯示成功訊息即完成。

---

### 3. 刪除資料庫語法

在 Console 輸入：

```sql
-- 刪除資料庫
DROP DATABASE IF EXISTS tibame_shop;
```

- **`DROP DATABASE`**：刪除指定資料庫與所有內容（亦可寫為 `DROP SCHEMA`）。
- **`IF EXISTS`**：若資料庫不存在則略過，避免拋出錯誤。

#### 執行方式：
1. 游標停留在該行語句。
2. 按 **`Cmd + Enter`**（macOS）或 **`Ctrl + Enter`**（Windows/Linux）執行。

---

## 常見問題：新建資料庫未出現在左側樹狀清單

### 原因
DataGrip 預設只載入與解析勾選的資料庫（Introspection）。在 Console 透過 SQL 建立新庫後，若該庫未被納入顯示清單，不會自動出現在左側面板。

### 解決步驟

1. **開啟 Schemas 篩選選單**：
   - 點擊連線節點右側的灰色數字標籤（例如 `1 of 4`）。
   - 或在連線節點按右鍵，選擇 **`Tools` -> `Manage Shown Schemas...`**。
2. **勾選目標資料庫**：
   - 在彈出清單中，勾選新建立的資料庫（或勾選最上方的 **`All schemas`** 顯示全部）。
   - 按 `Enter` 關閉選單。
3. **重新整理中繼資料**：
   - 點擊 Database Explorer 工具列頂端的 **Refresh** 圖示。
   - 或在連線節點按快速鍵 **`Cmd + F5`**（macOS）/ **`Ctrl + F5`**（Windows）。

---

## 常用相關指令

```sql
-- 切換目前使用的資料庫
USE tibame_shop;

-- 列出伺服器上所有資料庫
SHOW DATABASES;

-- 檢查指定資料庫的建立語法與編碼設定
SHOW CREATE DATABASE tibame_shop;
```

---

## 快速速查表

| 操作目標 | GUI 路徑 | SQL 語法 |
| :--- | :--- | :--- |
| **建立資料庫** | 連線節點右鍵 -> `New` -> `Schema...` -> 設定編碼 -> `OK` | `CREATE DATABASE IF NOT EXISTS <名稱> CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;` |
| **刪除資料庫** | 選取資料庫 -> 按 `Delete` 鍵 -> `OK` | `DROP DATABASE IF EXISTS <名稱>;` |
| **顯示未列出的資料庫** | 點擊連線旁 `N of M` 標籤 -> 勾選目標資料庫 -> 按 `Cmd + F5` 重新整理 | `SHOW DATABASES;` |
| **切換資料庫** | 於 Console 右上角下拉選單切換 | `USE <名稱>;` |
