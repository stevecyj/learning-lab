# DataGrip 連線與高效開發設定指引

使用 JetBrains DataGrip 連線至 Docker 容器中的 MySQL 8.4 LTS 資料庫。包含連線組態配置、Driver 驅動管理、Schemas 範圍設定、Query Console 查詢技巧、Result Grid 即時資料編輯、Mock 資料匯出、ER 圖生成以及常用快速鍵速查。

---

## 這份指引在講什麼

本篇以 JetBrains DataGrip 作為唯一的圖形化資料庫開發工具（IDE），詳細說明如何連接至透過 Docker Compose 運行的 MySQL 8.4 LTS 容器。內容聚焦在現代資料庫開發工作流，協助工程師從傳統介面思維無縫切換到專業的 IDE 操作體系。

---

## 學完要會什麼

1. 掌握 DataGrip Data Source 設定流程，正確連線至本機 Docker Port 3306。
2. 理解 Schemas 作用範圍，避免因過濾設定導致資料庫未顯示在導覽樹中。
3. 熟練使用 Query Console 執行 SQL 語句（游標識別、區塊執行、交易控制）。
4. 運用 Result Grid 進行資料列編輯、暫存提交（Submit/Revert）與一鍵導出為 JSON/CSV 等格式。
5. 善用 DDL 導航（`Cmd + B`）、視覺化資料表修改與 ER 關聯圖生成。
6. 排查連線異常（如 Docker 容器尚未就緒、連接埠被佔用或 JDBC Driver 缺失）。

---

## 核心名詞與連線架構

- **Data Source（資料來源）**：DataGrip 管理資料庫連線的單位，包含主機位址、埠號、驗證資訊與驅動程式。
- **JDBC Driver（Java 資料庫連接驅動）**：DataGrip 與 MySQL 溝通的底層中介程式。DataGrip 內建自動下載與版本管理機制。
- **Docker Port Mapping（3306:3306）**：MySQL 在 Docker 容器內部運行，透過 Compose 將容器內的 `3306` 埠映射到 Mac 本機的 `localhost:3306`，DataGrip 連線時目標填寫 `localhost` 即可。
- **Schemas（綱要／資料庫）**：MySQL 中的 Database。DataGrip 採用按需載入（Introspect）機制，只會分析勾選的資料庫。
- **Query Console（查詢控制台）**：獨立的 SQL 編輯空間，綁定特定的連線 Session 與當前活躍資料庫。

---

## 連線至 Docker MySQL 8.4 完整步驟

在設定前，請確認 Docker MySQL 容器已啟動且處於 `Healthy` 狀態（可執行 `docker compose ps` 確認）。

### 步驟 1：建立 MySQL Data Source

1. 開啟 DataGrip。
2. 在左側 **Database Explorer** 工具面板（快速鍵 `Cmd + 1`），點選左上角的 **`+`**。
3. 依序選擇 **Data Source** -> **MySQL**。

### 步驟 2：下載與驗證 JDBC Driver

- 首次設定時，視窗下方若出現警告提示：`Download missing driver files`。
- 點擊 **Download**，DataGrip 會自動從官方倉庫下載相容於 MySQL 8.x/8.4 的 JDBC 驅動套件，不需要手動至官網抓取 `.jar` 檔案。

### 步驟 3：設定連線參數

在 **General** 分頁填寫以下設定（對應專案的 `compose.yaml` 與 `.env`）：

| 設定欄位 | 填寫內容 | 說明 |
| :--- | :--- | :--- |
| **Name** | `Docker MySQL 8.4 (practice)` | 連線自訂名稱，便於在專案多資料庫中辨識 |
| **Host** | `localhost`（或 `127.0.0.1`） | 本機主機位址（由 Docker 端口映射） |
| **Port** | `3306` | 本機通訊埠 |
| **Authentication** | `User & Password` | 採用標準使用者名稱與密碼驗證 |
| **User** | `steve`（或最高管理者 `root`） | 日常開發帳號或 root 帳號 |
| **Password** | `password`（或 root 密碼 `root`） | 對應 `.env` 中設定的密碼 |
| **Database** | `practice` | 預設連入的目標資料庫名稱 |

### 步驟 4：設定 Schemas 顯示範圍（關鍵步驟）

DataGrip 為了效能最佳化，預設可能只載入預設資料庫。若想在左側導覽面板隨時切換不同 Database：

1. 在連線設定視窗頂部切換至 **Schemas** 分頁。
2. 勾選 **`practice`**（或直接勾選 **All schemas**）。
3. 點擊視窗右下角 **Apply**。

### 步驟 5：測試連線與完成

1. 點擊視窗左下角的 **Test Connection** 按鈕。
2. 出現綠色勾勾圖示、顯示 `Succeeded` 與 MySQL 8.4 版本字樣即代表連線完全成功。
3. 點擊 **OK** 關閉設定視窗。

---

## DataGrip 核心功能與現代開發工作流

### 1. Query Console 執行技巧

開啟 Console：在左側 Database Explorer 的資料庫節點按 `F4`，或右鍵點選 **New** -> **Query Console**。

- **智慧語句偵測（Smart Statement Execution）**：
  - 將游標停留在要執行的 SQL 語句任一行上，直接按下 **`Cmd + Enter`**（macOS）或 **`Ctrl + Enter`**（Windows/Linux）。
  - DataGrip 會自動辨識整段 SQL 邊界並執行，**完全不需要滑鼠反白選取整段語句**。
