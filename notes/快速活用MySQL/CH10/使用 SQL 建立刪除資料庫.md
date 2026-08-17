# 使用 SQL 建立與刪除資料庫

說明如何使用 SQL 指令在 MySQL 中建立與刪除資料庫，以及 MySQL Workbench 的執行模式與快取更新機制。

---

## 1. 這堂課真正要解決的問題

透過圖形介面（GUI）點選建庫與刪庫雖然方便，但無法寫入腳本、無法放入 Git 版本控制，也無法在自動化流程中重複執行。

本課要解決兩個具體問題：
1. **用 SQL 控制資料庫生命週期**：使用 `CREATE` 與 `DROP` 指令建立與刪除資料庫。
2. **掌握 IDE 執行範圍與畫面同步**：分清 Workbench「單行執行」與「選取/全檔執行」的差異，並理解伺服器真實狀態與畫面清單更新的落差。

---

## 2. 核心概念

### 概念一：資料庫建立與刪除指令 (`CREATE DATABASE` / `DROP DATABASE`)
- **它是什麼**：SQL 的資料定義語言（DDL），用來建立或刪除整個資料庫。
- **為什麼存在**：提供標準文字指令，讓建庫與刪庫可以被腳本化與自動化執行。
- **解決什麼問題**：解決手動建庫無法跨機器自動重現、測試環境無法自動重置的問題。
- **何時使用**：新專案初始化、建立或清空測試環境、執行資料庫遷移（Migration）腳本。
- **何時不適合使用**：正式營運環境嚴禁隨意執行 `DROP`；若只需清空單一資料表的內容，應使用 `TRUNCATE` 或 `DELETE`，而不是刪除整個資料庫。

### 概念二：語法等價性 (`DATABASE` 與 `SCHEMA` 在 MySQL 中完全相同)
- **它是什麼**：在 MySQL 中，`CREATE DATABASE` 與 `CREATE SCHEMA`（以及 `DROP DATABASE` 與 `DROP SCHEMA`）語意完全相同。
- **為什麼存在**：相容 ANSI SQL 標準，並相容其他關聯式資料庫開發者的習慣。
- **解決什麼問題**：減少從其他資料庫系統轉換過來的語法記憶成本。
- **何時使用**：撰寫建庫腳本時任選一種，並在專案內保持命名風格一致。
- **何時不適合使用**：若系統未來需移植到 PostgreSQL 或 Oracle，需注意這兩者中 Database 與 Schema 是階層關係（一個 Database 內有多個 Schema），不可混為一談（*延伸知識*）。

### 概念三：用戶端快取與重刷機制 (Client Cache vs Server State)
- **它是什麼**：Workbench 左側導覽列顯示的清單是本地快取，不會主動向伺服器即時輪詢更新。
- **為什麼存在**：避免頻繁向資料庫伺服器發送中繼資料查詢，降低伺服器與網路負擔。
- **解決什麼問題**：平衡用戶端操作流暢度與伺服器效能。
- **何時使用**：執行完 `CREATE` 或 `DROP` 後，若左側清單未更新，點擊「Refresh（重刷）」按鈕同步狀態。
- **何時不適合使用**：若已直接下 SQL 指令（如 `SHOW DATABASES;`）查詢伺服器，伺服器會直接回傳真實狀態，不需要看介面導覽列。

### 概念四：IDE 執行範圍控制 (單行執行 vs 選取/全檔執行)
- **它是什麼**：Workbench 工具列提供「帶游標閃電」與「無游標閃電」兩種執行模式。
- **為什麼存在**：SQL 檔案常包含多段語句，開發者需要手動決定是單步測試還是整批執行。
- **解決什麼問題**：避免在多語句檔案中誤觸全域執行，導致連帶執行危險指令。
- **何時使用**：
  - **帶游標閃電**：游標停在該行即可單獨執行該句，適合逐步除錯。
  - **無游標閃電**：反白選取特定區塊後執行；若未反白任何文字，會直接從頭到尾執行整份檔案。
- **何時不適合使用**：若檔案中同時寫了 `CREATE` 與 `DROP`，切勿在未選取文字的狀態下點擊無游標閃電。

---

## 3. Mental Model

### 執行流程與狀態變化

