from pprint import pp, pprint
from urllib import request
from urllib.parse import urljoin

from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/joke/index.html"
# res = request.urlopen(url)

useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"
headers = {"User-Agent": useragent}
req = request.Request(url=url, headers=headers)
res = request.urlopen(req)

print("狀態碼：", res.status)

# 第二個參數 features 一定要給，不然 bs4 會自己猜，並印出警告。
# "lxml" 速度快、修爛 HTML 的能力也好，但要先 uv add lxml。
# 另一個選擇是內建的 "html.parser"，零依賴但慢一點。
# res 是 file-like 物件，bs4 會自己 read() 並判斷編碼，所以不用先 decode。
soup = BeautifulSoup(res, "lxml")
action_bar = soup.find_all("div", {"id": "action-bar-container"})
tmp_div = action_bar[0].find("div")
tmp_a = action_bar[0].find("a")
assert tmp_a is not None

tmp_text_in_a = tmp_a.text
tmp_url = tmp_a["href"]
full_url = urljoin(res.url, tmp_url)

# print(dir(tmp_a))
print(full_url)
