"""
用 requests 抓網頁與 API，對照 01_urllib_request.py 看差別。

執行方式（在專案根目錄）：
    uv run "notes/python爬蟲/02_requests_basic.py"
"""

import requests

# 目標網址。httpbin.org 是專門用來練習 HTTP 的測試站。
HTML_URL = "https://httpbin.org/html"       # 回傳一段 HTML
JSON_URL = "https://httpbin.org/get"        # 回傳 JSON，內容是你送出的請求資訊

# 有些網站會擋掉沒有 User-Agent 的請求，requests 預設會送 "python-requests/2.x"。
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def fetch_html() -> None:
    """抓 HTML：對照 01_ 的 urllib 版本，requests 少了 Request 物件與手動 decode。"""
    # requests.get 直接回傳 Response 物件，不需要 with，也不需要自己組 Request。
    resp = requests.get(HTML_URL, headers=HEADERS, timeout=10)

    # raise_for_status()：狀態碼是 4xx／5xx 就丟出 HTTPError，否則回傳 None。
    # urllib 是「非 2xx 自動丟例外」，requests 則要自己呼叫這行才會丟。
    resp.raise_for_status()

    print(f"狀態碼：{resp.status_code}")
    print(f"編碼：{resp.encoding}")        # requests 從 headers 猜出來的編碼
    print(f"長度：{len(resp.text)} 字元")   # resp.text 已經是 str，自動 decode 過
    print("-" * 40)
    print(resp.text[:500])


def fetch_json() -> None:
    """抓 JSON：帶查詢參數，並把回應直接轉成 dict。"""
    # params 是查詢字串，requests 會幫你組成 ?keyword=python&page=2 並做 URL 編碼。
    params = {"keyword": "python", "page": 2}

    resp = requests.get(JSON_URL, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()

    print(f"實際請求網址：{resp.url}")

    # resp.json() 把回應內容當 JSON 解析成 Python 物件（這裡是 dict）。
    # 等同 JS 的 await res.json()。
    data = resp.json()

    # httpbin 的 /get 會把收到的查詢參數放在 "args" 這個 key 底下。
    print(f"伺服器收到的參數：{data['args']}")
    print(f"伺服器看到的 User-Agent：{data['headers']['User-Agent']}")


def main() -> None:
    try:
        fetch_html()
        print("=" * 40)
        fetch_json()

    except requests.HTTPError as e:
        # 伺服器有回應，但狀態碼是 4xx／5xx（由 raise_for_status 丟出）
        print(f"HTTP 錯誤：{e}")
    except requests.Timeout:
        # 超過 timeout 秒還沒回應
        print("請求逾時")
    except requests.RequestException as e:
        # 所有 requests 例外的共同父類別：DNS 失敗、連線被拒、SSL 錯誤等
        print(f"請求失敗：{e}")


if __name__ == "__main__":
    main()
