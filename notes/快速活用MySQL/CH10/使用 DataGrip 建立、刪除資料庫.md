# 使用 DataGrip 建立與刪除資料庫教學指引

本教學以 JetBrains DataGrip 連線 MySQL 資料庫為核心，詳細說明如何透過「GUI 視覺化介面」與「SQL Query Console 控制台」兩種方式進行資料庫（Database / Schema）的建立、檢視、切換與安全刪除，並特別釐清 DataGrip 常見的介面名詞誤區與「資料庫建立後在導覽樹中消失」的顯示機制。

---

## 這份指引在講什麼

本篇專為使用 DataGrip 開發 MySQL 的工程師設計，用精確的「畫面方位」與「步驟分解」，完整拆解資料庫生命週期的核心操作。無需圖片也能依照畫面方位（左側工具列、右鍵選單、中心彈窗、下方預覽區）一步步完成建立與刪除，同時掌握字元集（Charset）與定序規則（Collation）的最佳設定。

---

## 學完要會什麼

1. 清楚辨識 DataGrip 介面版面佈局（左側 Database Explorer、中央 Editor/Console、底端狀態列）。
2. 理解 MySQL 中 `DATABASE` 與 `SCHEMA` 在 DataGrip 裡的對應關係。
3. 熟練使用 **GUI 視窗** 建立 MySQL 資料庫並配置 `utf8mb4` 與定序規則。
4. 熟練使用 **Query Console** 撰寫標準 SQL 語法建立與刪除資料庫。
5. 掌握 DataGrip 的 **Schemas 顯示過濾（Manage Shown Schemas / N of M）** 機制，解決「建立後看不到資料庫」的頭號痛點。
6. 理解安全刪除（Drop Database）的確認機制、潛在風險與 `IF EXISTS` 的防禦性寫法。

---

## 核心名詞與觀念辨析

在操作前，先釐清幾個 DataGrip 與 MySQL 容易混淆的概念：

- **Database 與 Schema 的關係**：
  - 在 Oracle 或 PostgreSQL 中，一個 Database 內部可包含多個 Schema，兩者是層級關係。
  - 在 **MySQL** 中，`DATABASE` 與 `SCHEMA` **完全同義**（`CREATE DATABASE` 與 `CREATE SCHEMA` 作用完全相同）。
  - **DataGrip 官方選單提示**：在連線 MySQL 時，DataGrip 右鍵選單主要顯示為 **`New | Schema`**（部分文檔通稱 Database），在 MySQL 環境下建立 Schema 即等同於建立 Database。
- **Database Explorer（資料庫總管）**：
  - DataGrip 畫面最左側的主要導覽面板（舊版本或 IntelliJ 整合版亦稱 Database 工具視窗）。
  - 快速鍵：macOS `Cmd + 1` / Windows & Linux `Alt + 1`。
- **Introspection（中繼資料載入）與 Schemas 過濾機制**：
  - DataGrip 為了避免大型專案卡頓，預設**不會自動把伺服器上的所有資料庫全部載入展開**。
  - 連線節點旁邊會標記灰色數字如 `1 of 5`（代表目前勾選顯示 5 個資料庫中的 1 個），未勾選的資料庫不會出現在左側樹狀清單中。

---

## 畫面整體佈局與方位導覽

在進行任何操作前，請先對照以下畫面方位分佈：

```
+--------------------------------------------------------------------------------------+
| 頂部主選單列 (Menu Bar): File, Edit, View, Tools, Window...                          |
+---------------------+----------------------------------------------------------------+
| 最左側窄條 (邊欄)   | 中央 / 右側主工作區 (Main Editor & Query Console)              |
| [資料庫圓柱圖示]    |                                                                |
|                     |  -- 可以在此撰寫與執行 SQL 語句 (Cmd+Enter / Ctrl+Enter)       |
| 展開之主要面板：    |  -- CREATE DATABASE / DROP DATABASE                           |
| 【Database Explorer】|                                                                |
|  - Data Source 節點 |                                                                |
|    └ 灰色 [1 of 4]  +----------------------------------------------------------------+
|    └ 🗄️ practice   | 下方結果面板 (Services / Output / Result Grid)                  |
|    └ 🗄️ my_new_db  |  -- 顯示 SQL 執行結果、受影響列數或錯誤訊息                     |
+---------------------+----------------------------------------------------------------+
```

---

## 方法一：使用 GUI 視覺化介面操作

### 1. 建立資料庫（Create Schema）

#### 操作步驟：
1. **定位左側導覽面板**：
   - 點擊 IDE 畫面最左側邊欄的 **資料庫圓柱圖示**，或按下快速鍵 `Cmd + 1`（macOS）/ `Alt + 1`（Windows），展開 **Database Explorer**。