```
[ 開發者於 SQL 編輯區 ]
      │
      │ 1. 輸入指令 (如 CREATE DATABASE bookshop;)
      │ 2. 選擇執行方式 (帶游標閃電 或 選取後點無游標閃電)
      ▼
[ MySQL Workbench (Client) ]
      │
      │ 3. 透過網路發送 SQL 請求
      ▼
[ MySQL Server (Engine) ]
      │
      │ 4. 檢查語法與權限
      │ 5. 於資料目錄建立或刪除資料庫實體結構
      │ 6. 更新內部 Data Dictionary
      │
      ├─── 回傳執行成功訊息 ───► [ Workbench 下方 Output 顯示綠色勾勾 ]
      │
      └─── (伺服器真實狀態已更新)
            :
            : (此時 Client 左側導覽列尚未向伺服器重新索取清單)
            :
[ 開發者點擊 Refresh 按鈕 ] ─── 查詢最新中繼資料 ───► [ Client 更新左側 Schemas 清單 ]
```

---

## 4. 專家視角

### 初學者需要知道，但資深工程師通常不會特別思考的內容
1. **同義語法**：`CREATE SCHEMA` 與 `CREATE DATABASE` 在 MySQL 中完全一樣。
2. **圖示區別**：Workbench 的帶游標閃電是跑單行，無游標閃電是跑選取區塊或整份檔案。
3. **介面未同步不等於執行失敗**：下方 Output 出現綠色勾勾代表伺服器已執行成功，左側沒更新按 Refresh 即可。

### 即使是資深工程師仍然會注意的內容
1. **`DROP DATABASE` 無法復原**：DDL 指令在 MySQL 會直接觸發隱式提交（Implicit Commit），無法用 `ROLLBACK` 復原，一旦刪除就是清空整個資料庫所有資料表與資料。
2. **腳本的冪等性（Idempotency）**：正式遷移腳本中，通常會加上防禦性判斷（如 *延伸知識：`IF NOT EXISTS` / `IF EXISTS`*），避免重複執行時報錯中斷。
3. **混合指令檔案的執行風險**：同一檔案同時存在 `CREATE` 與 `DROP` 時，避免使用全檔執行，以免誤砍資料庫。

---

## 5. 語法 vs 通用知識

| 分類 | 具體內容 | 通用程式設計對應觀念 |
| :--- | :--- | :--- |
| **MySQL 特有知識** | `CREATE DATABASE <名稱>;`<br>`CREATE SCHEMA <名稱>;`<br>`DROP DATABASE <名稱>;`<br>`DROP SCHEMA <名稱>;` | MySQL 特有的同義詞機制。其他資料庫（如 PostgreSQL）中 Database 與 Schema 是不同的階層。 |
| **Workbench 特有知識** | 帶游標閃電 vs 無游標閃電 | 資料庫開發工具（IDE）中「單行執行」與「批次執行」的快捷操作。 |
| **通用觀念** | **宣告式資源生命週期管理** | 以程式碼定義資源的建立與銷毀，類似 Docker 的 `create` / `rm` 或 Terraform 的資源宣告。 |
| **通用觀念** | **客戶端快取與真相來源 (Single Source of Truth)** | 介面顯示的只是本地快照，伺服器才是真實資料來源，兩者需要手動或被動同步。 |
| **通用觀念** | **破壞性操作防禦** | 具有不可逆破壞性的操作（如刪除資料庫、清除檔案）需要明確的執行範圍確認與權限控管。 |

---

## 6. Trade-off

### 比較：GUI 介面點選 vs 撰寫 SQL 腳本

| 比較項目 | GUI 介面點選 | 撰寫 SQL 腳本 |
| :--- | :--- | :--- |
| **操作難度** | 低（不用記語法，點按鈕即可） | 中（需記住指令關鍵字與語法規則） |
| **自動化與重現性** | 無（換環境必須手動重按） | 高（可在新環境一鍵執行） |
| **版本控制** | 無法放入 Git 追蹤變更 | 可納入 Git 記錄修改歷史與 Code Review |
| **失誤風險** | 人工容易點錯選項或漏設設定 | 腳本經檢查後執行較穩定，但全檔執行需注意 `DROP` |
| **適用場景** | 本機快速臨時測試 | 團隊協作、正式環境建置、測試環境自動初始化 |

---

## 7. 常見誤解

### 誤解一：執行 `CREATE DATABASE` 且下方出現綠色勾勾，但左側清單沒出現，代表建立失敗？
> **事實**：下方綠色勾勾表示伺服器已建立完成。左側未出現只是 Workbench 尚未重新抓取清單，點擊 Refresh 即可顯示。

### 誤解二：在 MySQL 中，`CREATE SCHEMA` 會在資料庫底下建立子目錄或子層級？
> **事實**：在 MySQL 內部，`SCHEMA` 與 `DATABASE` 完全同義，建立出來的都是獨立的資料庫實體。

