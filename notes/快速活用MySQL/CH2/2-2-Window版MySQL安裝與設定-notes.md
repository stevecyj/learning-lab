# Windows 版 MySQL 安裝與設定

## 這堂課在講什麼

說明在 Windows 作業系統下載、安裝與設定 MySQL Community Server（社群版）的完整步驟。內容涵蓋下載完整離線安裝包、安裝 Visual C++ 必要相依套件、保留預設 Port 3306 與驗證模式、設定 root 密碼並新增日常管理用的 dba 帳號（包含 Host 權限差異），以及完成 Windows 服務註冊與結束安裝的注意事項。

## 學完要會什麼

1. 在 MySQL 官方網站選取並下載 Windows 完整的離線安裝包（MySQL Installer）。
2. 理解安裝必要相依套件（Microsoft Visual C++ Redistributable）的原因，並完成安裝。
3. 熟悉安裝類型（Developer Default）與連線通訊埠（Port 3306）的設定。
4. 設定最高權限 `root` 密碼，並建立日常管理用的 `DB Admin`（如 dba）帳號，理解 `%` 與 `localhost` 的連線限制差異。
5. 完成 MySQL 註冊為 Windows 服務的設定流程與啟動選項控制。

## 重點整理

### 1. 下載版本選擇：社群版（Community Server）與完整安裝包
- **社群版（MySQL Community Server）**：開源且免費，可自由查看原始碼，適合學習與本機開發測試。
- **安裝包類型**：
  - 官網提供約 2.5 MB 的 Web 安裝檔與約 405.2 MB 的完整安裝包。
  - 建議下載約 405.2 MB 的完整離線安裝包，後續安裝時即使沒有網路也能順利完成。
  - 完整安裝包內已包含圖形化管理工具 MySQL Workbench，安裝後不需另外個別下載。
- **略過 Oracle 登入**：點擊下載後若跳出 Oracle 帳號註冊或登入提示，點選「No thanks, just start my download.」即可直接下載。

### 2. 必要相依套件（Prerequisites）與安裝類型
- **安裝類型（Setup Type）**：本機學習與測試用途選擇預設的 `Developer Default`。
- **檢查必要套件（Check Requirements）**：
  - 進入此畫面時，必須先點擊 **Execute** 執行安裝，不可直接按 Next（若直接按 Next 會略過相依套件，導致 Workbench 等工具後續無法安裝）。
  - **Microsoft Visual C++ Redistributable Package**：MySQL Workbench 圖形介面是使用 C++ 開發，因此必須安裝此套件才能運作。若系統先前已安裝過，此清單可能不會跳出。
  - 安裝完必要套件後按 Next，若系統提示仍有部分非必要套件未滿足，點擊 Yes 略過即可。

### 3. 核心組態與帳號權限設定
- **通訊埠（Port Number）**：TCP/IP 預設通訊埠為 `3306`，日後工具連線資料庫皆需指定此 Port。
- **驗證方式（Authentication Method）**：採用預設建議的強密碼加密驗證（Use Strong Password Encryption for Authentication）。
- **最高管理者帳號（root）**：
  - `root` 為 MySQL 最高管理權限帳號，名稱無法自訂或更改。
  - 設定的密碼必須妥善記住；若遺忘密碼需重新安裝或進入安全模式才能重設。
- **新增日常管理帳號（dba）**：
  - 長期使用 root 容易增加密碼外洩的安全風險，建議另建一組管理帳號供日常使用。
  - 點擊 **Add User**，輸入帳號名稱（如 `dba`），Role 選擇 `DB Admin` 並設定密碼。
  - **連線主機（Host）設定差異**：
    - `%`（預設值）：允許從任何遠端主機連線，只要帳號密碼正確即可登入。
    - `localhost`：限制只能從安裝 MySQL 的本機實體電腦登入管理，不允許任何遠端連線。