2. **開啟新增選單**：
   - 在你的 MySQL 連線節點（例如 `Docker MySQL 8.4` 或 `localhost`）上 **按滑鼠右鍵**。
   - 在彈出的右鍵選單中，將滑鼠移至頂部的 **`New`**，在次級選單中點選 **`Schema...`**。
   - *(替代路徑：點選該連線節點後，直接點擊 Database Explorer 工具列頂端的 `+` 號，選擇 `Schema`)*。
3. **填寫建立資料庫彈窗（Create Schema 視窗）**：
   - 畫面中央會彈出一個名為 **Create Schema** 的設定對話框：
     - **Name（資料庫名稱）**：輸入你想建立的資料庫名稱（例如 `tibame_shop`）。
     - **Character set（字元編碼）**：從下拉選單選擇 **`utf8mb4`**（支援完整 Unicode 與 Emoji 表情符號）。
     - **Collate（定序規則）**：
       - 若為 MySQL 8.0 / 8.4+，推薦選擇 **`utf8mb4_0900_ai_ci`**（預設且效能最佳、不區分大小寫與重音符號）。
       - 若為舊版 MySQL 5.7 相容環境，可選擇 `utf8mb4_unicode_ci` 或 `utf8mb4_general_ci`。
4. **檢視與執行**：
   - 對話框下方會即時產生對應的 DDL 語句預覽（例如 `CREATE SCHEMA tibame_shop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;`）。
   - 確認無誤後，點選對話框右下角的 **`OK`**（或按 `Enter` / 點擊 `Execute`）送出執行。

---

### 2. 刪除資料庫（Drop Schema / Database）

> [!CAUTION]
> **危險操作警告**：刪除資料庫是不可逆的破壞性動作！一旦執行，該資料庫內的所有資料表、檢視表（View）、預存程序與所有資料列都會被立即清空且**無法從資源回收筒復原**。執行前請務必確認選中的資料庫名稱。

#### 操作步驟：
1. **定位目標資料庫**：
   - 在左側 **Database Explorer** 面板中，展開連線節點，找到你想刪除的資料庫名稱（例如 `tibame_shop`）。
2. **觸發刪除動作**：
   - **方式 A（鍵盤捷徑）**：選取該資料庫名稱，直接按下鍵盤的 **`Delete`** 鍵（macOS 筆電鍵盤為 `Delete` 或 `Cmd + Delete`）。
   - **方式 B（滑鼠右鍵）**：在目標資料庫上 **按滑鼠右鍵**，在彈出的選單中點選 **`Drop...`**（部分版本顯示為 **`Delete...`** 或位於 **`Object Actions | Drop...`**）。
3. **確認刪除彈窗（Confirm Drop 視窗）**：
   - 畫面中央會跳出 **Drop** 警告確認對話框：
     - 確認視窗中間列出的對象確實是你要刪除的資料庫。
     - **勾選項（可選）**：
       - `Use IF EXISTS syntax`：建議勾選，會自動在指令加上 `IF EXISTS`，避免物件不存在時報錯。
       - `Use DROP CASCADE syntax`：若存在依賴關聯時可一併級聯清理。
     - 視窗下方文字區塊會顯示即將執行的 SQL：`DROP SCHEMA `tibame_shop`;` 或 `DROP DATABASE ...;`。
4. **執行刪除**：
   - 點擊對話框右下角的 **`OK`**（或按下 `Enter`）正式執行刪除。
   - 左側導覽樹中的該資料庫節點將隨之消失。

---

## 方法二：使用 SQL Query Console 控制台操作

工程師在實際工作中最推薦、最精確的方法是直接透過 SQL 查詢控制台下達 DDL 指令。

### 1. 開啟 Query Console
1. 在左側 **Database Explorer** 的連線節點或任一資料庫上，按快捷鍵 **`F4`**（macOS/Windows 通用）。
2. 或在連線節點上按右鍵，選擇 **`New` -> `Query Console`**。
3. 中央主工作區會開啟一個全新的 SQL 編輯分頁。

---

### 2. 建立資料庫的標準 SQL 語法

在 Console 編輯區輸入以下語法：

```sql
-- 1. 建立資料庫（最基礎語法）
CREATE DATABASE IF NOT EXISTS tibame_shop;

-- 2. 建立資料庫並明確指定現代推薦字元編碼與定序規則（強烈推薦）
CREATE DATABASE IF NOT EXISTS tibame_shop
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
```

#### 語法解說：
- **`CREATE DATABASE`**：建立資料庫的核心關鍵字（在 MySQL 中亦可寫成 `CREATE SCHEMA`）。
- **`IF NOT EXISTS`**：防禦性語法。如果該名稱的資料庫已存在，則忽略不報錯，避免自動化腳本中斷。
- **`CHARACTER SET utf8mb4`**：指定資料庫預設字元集為 4 位元組 UTF-8，可完整儲存繁體中文、各國文字與 Emoji。
- **`COLLATE utf8mb4_0900_ai_ci`**：指定文字排序與比對規則（`ai` 代表重音不敏感 Accent-insensitive，`ci` 代表大小寫不敏感 Case-insensitive）。

