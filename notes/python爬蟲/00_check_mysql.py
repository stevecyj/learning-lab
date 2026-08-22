"""
環境自我檢查：確認 mysqlclient(MySQLdb) 能匯入，並且真的連上 Docker 裡的 MySQL。

執行方式（在專案根目錄）：
    uv run "notes/python爬蟲/00_check_mysql.py"

連線設定來自 mysql-learning/.env，若該檔不存在則用下方預設值。
"""

import os
import sys
from pathlib import Path

# --- 1. 找出專案根目錄 ---------------------------------------------------
# __file__ 是這支腳本自己的路徑。
# .resolve() 轉成絕對路徑，.parents[2] 往上跳兩層：
#   parents[0] = notes/python爬蟲
#   parents[1] = notes
#   parents[2] = 專案根目錄
# 用這個方式算路徑，不管你從哪個目錄執行腳本都會指到同一個地方。
ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / "mysql-learning" / ".env"

# --- 2. 讀 .env，組出連線參數 --------------------------------------------
# 預設值：對應 mysql-learning/compose.yaml 的設定。
config = {
    "MYSQL_ROOT_PASSWORD": "root",
    "MYSQL_DATABASE": "practice",
    "MYSQL_USER": "steve",
    "MYSQL_PASSWORD": "password",
}

if ENV_FILE.exists():
    # .env 每行長這樣：KEY=VALUE
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        # 跳過空行與註解行
        if not line or line.startswith("#") or "=" not in line:
            continue
        # split("=", 1) 只切第一個等號，密碼裡若含 "=" 才不會被切壞
        key, value = line.split("=", 1)
        config[key.strip()] = value.strip()
    print(f"[讀取設定] {ENV_FILE}")
else:
    print(f"[讀取設定] 找不到 {ENV_FILE}，使用預設值")

HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
PORT = int(os.environ.get("MYSQL_PORT", "3306"))
USER = "root"                              # 用 root 才看得到全部資料庫
PASSWORD = config["MYSQL_ROOT_PASSWORD"]
DATABASE = config["MYSQL_DATABASE"]


def step(n: int, title: str) -> None:
    print(f"\n--- {n}. {title} ---")


# --- 3. 檢查能不能匯入 MySQLdb -------------------------------------------
step(1, "匯入 MySQLdb")
try:
    import MySQLdb
except ModuleNotFoundError:
    # 這是最常見的失敗：pyproject.toml 有寫 mysqlclient，但沒裝進 .venv，
    # 或是編譯失敗（缺 MySQL 的 C 開發檔）。
    print("✗ 匯入失敗：沒有 MySQLdb 模組")
    print("  修法：")
    print("    brew install mysql-client")
    print('    export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"')
    print("    uv sync")
    sys.exit(1)

# version_info 是一個 tuple，例如 (2, 2, 8, 'final', 0)
print(f"✓ MySQLdb {MySQLdb.version_info}")
print(f"  底層 C client 版本：{MySQLdb.get_client_info()}")


# --- 4. 連線 -------------------------------------------------------------
step(2, f"連線 {USER}@{HOST}:{PORT}")
try:
    # connect() 的四個常用參數：主機、帳號、密碼、預設資料庫。
    # connect_timeout 避免伺服器沒開時卡住不動。
    db = MySQLdb.connect(
        host=HOST,
        user=USER,
        passwd=PASSWORD,
        db=DATABASE,
        port=PORT,
        charset="utf8mb4",
        connect_timeout=5,
    )
except MySQLdb.OperationalError as e:
    # OperationalError 涵蓋「連不上」與「帳密錯」兩種情況，用錯誤碼區分。
    # e.args 是 (錯誤碼, 錯誤訊息)
    code = e.args[0] if e.args else "?"
    print(f"✗ 連線失敗（錯誤碼 {code}）：{e}")
    if code == 2003:
        print("  → 連不到 3306。檢查容器是否啟動：")
        print("     docker compose -f mysql-learning/compose.yaml up -d")
    elif code == 1045:
        print("  → 帳號或密碼錯誤。核對 mysql-learning/.env 的 MYSQL_ROOT_PASSWORD")
    elif code == 1049:
        print(f"  → 資料庫 {DATABASE} 不存在")
    sys.exit(1)

print("✓ 連線成功")


# --- 5. 實際下查詢 -------------------------------------------------------
# cursor 是「執行 SQL 並取回結果」的把手。一個連線可以開多個 cursor。
cur = db.cursor()

step(3, "伺服器資訊")
cur.execute("SELECT VERSION(), DATABASE(), CURRENT_USER()")
# fetchone() 取一列，回傳 tuple；欄位順序對應 SELECT 的順序。
version, current_db, current_user = cur.fetchone()
print(f"  MySQL 版本：{version}")
print(f"  目前資料庫：{current_db}")
print(f"  目前使用者：{current_user}")

step(4, "資料庫清單")
cur.execute("SHOW DATABASES")
# fetchall() 取全部列，回傳 tuple of tuples，例如 (('practice',), ('sakila',))
# row[0] 取每一列的第一個欄位
databases = [row[0] for row in cur.fetchall()]
for name in databases:
    print(f"  - {name}")

step(5, f"{DATABASE} 的資料表")
cur.execute("SHOW TABLES")
tables = [row[0] for row in cur.fetchall()]
if tables:
    for name in tables:
        # %s 在 MySQLdb 裡是「值」的佔位符，不能用來代入表名，
        # 所以表名這裡直接字串串接（來源是 SHOW TABLES，非使用者輸入）。
        cur.execute(f"SELECT COUNT(*) FROM `{name}`")
        count = cur.fetchone()[0]
        print(f"  - {name}（{count} 列）")
else:
    print(f"  （{DATABASE} 目前沒有任何資料表）")

# --- 6. 收尾 -------------------------------------------------------------
# 先關 cursor 再關連線。沒關也不會壞，但養成習慣比較好。
cur.close()
db.close()

print("\n環境檢查全部通過。")
