# Docker 後端多服務架構與無中斷切換

說明後端多服務（Web 伺服器、應用程式、Redis、MySQL）在 Docker 容器中的拆分原則、`compose.yaml` 編排方式，以及無中斷切換（藍綠部署與資料庫備援）的架構設計。

---

## 服務拆分原則：一個 Container 只跑一個主要行程

業界標準是**每個服務獨立一個 Container**：

- **Web 伺服器 / 反向代理（Nginx / Apache）**：獨立 Container
- **應用程式後端（Python / Node.js / Java）**：獨立 Container
- **快取（Redis）**：獨立 Container
- **資料庫（MySQL）**：獨立 Container

```text
               【實體電腦 / 伺服器 Host】
                           │
       ┌───────────────────┴───────────────────┐
       │             Docker 內部網路            │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Container 1 │    │  Container 2 │    │  Container 3 │
│ (Web Server) │ ── │   (Backend)  │ ── │   (MySQL)    │
│  Port: 80    │    │  Port: 8000  │    │  Port: 3306  │
└──────────────┘    └──────────────┘    └──────────────┘
```

### 拆分原因

1. **容器生命週期**：Docker 容器存活取決於主行程（PID 1）。多個程式塞在同一個容器時，若其中一個程式異常終止，Docker 無法正確管理與重啟單一服務。
2. **獨立擴展（Scale）**：流量增加時，通常只需增加後端運算實例（例如後端擴展至 3 個 Container），資料庫不需隨之倍增。
3. **獨立升級**：更新後端程式只需重啟後端 Container，MySQL 與 Redis 保持連線不中斷。

---

## 多服務編排：使用單一 `compose.yaml`

專案通常透過**一個 `compose.yaml`** 定義與協調整體系統。Docker Compose 會為所有服務建立專屬的內部虛擬網路，Container 之間可直接透過服務名稱通訊。

### 多服務配置範例（Nginx + Backend + Redis + MySQL）

```yaml
services:
  # 1. 流量入口：反向代理 / Web 伺服器
  web:
    image: nginx:alpine
    container_name: app-web
    ports:
      - "80:80"
    depends_on:
      - backend

  # 2. 業務邏輯：後端應用程式
  backend:
    image: my-backend-app:1.0
    container_name: app-backend
    environment:
      - DATABASE_HOST=mysql      # 使用下方 mysql 服務名稱
      - REDIS_HOST=redis         # 使用下方 redis 服務名稱
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_started

  # 3. 快取服務
  redis:
    image: redis:7-alpine
    container_name: app-redis

  # 4. 資料儲存：MySQL 8.4 LTS
  mysql:
    image: mysql:8.4
    container_name: app-mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: practice
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mysql_data:
```

---

## 無中斷切換架構設計

### 1. 無狀態服務（後端 Server）的藍綠部署

後端伺服器本身不儲存持久化資料（Stateless），透過前端反向代理（如 Nginx）可達成零停機切換：

```text
                        【外部請求】
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Nginx (反向代理入口)   │
                 └───────────┬───────────┘
                             │ (轉發流量)
              ┌──────────────┴──────────────┐
              ▼                             ▼
       ┌──────────────┐              ┌──────────────┐
       │   Server A   │              │   Server B   │
       │ (目前版本)    │              │ (新版待命)   │
       └──────────────┘              └──────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                     ┌──────────────┐
                     │ MySQL 資料庫 │
                     └──────────────┘
```

#### 切換流程

1. **常態運作**：Nginx 將所有流量導向 `Server A`，`Server A` 讀寫共用的 `MySQL`。
2. **部署新版**：啟動新版容器 `Server B`，等待其通過健康檢查。
3. **切換流量**：執行 `nginx -s reload` 重新載入設定，將流量瞬間轉向 `Server B`（毫秒級切換，連線不中斷）。
4. **關閉舊版**：`Server A` 處理完現有請求後平順關閉（Graceful Shutdown）。

---

### 2. 有狀態服務（資料庫）的備份與備援

資料庫涉及實體資料寫入（Stateful），不能直接透過 Nginx 流量切換，需採用專用備份或複製機制：

1. **線上熱備份（Hot Backup）**：
   - 透過臨時容器執行 `mysqldump` 或備份工具，將資料直接輸出至掛載磁碟，MySQL 服務全程不中斷。
2. **主從備援（Master / Replica 架構）**：
   - **Primary（主庫 A）**：處理所有寫入操作（`INSERT` / `UPDATE` / `DELETE`）。
   - **Replica（從庫 B）**：即時同步主庫資料，分擔查詢操作（`SELECT`）。
   - **故障轉移（Failover）**：當主庫維護或異常時，將從庫 B 晉升為主庫並轉移連線。

---

## 服務角色對照

| 角色 | 職責 | 常見技術 |
| :--- | :--- | :--- |
| **Web 伺服器 / 反向代理** | 接收外部請求、處理 SSL、靜態檔案分發與流量轉發 | Nginx, Apache, Traefik |
| **Application Server** | 執行業務邏輯與運算，與資料庫連線交換資料 | Python (FastAPI/Django), Node.js, Spring Boot |
| **Cache Server** | 於記憶體儲存高頻讀取的暫存資料，降低資料庫負擔 | Redis, Memcached |
| **Database Server** | 持久化儲存結構化資料，保證交易完整性（ACID） | MySQL, PostgreSQL |