#### 執行步驟：
1. 將輸入游標停留在該行 SQL 語句中任意位置（無需反白選取整段）。
2. 按下快速鍵 **`Cmd + Enter`**（macOS）或 **`Ctrl + Enter`**（Windows/Linux）。
3. 觀察下方 **Services / Output** 視窗，顯示 `1 row affected` 或綠色勾勾即代表建立成功。

---

### 3. 刪除資料庫的標準 SQL 語法

在 Console 編輯區輸入以下語法：

```sql
-- 安全刪除資料庫
DROP DATABASE IF EXISTS tibame_shop;
```

#### 語法解說：
- **`DROP DATABASE`**：完全刪除指定資料庫（包含其中所有資料表與內容）。在 MySQL 中亦可寫成 `DROP SCHEMA`。
- **`IF EXISTS`**：防禦性語法。若該資料庫不存在則靜默略過，不會拋出 `ERROR 1008 (HY000): Can't drop database '...'; database doesn't exist` 錯誤。

#### 執行步驟：
1. 游標停留在 `DROP DATABASE ...` 該行。
2. 按下 **`Cmd + Enter`**（macOS）或 **`Ctrl + Enter`**（Windows/Linux）執行。

---

## 關鍵避坑：為什麼建立資料庫後，左側樹狀圖沒出現？

這是新手使用 DataGrip 時最常遇到的困惑：「我明明執行了 `CREATE DATABASE` 且回傳成功，為什麼左側 Database Explorer 裡面找不到它？」

### 原因說明：
DataGrip 為了系統效能，採用了**中繼資料載入過濾（Introspection Filter）**機制。當新資料庫建立時，它可能尚未被納入「已顯示清單（Shown Schemas）」，或者尚未觸發重新中繼資料載入。

### 解決方法（三步驟）：

#### 步驟 1：點擊「N of M」綱要過濾器
- 在左側 **Database Explorer** 中，觀察你的連線節點名稱右側（例如 `Docker MySQL 8.4  1 of 4`）。
- 點擊那個灰色的 **`1 of 4`**（或數字標籤）。
- *(替代方式：在連線節點按右鍵，選擇 **`Tools` -> `Manage Shown Schemas...`**)*。

#### 步驟 2：勾選新建立的資料庫
- 彈出的選單中會列出 MySQL 伺服器上所有的資料庫。
- 找到你剛建立的資料庫名稱（例如 `tibame_shop`），將前面的核取方塊 **打勾**。
- *(若希望未來所有資料庫都自動顯示，可以直接勾選最上方的 **`All schemas`**)*。
- 按下鍵盤 `Enter` 或點擊空白處確認。

#### 步驟 3：手動重新整理（Refresh）
- 點選左側 Database Explorer 工具列頂端的 **圓形箭頭重新整理圖示（Refresh）**。
- 或在連線節點上按下快速鍵 **`Cmd + F5`**（macOS）/ **`Ctrl + F5`**（Windows）。
- 資料庫即會正確展示在左側樹狀清單中。

---

## 建立與刪除後常用操作補充

### 1. 切換當前作用資料庫（USE Database）
在 SQL Console 撰寫查詢前，需指定要在哪個資料庫工作：
```sql
USE tibame_shop;
```
*(在 DataGrip 中，也可以直接在 Query Console 視窗右上角的下拉選單切換當前活躍的 Schema/Database)*。

### 2. 查詢目前 MySQL 伺服器上的所有資料庫清單
```sql
SHOW DATABASES;
```

### 3. 查看特定資料庫的建立 DDL 資訊（確認編碼）
```sql
SHOW CREATE DATABASE tibame_shop;
```

---

## 總結與最佳實踐檢核清單

| 情境 / 需求 | 推薦方式 | 核心指令 / 操作路徑 |
| :--- | :--- | :--- |
| **快速視覺化建立** | GUI 視窗 | 右鍵連線節點 -> `New` -> `Schema...` -> 輸入名稱與編碼 -> `OK` |
| **精準/自動化建立** | SQL Console | `CREATE DATABASE IF NOT EXISTS <名稱> CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;` |
| **資料庫未在左側出現** | Schemas 過濾 | 點擊連線旁的 `N of M` 標籤 -> 勾選目標資料庫或 `All schemas` -> 按 `Cmd + F5` 重新整理 |
| **安全刪除資料庫** | SQL Console | `DROP DATABASE IF EXISTS <名稱>;` |
| **GUI 快速刪除** | 鍵盤/選單 | 選取資料庫節點 -> 按 `Delete` 鍵 -> 檢查預覽 SQL -> 點擊 `OK` |
