# 使用 Docker Compose 建置 MySQL 8.4 LTS 本機開發環境

在 Mac 上透過 Docker Desktop 與 Docker Compose 建置 MySQL 8.4 LTS 開發環境。包含版本選型、`compose.yaml` 與 `.env`
設定、Named Volume 資料持久化、Healthcheck 健康檢查與常用管理指令。

---

## 為什麼選 MySQL 8.4 LTS 與 Docker Compose

### 1. 版本選型

- **MySQL 8.0 已於 2026 年 4 月 EOL**：官方不再提供安全更新，新環境不應再基於 8.0 建立。
- **不使用 `image: mysql:latest`**：`latest` 為浮動標籤，遇到大版本升級時會自動拉取不相容映像檔，容易損壞既有環境。
- **固定在 `image: mysql:8.4` (LTS)**：固定在長期支援版，環境穩定，同時能持續取得 8.4 系列的修補程式。

### 2. 環境架構

- **不安裝本機 MySQL Server**：避免常駐背景吃資源、Port 衝突、解除安裝殘留以及多版本切換問題。
- **不使用單行 `docker run` 指令**：參數難以版控且容易遺漏。
- **使用 Docker
  Compose**：專案通常同時包含後端（Backend）、快取（Redis）與資料庫（MySQL）。Compose 能把服務、網路與資料卷以檔案集中管理，隨時一鍵建立或銷毀。

---

## 核心名詞

- **Mac 本機（Host）**：執行 Docker Desktop 的實體作業系統。
- **Docker 容器（Container）**：隔離的 Linux 執行環境，MySQL Server 在其中執行。
- **具名資料卷（Named Volume，`mysql_data`）**：Docker 在本機硬碟管理的獨立儲存區。執行 `docker compose down`
  刪除容器時，資料庫資料仍完整保留。
- **連接埠映射（Port Mapping，`3306:3306`）**：將 Mac 本機的 3306 埠轉發到容器內的 3306 埠。
- **容器狀態差異**：
  - `Running`：容器已啟動，但 MySQL 內部可能仍在初始化或載入資料。
  - `Healthy`：Healthcheck 探測（`mysqladmin ping`）成功，代表 MySQL 已可正常連線。

---

## 專案結構與設定檔

建立目錄與設定檔：

```text
mysql-learning/
├── compose.yaml
├── .env
└── .env.example
```

> **注意**：`.env` 包含帳號密碼，需加入 `.gitignore` 避免進 Git；可提供 `.env.example` 作為範本。

### 1. 環境變數檔：`.env`

```env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=practice
MYSQL_USER=steve
MYSQL_PASSWORD=password
```

- `MYSQL_ROOT_PASSWORD`：最高管理者 `root` 的密碼。
- `MYSQL_DATABASE`：容器首次建立時自動初始化的資料庫名稱。
- `MYSQL_USER`：日常開發使用的一般帳號。
- `MYSQL_PASSWORD`：日常開發帳號的密碼。

### 2. 服務設定檔：`compose.yaml`

使用 Compose Specification 規範，檔名為 `compose.yaml`，不需寫 `version:`：

```yaml
services:
  mysql:
    image: mysql:8.4
    container_name: mysql-learning

    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

    ports:
      - "3306:3306"

    volumes:
      - mysql_data:/var/lib/mysql

    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

    restart: unless-stopped

volumes:
  mysql_data:
```

- `services.mysql`：定義 MySQL 服務。
- `image: mysql:8.4`：使用官方 MySQL 8.4 LTS 映像檔。
- `container_name: mysql-learning`：指定容器名稱。
- `environment`：讀取 `.env` 變數作為初始化參數。
- `ports: ["3306:3306"]`：將 Mac 本機 3306 埠映射至容器內 3306 埠。
- `volumes: [mysql_data:/var/lib/mysql]`：將資料卷 `mysql_data` 掛載至 MySQL 預設資料目錄 `/var/lib/mysql`。
- `healthcheck`：每 10 秒執行 `mysqladmin ping`；5 秒內回應成功即標記為 `healthy`。
- `restart: unless-stopped`：除非手動停止，否則 Docker 重啟時自動復原容器。
- `volumes.mysql_data`：宣告具名資料卷。

---

## 常用指令

進入 `mysql-learning` 目錄執行：

```bash
cd mysql-learning
```

### 1. 服務管理