### 4. 服務註冊與完成設定
- **Windows 服務（Windows Service）**：安裝程式會將 MySQL 註冊為 Windows 系統服務，服務名稱保持預設即可，可透過 Windows 服務管理員或 MySQL 管理介面啟動。
- **連線測試（Connect To Server）**：在後續子設定畫面中輸入 root 密碼並點擊 **Check**，確認連線成功（顯示打勾）後按 Next。
- **結束安裝選項**：最後步驟預設會勾選自動啟動 MySQL Workbench 與命令提示字元（MySQL Shell），教學建議取消勾選，待需要時再手動由選單開啟。

## 範例與操作

### 完整安裝與設定步驟流程

1. **官網下載**
   - 瀏覽器搜尋 `download mysql community server`，點選官方第一個連結。
   - 作業系統選擇 `Microsoft Windows`，點擊 `MySQL Installer for Windows` 下方的「Go to Download Page」。
   - 選擇約 405.2 MB 的安裝檔，點擊 `Download`。
   - 點擊 `No thanks, just start my download.` 下載並儲存安裝檔。

2. **執行安裝與安裝必要套件**
   - 雙擊執行安裝檔，Setup Type 選擇 `Developer Default`，按 Next。
   - 在 Check Requirements 畫面點擊 **Execute**，彈出 Visual C++ 安裝畫面時勾選同意並點擊安裝。
   - 安裝完成後關閉視窗，按 Next（若有未裝的次要元件提示可按 Yes 略過）。
   - 在 Installation 畫面點擊 **Execute** 安裝 MySQL Server、Workbench 等工具，待全部狀態顯示 Complete 後按 Next。

3. **產品設定（Product Configuration）**
   - **Type and Networking**：確認 TCP/IP Port 為 `3306`，按 Next。
   - **Authentication Method**：選擇預設的強密碼驗證，按 Next。
   - **Accounts and Roles**：
     - 設定並確認 `root` 密碼。
     - 點擊 **Add User**，輸入 Username（如 `dba`）、設定 Host（`%` 允許遠端，`localhost` 僅限本機）、選擇 Role 為 `DB Admin` 並輸入密碼，點擊 OK。
     - 確認帳號清單後按 Next。
   - **Windows Service**：保持預設服務名稱，按 Next。
   - **Apply Configuration**：點擊 **Execute** 套用設定，完成後按 Finish。

4. **連線檢查與結束**
   - 進入後續子設定頁面，在 Connect To Server 頁面輸入 root 密碼，點擊 **Check** 驗證。
   - 驗證成功後按 Next，再點擊 **Execute** 套用，完成後按 Finish。
   - 在最後的完成畫面中，取消勾選「Start MySQL Workbench after Setup」與「Start MySQL Shell after Setup」。
   - 點擊 **Finish** 完成所有安裝與設定。

## 常見誤解／注意事項

- **不要直接跳過 Check Requirements**：在此頁面務必先點擊 **Execute** 安裝 Visual C++ 等相依套件。若直接按 Next，會導致圖形介面工具（MySQL Workbench）因缺少執行環境而無法安裝或運作。
- **Web 安裝檔與離線安裝檔差異**：2.5 MB 的 Web 安裝檔在執行時才從網路下載套件；405.2 MB 的完整安裝檔已內含所有套件，即使離線也能順利安裝。
- **不需強制註冊 Oracle 帳號**：下載時出現註冊/登入提示，直接點選下方「No thanks, just start my download.」即可開始下載。
- **root 密碼遺忘處理成本高**：`root` 帳號名稱無法修改且具備最高權限，若忘記密碼須透過安全模式重設或重新安裝。
- **避免日常常態使用 root 登入**：建立具備 `DB Admin` 權限的專用帳號（如 dba），可在滿足管理需求的同時降低最高權限帳號密碼外洩的風險。

## 重點速記

在 Windows 安裝 MySQL Community Server 時，選擇 405 MB 完整離線安裝包並優先執行 Visual C++ 相依套件安裝，妥善設定 root 密碼與專用 dba 帳號即可完成資料庫與 Workbench 的建置。
