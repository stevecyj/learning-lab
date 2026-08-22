"""
用 urllib.request 抓一個網頁，印出狀態碼、編碼與前 500 個字元。

執行方式（在專案根目錄）：
    uv run "notes/python爬蟲/01_urllib_request.py"
"""

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# 目標網址。這個站專門用來練習 HTTP 請求，會把你送出的內容原封不動回傳。
URL = "https://httpbin.org/html"

# 很多網站會擋掉沒有 User-Agent 的請求，urllib 預設會送 "Python-urllib/3.x"。
# 這裡改成瀏覽器的樣子，降低被擋的機率。
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def main() -> None:
    # Request 物件把「網址 + 標頭」包在一起，urlopen 才能帶著標頭去請求。
    req = Request(URL, headers=HEADERS)

    try:
        # with 會在區塊結束時自動關閉連線，等同 JS 裡手動 abort/釋放資源。
        with urlopen(req, timeout=10) as resp:
            status = resp.status          # HTTP 狀態碼，例如 200
            charset = resp.headers.get_content_charset() or "utf-8"
            raw = resp.read()             # bytes，還不是字串
            html = raw.decode(charset)    # 用回應宣告的編碼轉成 str

        print(f"狀態碼：{status}")
        print(f"編碼：{charset}")
        print(f"長度：{len(html)} 字元")
        print("-" * 40)
        print(html[:500])

    except HTTPError as e:
        # 伺服器有回應，但是 4xx / 5xx
        print(f"HTTP 錯誤 {e.code}：{e.reason}")
    except URLError as e:
        # 連不上（DNS 失敗、超時、沒網路）
        print(f"連線失敗：{e.reason}")


if __name__ == "__main__":
    main()