| 目的                 | 指令                           | 說明                                            |
| :------------------- | :----------------------------- | :---------------------------------------------- |
| **啟動服務**         | `docker compose up -d`         | 背景啟動容器並執行健康檢查                      |
| **查看狀態**         | `docker compose ps`            | 查看容器狀態與健康度（`healthy` / `starting`）  |
| **查看日誌**         | `docker compose logs -f mysql` | 即時監看輸出（按 `Ctrl+C` 離開）                |
| **重新啟動**         | `docker compose restart mysql` | 重啟 MySQL 容器                                 |
| **停止並刪除容器**   | `docker compose down`          | 移除容器與網路，**保留 Named Volume 資料**      |
| **清空資料重新開始** | `docker compose down -v`       | 移除容器並**刪除 Named Volume**（資料全部清除） |

#### 常用參數拆解與記憶法

- `-d`（`--detach`，背景分離模式）：
  - **意思**：讓容器在背景獨立執行，把終端機（Terminal）的控制權立即釋放出來。
  - **如果沒加**：終端機會停留在容器前台印日誌；若按 `Ctrl+C` 就會直接停止容器。
- `-f`（`--follow`，持續追蹤）：
  - **意思**：持續監聽並即時輸出最新的日誌（類似 Linux 的 `tail -f`）。
  - **操作技巧**：按 `Ctrl+C` 只會離開監看畫面，**不會**停止容器運行。
- `-v`（`--volumes`，刪除資料卷）：
  - **意思**：在執行 `down` 移除容器時，連同 `compose.yaml` 定義的具名資料卷（Named Volume，如 `mysql_data`）一併刪除。
  - **核心差異**：
    - `docker compose down`：刪除容器與網路，**保留資料卷**（下次啟動時資料庫內容仍在）。
    - `docker compose down -v`：刪除容器、網路並**徹底清空資料庫硬碟資料**（完全重置環境時使用）。
- 指令結尾的 `mysql`（指定服務）：
  - **意思**：指定操作 `compose.yaml` 裡名為 `mysql` 的服務（`services.mysql`）。
  - **如果省略**：例如 `docker compose logs -f`，會同時顯示 Compose 專案內所有服務的日誌。

### 2. 進入 MySQL 指令列

使用一般帳號（`steve`）連線：

```bash
docker compose exec mysql mysql -u steve -p
```

_提示密碼時輸入 `.env` 設定的值（如 `password`）。_

使用最高管理員（`root`）連線：

```bash
docker compose exec mysql mysql -u root -p
```

_提示密碼時輸入 `root`。_

#### 連線指令參數拆解（為什麼有兩個 mysql？）

以 `docker compose exec mysql mysql -u steve -p` 為例：

- `exec`（Execute）：在**已經處於 Running 狀態**的容器內部執行程式。
- 第一個 `mysql`（目標服務）：告知 Docker Compose 要進入哪一個容器（對應 `compose.yaml` 裡的 `services.mysql`）。
- 第二個 `mysql`（容器內程式）：在容器內啟動 MySQL CLI 用戶端指令（`/usr/bin/mysql`）。
- `-u steve`（`--user`，使用者）：指定登入 MySQL 的使用者帳號。
- `-p`（`--password`，密碼提示）：通知系統在按下 Enter 後以隱藏字元提示輸入密碼（Prompt for password），避免明文密碼留在終端機歷史紀錄中。

連線後即可執行 SQL：

```sql
SHOW DATABASES;

USE practice;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

INSERT INTO users (name) VALUES ('Steve');

SELECT * FROM users;
```

---

## GUI 連線設定

DataGrip、DBeaver、MySQL Workbench 連線參數：

- **連線類型**：MySQL
- **Host**：`localhost` 或 `127.0.0.1`
- **Port**：`3306`
- **Database**：`practice`
- **User**：`steve`（或管理者 `root`）
- **Password**：`password`（或 root 密碼 `root`）

---

## 注意事項

1. **先決條件**：
   - 執行前須啟動 Docker Desktop。
   - Mac 本機的 `3306` 埠不能被其他 MySQL 服務佔用。
2. **適用範圍**：
   - 此設定供本機開發與學習使用。
   - 正式營運環境（Production）建議使用雲端託管服務（如 AWS RDS、GCP Cloud SQL）搭配備份與 VPC 網路隔離。
