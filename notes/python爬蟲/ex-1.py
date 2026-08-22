from urllib import request

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
print(soup)
print(soup.title)
