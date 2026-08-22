"""
requests 負責「抓」，BeautifulSoup 負責「解析」，兩個搭配把網頁變成 Python 資料。

執行方式（在專案根目錄）：
    uv run "notes/python爬蟲/03_requests_bs4_parse.py"
"""

import requests
from bs4 import BeautifulSoup

# quotes.toscrape.com 是專門開放給人練習爬蟲的網站，結構固定不會亂改。
# 每一頁有 10 則名言，每則包含 引言、作者、標籤。
URL = "https://quotes.toscrape.com/"

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def fetch_html(url: str) -> str:
    """第一步：用 requests 把網頁抓下來，回傳 HTML 字串。"""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()   # 4xx／5xx 就丟 HTTPError
    return resp.text          # 已經解碼好的 str


def parse_quotes(html: str) -> list[dict]:
    """第二步：用 BeautifulSoup 把 HTML 字串解析成結構化的 list[dict]。"""

    # BeautifulSoup(要解析的字串, 用哪個解析器)
    # "html.parser" 是 Python 內建的，不用另外裝套件。
    # soup 物件代表整份文件，可以往下找任何標籤。
    soup = BeautifulSoup(html, "html.parser")

    # select() 用 CSS 選擇器找出「所有」符合的元素，回傳 list。
    # 等同 JS 的 document.querySelectorAll(".quote")。
    # 這個網站每則名言都包在 <div class="quote"> 裡面。
    quote_blocks = soup.select("div.quote")

    results = []

    # 對每一個 <div class="quote"> 區塊，抓出裡面的三份資料。
    for block in quote_blocks:
        # select_one() 只找第一個符合的，找不到回傳 None。
        # 等同 JS 的 querySelector()。注意搜尋範圍是 block 之內，不是整頁。
        text_tag = block.select_one("span.text")
        author_tag = block.select_one("small.author")

        # .get_text() 取出標籤內的純文字（去掉 HTML 標籤）。
        # strip=True 順便去掉頭尾空白與換行，等同 JS 的 el.textContent.trim()。
        text = text_tag.get_text(strip=True)
        author = author_tag.get_text(strip=True)

        # 標籤有好幾個，所以用 select() 拿 list，再用 list comprehension 逐個取文字。
        # 展開成完整寫法是：
        #     tags = []
        #     for t in block.select("div.tags a.tag"):
        #         tags.append(t.get_text(strip=True))
        tags = [t.get_text(strip=True) for t in block.select("div.tags a.tag")]

        results.append({"text": text, "author": author, "tags": tags})

    return results


def find_next_page(html: str) -> str | None:
    """示範抓「屬性值」：找出下一頁的連結網址，沒有下一頁就回傳 None。"""
    soup = BeautifulSoup(html, "html.parser")

    # 下一頁按鈕的結構是 <li class="next"><a href="/page/2/">Next</a></li>
    next_link = soup.select_one("li.next a")

    if next_link is None:
        return None

    # 標籤的屬性用 dict 的方式取：next_link["href"] 拿到 "/page/2/"。
    # 這是相對路徑，要自己接上網域才是完整網址。
    return URL.rstrip("/") + next_link["href"]


def main() -> None:
    try:
        html = fetch_html(URL)
        quotes = parse_quotes(html)

        print(f"這一頁共抓到 {len(quotes)} 則名言")
        print("=" * 50)

        # enumerate 同時給出索引與元素，start=1 讓編號從 1 開始。
        for i, q in enumerate(quotes[:3], start=1):
            print(f"{i}. {q['text']}")
            print(f"   —— {q['author']}")
            print(f"   標籤：{', '.join(q['tags'])}")
            print()

        next_url = find_next_page(html)
        print(f"下一頁網址：{next_url}")

    except requests.HTTPError as e:
        print(f"HTTP 錯誤：{e}")
    except requests.Timeout:
        print("請求逾時")
    except requests.RequestException as e:
        print(f"請求失敗：{e}")


if __name__ == "__main__":
    main()