- **選取執行**：若滑鼠選取了特定程式碼區塊再按 `Cmd + Enter`，則只執行選取的部分。
- **多語句批次執行**：按 `Cmd + Shift + Enter` 或在彈出選單選擇「Execute All Statements」。
- **交易控制模式（Transaction Mode）**：
  - 工具列右上角可切換 **Tx: Auto**（自動提交）或 **Tx: Manual**（手動提交）。
  - 在 Manual 模式下執行 `UPDATE` / `DELETE` 後，可手動點擊工具列的 **Commit** 或 **Rollback**。

### 2. Result Grid（資料表格）編輯與提交

執行 `SELECT` 查詢後，下方會展示強大的 Result Grid 面板：

- **單元格直接編輯**：雙擊欄位可直接修改內容。
- **增刪資料列**：
  - 點擊表格工具列的 **`+`**（Add Row）新增一行。
  - 選取資料列後點擊 **`-`**（Delete Row）標記刪除。
- **變更暫存與提交（Submit / Revert）**：
  - 所有修改在介面上會先以顏色醒目標記（藍色新增、綠色修改、淡灰刪除），此時尚未寫入 MySQL。
  - 確認修改無誤後，點擊上方工具列的 **Submit**（向上箭頭圖示，或按 `Cmd + Enter`）正式寫入資料庫。
  - 若想取消暫存變更，點擊 **Revert**（撤銷圖示）即可復原。

### 3. 一鍵匯出為前端 Mock 資料（Data Extractor）

在查詢結果表格右上角有一個 **Extractor** 下拉選單，可一鍵轉換資料格式：

- **JSON**：直接複製為標準 JSON 陣列格式（前端建立 Mock API 或測試資料極為便利）。
- **Markdown Table**：直接匯出為 Markdown 表格語法，適合貼入筆記或 PR 說明文件。
- **CSV / TSV**：匯出為試算表格式。
- **SQL INSERT**：將表格資料整批產生為 `INSERT INTO ...` 語法，方便建立 Seed Data。

### 4. 資料表結構導航與 DDL 預覽

- **快速查看 DDL**：在左側樹狀結構或 SQL 語法中的 Table 名稱上按下 **`Cmd + B`**（Go to DDL），可立即跳轉至該資料表的完整 `CREATE TABLE` 定義。
- **視覺化資料表修改（Modify Table）**：
  - 對資料表按右鍵選擇 **Modify Table...**（快速鍵 `Cmd + F6`）。
  - 在 GUI 介面新增欄位、調整型別、勾選 `Auto Increment` 或設定索引與外鍵。
  - 介面下方會即時產生對應的 `ALTER TABLE` 語法預覽，點擊 **Execute** 即可套用。

### 5. 一鍵生成資料庫關聯圖（ER Diagram）

1. 在 Database Explorer 選取 `practice` 資料庫或多張資料表。
2. 按下快速鍵 **`Cmd + Alt + U`**（macOS）或右鍵選擇 **Diagrams** -> **Show Visualization...**。
3. DataGrip 會自動繪製完整的實體關聯圖（ER Diagram），直觀呈現資料表之間的主外鍵關聯。

---

## 常用開發快速鍵速查表（macOS）

| 操作功能 | 快速鍵（macOS） | 說明 |
| :--- | :--- | :--- |
| **執行當前 SQL 語句** | `Cmd + Enter` | 游標停在該語句即可，自動辨識邊界 |
| **開新 Query Console** | `F4` 或 `Cmd + Shift + F10` | 針對當前選取的 Database 開啟控制台 |
| **開啟 / 隱藏 Database 面板** | `Cmd + 1` | 快速切換左側導覽列 |
| **跳轉至 Table DDL 定義** | `Cmd + B` | 在 SQL 編輯區的資料表名稱上按快捷鍵 |
| **格式化 SQL 程式碼** | `Cmd + Alt + L` | 依據標準規範美化 SQL 縮排與排版 |
| **視覺化修改資料表** | `Cmd + F6` | 開啟 Modify Table 視窗 |
| **生成 ER 關聯圖** | `Cmd + Alt + U` | 繪製資料庫關聯視覺圖 |
| **提交 Result Grid 修改** | `Cmd + Enter`（在表格區） | 將介面上的暫存修改寫入資料庫 |
| **重新載入 Schema（Introspect）** | `Cmd + Shift + F5` | 當後端 Migration 新增 Table 後同步結構 |

---

## 常見問題排查

### 1. 連線失敗：`Connection refused` 或 `Communications link failure`

- **原因**：Docker 容器尚未啟動，或 Docker Desktop 尚未開機。
- **排查步驟**：
  1. 確認 Docker Desktop 正在運行。
  2. 在終端機進入專案目錄執行 `docker compose ps`，確認容器狀態為 `healthy`。
  3. 檢查 Mac 本機 `3306` 埠是否被其他本機 MySQL 或服務佔用（執行 `lsof -i :3306` 檢查）。

### 2. 帳號驗證失敗：`Access denied for user 'steve'@'...'`

- **原因**：密碼輸入錯誤，或使用的帳號尚未在容器建立時初始化。
- **排查步驟**：
  1. 檢查專案目錄下的 `.env` 檔案確認 `MYSQL_USER` 與 `MYSQL_PASSWORD`。
  2. 若剛修改了 `.env`，注意 Named Volume（`mysql_data`）可能保留了舊密碼，需要執行 `docker compose down -v` 重新初始化資料庫（此操作會清空現有資料。

### 3. 左側樹狀圖看不到新建立的資料庫或資料表

- **原因**：DataGrip 快取未更新，或 Schemas 過濾條件未勾選。
- **排查步驟**：
  1. 在資料庫節點上點擊右鍵 -> **Refresh**（或按 `Cmd + Shift + F5`）。
  2. 右鍵點選 Data Source -> **Properties...** -> 切換至 **Schemas** 分頁確認目標 Database 是否已被勾選。