### 誤解三：游標停在 `DROP DATABASE` 那一行，按無游標閃電只會執行那一行？
> **事實**：無游標閃電是「執行選取範圍或整份檔案」。未反白文字時，會從檔案第一行依序執行到最後一行。

### 誤解四：誤執行 `DROP DATABASE` 後，可以用 `ROLLBACK` 復原？
> **事實**：`DROP DATABASE` 是 DDL 指令，執行後立即生效且無法透過交易回滾復原。

---

## 8. Code Prediction — 請先作答

閱讀以下三段 SQL，預測：
1. **執行結果**（成功/失敗/報錯）
2. **原因**
3. **資料庫內部狀態變化**

### 題目一
```sql
CREATE DATABASE shop_db;
CREATE SCHEMA shop_db;
```
> **情境**：在同一台 MySQL 伺服器上依序執行上述兩行。預測第二行執行時的結果與原因。

### 題目二
```sql
CREATE DATABASE inventory_v1;
DROP SCHEMA inventory_v1;
DROP DATABASE inventory_v1;
```
> **情境**：依序執行上述三行。預測第三行執行時的結果。

### 題目三
```sql
-- 檔案：init_db.sql
CREATE DATABASE report_system;
DROP DATABASE report_system;
```
> **情境**：在 Workbench 開啟此檔案，未反白任何文字，直接點擊無游標閃電（執行全檔）。預測執行完畢後伺服器上是否存在 `report_system` 資料庫？為什麼？

---

## 9. Bug Hunt — 請先作答

找出以下兩段內容的問題、說明原因並提供修正方式。

### 題目一
```sql
CREATE DATABASE app_demo
CREATE DATABASE test_demo;
```
在 Workbench 中反白選取這兩行執行，系統回報語法錯誤（Syntax Error）。問題出在哪裡？如何修正？

### 題目二
```sql
DROP DATABASE staging_db;
CREATE DATABASE staging_db;
```
在一台從未建立過 `staging_db` 的全新伺服器上全檔執行此腳本，第一行直接報錯中斷，第二行未執行。
1. 為什麼會報錯？
2. 依本課所學，如何調整操作順序？
3. *(延伸思考)*：實務上有什麼 SQL 語法可以讓「資料庫不存在時不報錯並繼續往下執行」？

---

## 10. Coding Challenge

### 目標：測試環境重置腳本
撰寫一份 SQL 腳本，完成以下步驟：
1. 刪除已存在的舊資料庫 `learning_lab`。
2. 建立全新的資料庫 `learning_lab`。
3. 使用等價的另一種關鍵字（`SCHEMA`）建立備用資料庫 `learning_lab_backup`。
4. 每行 SQL 皆需有正確的結束符號。
5. **挑戰延伸 (Stretch Goal)**：為建庫語法加上繁體中文 UTF-8 編碼設定（提示：`CHARACTER SET` 與 `COLLATE`，屬延伸知識）。

---

## 11. Retrieval Practice — 請先作答

不看筆記，用自己的話回答：

1. **[Why] 為什麼在專案中建立與刪除資料庫應使用 SQL 腳本，而不是每次手動在介面點選？**
2. **[How] 在 Workbench 執行 `CREATE DATABASE` 成功後，左側清單若未出現該資料庫，標準排除步驟是什麼？**
3. **[Trade-off] 在 Workbench 中，「單行執行（帶游標閃電）」與「全檔執行（無游標閃電）」各有什麼優點與風險？**
4. **[Prediction] 依序執行 `CREATE DATABASE demo;`、`DROP SCHEMA demo;`、`CREATE SCHEMA demo;`，最終結果為何？`DATABASE` 與 `SCHEMA` 是否會發生名稱衝突？**
5. **[Application] 在自動化測試或 Docker 環境初始化時，SQL 建庫腳本的作用是什麼？**

---

## 12. 下一步

### 學完應掌握的技能：
- 使用 `CREATE DATABASE` 與 `CREATE SCHEMA` 建立資料庫。
- 使用 `DROP DATABASE` 與 `DROP SCHEMA` 刪除資料庫。
- 區分 Workbench 中單行執行與選取/全檔執行的操作方式。
- 理解介面快取與點擊 Refresh 同步狀態的原因。
- 注意 `DROP` 的不可逆性與全檔執行的操作風險。

### 接續學習概念：
1. **切換使用資料庫 (`USE <database_name>;`)**：指定連線進入該資料庫，才能在內部建立資料表。
2. **定義資料表結構 (`CREATE TABLE` / `DROP TABLE`)**：在資料庫內規劃欄位、資料型態與主鍵。
3. **字元集與定序規則 (`CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci`)**：設定編碼以支援中文與 Emoji 儲存。
