# 3-2 Python 敘述、指定與縮排

## 核心內容

### 這一節真正要學會什麼

完成這一節後，我應該能夠：

1. 用換行與縮排寫出結構正確的 Python 程式。
2. 理解 `=` 會先計算右側運算式，再把結果指定給左側名稱。
3. 使用 `#` 撰寫註解，並分辨註解與字串。
4. 正確使用 `+`、`-`、`*`、`/`、`//`、`%` 與 `**`。
5. 在 Notebook 中先預測結果，再執行程式驗證。

---

### 一、敘述不一定剛好占一行

Python 程式通常以換行分隔敘述：

```python
a = 1
b = 2
print(a + b)
```

輸出：

```text
3
```

「每一行都是一個敘述」適合當作初步印象，但不完全精確：

- 一個敘述可以跨越多個實體行。
- 一行也可以用分號放入多個簡單敘述，但可讀性較差，不建議日常使用。
- `if`、`for`、`def` 等複合敘述會包含縮排的程式區塊。

長運算式優先放在成對括號內自然換行：

```python
total = (
    10
    + 20
    + 30
)
```

反斜線 `\` 也能明確續行：

```python
total = 10 + 20 + \
    30
```

不過反斜線後不能再放空白或註解，修改時也比較容易出錯。實務上優先使用 `()`、`[]` 或 `{}` 內的自然換行。

---

### 二、`=` 是指定，不是相等比較

```python
a = 1
b = 2
```

Python 會先計算 `=` 右側，再把結果綁定到左側名稱：

```python
total = a + b
```

這裡先取出 `a` 與 `b` 對應的值並完成加法，再讓 `total` 指向結果 `3`。

更精確的心智模型是：

> `=` 讓左側名稱綁定到右側運算結果。

它不保證「把值複製進一個盒子」。學到 list、dict 與其他可變物件時，同一個物件可以同時被多個名稱參照：

```python
items = [1, 2]
other_items = items
```

若要比較兩邊的值是否相等，使用 `==`：

```python
print(a == 1)  # True
print(a == b)  # False
```

指定方向不能任意顛倒：

```python
a = 1  # 合法
1 = a  # SyntaxError
```

---

### 三、註解使用 `#`

從 `#` 到該行結尾的文字是註解：

```python
# 計算訂單總額
order_total = 100 + 50
```

註解適合補充程式碼無法直接表達的原因、限制或決策。名稱清楚時，不必重述程式碼：

```python
# 不佳：把 100 加上 50
order_total = 100 + 50
```

三引號建立的是字串，不是 Python 的多行註解語法：

```python
message = """這是一個
跨越多行的字串"""
```

未指定給名稱的三引號字串有時看起來像註解，但 Python 仍會把它解析成字串運算式。模組、類別或函式開頭的三引號字串還會成為 docstring。要註解多行，應讓每行都以 `#` 開頭；編輯器通常有批次切換註解的快捷鍵。

---

### 四、縮排決定程式區塊

Python 使用縮排表示程式碼的從屬關係：

```python
temperature = 30

if temperature > 28:
    print("天氣炎熱")
    print("記得補充水分")

print("檢查完成")
```

兩個有四格縮排的 `print()` 都屬於 `if` 區塊；最後一個沒有縮排，因此不屬於 `if`。

專業程式碼最在乎的是：

- 每一層使用四個空白。
- 同一個區塊保持相同縮排。
- 不混用 Tab 與空白。
- 讓編輯器顯示不可見字元，並設定按 Tab 時插入空白。

縮排不一致可能產生 `IndentationError`；Tab 與空白的混用若造成解讀不一致，可能產生更具體的 `TabError`。正確拼法是 `IndentationError`，不是 `identation error`。

---

### 五、基本算術運算子

假設：

```python
a = 7
b = 3
```

| 運算 | 寫法 | 結果 |
| --- | --- | ---: |
| 加法 | `a + b` | `10` |
| 減法 | `a - b` | `4` |
| 乘法 | `a * b` | `21` |
| 一般除法 | `a / b` | `2.333...` |
| 向下取整除法 | `a // b` | `2` |
| 餘數 | `a % b` | `1` |
| 次方 | `a ** b` | `343` |

`//` 常被稱為整數除法，但結果不一定是 `int`：

```python
print(7 // 3)      # 2
print(7.0 // 3)    # 2.0
```

更重要的是，它會向負無限大取整，不是單純把小數部分刪掉：

```python
print(-7 // 3)  # -3
```

因為 `-7 / 3` 約為 `-2.333`，向下取整後是 `-3`。

`**` 表示次方：

```python
print(2 ** 3)  # 8
```

---

### Python 專家最在乎、最注意的事

1. **心智模型要準確**：`=` 是名稱綁定；`==` 才是相等比較。
2. **程式結構要一眼可讀**：四格空白與一致縮排比「程式剛好能跑」更重要。
3. **註解要說明原因**：`#` 是註解；三引號產生字串或 docstring。
4. **清楚理解運算語意**：`/`、`//`、`%` 各自不同，尤其要測試負數。
5. **優先使用括號換行**：比反斜線續行容易閱讀、修改與格式化。
6. **先預測再執行**：預測與實際結果的落差，能最快暴露錯誤理解。

## 開發上可採取的行動步驟

### 1. 啟動本專案的 JupyterLab

在專案根目錄執行：

```bash
uv run jupyter lab
```

建立或開啟 Notebook 後，把下面各段程式分別放進 Cell，使用 `Shift + Enter` 執行。

### 2. 練習指定與比較

執行前先預測四行輸出：

```python
a = 1
b = 2
total = a + b

print(a)
print(b)
print(total)
print(total == 3)
```

### 3. 一次比較所有基本算術運算子

```python
a = 7
b = 3

print("加法：", a + b)
print("減法：", a - b)
print("乘法：", a * b)
print("除法：", a / b)
print("向下取整除法：", a // b)
print("餘數：", a % b)
print("次方：", a ** b)
```

### 4. 用負數驗證 `//` 的真正行為

先猜答案，再執行：

```python
print(7 // 3)
print(-7 // 3)
print(7 // -3)
print(-7 // -3)
```

接著檢查除法演算法常用的不變關係：

```python
a = -7
b = 3

print(a == (a // b) * b + (a % b))  # True
```

### 5. 練習縮排所表達的從屬關係

```python
temperature = 30

if temperature > 28:
    print("天氣炎熱")
    print("記得補充水分")

print("檢查完成")
```

把 `temperature` 改成 `20` 再執行，觀察哪些敘述沒有執行，以及哪一行始終會執行。

### 6. 不開 Notebook，直接在終端機驗證

啟動本專案的 Python 互動環境：

```bash
uv run python
```

看到 `>>>` 後可以逐行輸入：

```python
a = 7
b = 3
print(a + b)
print(a // b)
print(a ** b)
```

輸入 `exit()` 離開。

## 我可以立刻採取的實作清單

- [ ] 執行 `uv run jupyter lab`
- [ ] 分別用自己的話解釋 `=` 與 `==`
- [ ] 執行七種基本算術運算
- [ ] 比較 `7 // 3` 與 `-7 // 3`
- [ ] 驗證 `a == (a // b) * b + (a % b)`
- [ ] 寫出一個含 `if` 與四格縮排的程式區塊
- [ ] 把一個反斜線續行範例改寫成括號換行
- [ ] 用 `#` 寫一則說明「原因」的註解
- [ ] 不看筆記回答下方複習題

### 複習題

先從記憶回答：

1. `=` 與 `==` 的用途有何不同？
2. 為什麼不能把三引號一律稱為多行註解？
3. `-7 // 3` 的結果是什麼？原因是什麼？
4. Python 如何判斷哪些敘述屬於同一個 `if` 區塊？
5. 長運算式為什麼通常優先使用括號換行？
6. `IndentationError` 與 `TabError` 各自表示什麼問題？

<details>
<summary>參考答案</summary>

1. `=` 將右側運算結果指定給左側名稱；`==` 比較兩邊的值是否相等。
2. 三引號建立字串；在特定位置還可能成為 docstring，並非註解語法。
3. 結果是 `-3`，因為 `//` 會向負無限大取整。
4. Python 以縮排層級判斷程式碼的從屬關係。
5. 括號內能自然換行，較容易閱讀、修改，也沒有反斜線尾端的限制。
6. `IndentationError` 表示縮排語法不正確；`TabError` 表示 Tab 與空白的混用造成縮排解讀不一致。

</details>

## 總結

這一節最重要的習慣是：

> 先理解右側運算，再用 `=` 綁定名稱；用一致縮排表達結構；執行前先預測結果。

能寫出 `a = 1` 只是起點。真正可維護的 Python 程式還需要準確的運算語意、清楚的程式區塊，以及不會誤導讀者的註解。若預測與實際輸出不同，應保留程式碼、預測值與實際值，直接詢問教學助理釐清。

## 官方參考資料

- [Python 3.11：Simple statements](https://docs.python.org/3.11/reference/simple_stmts.html)
- [Python 3.11：Compound statements](https://docs.python.org/3.11/reference/compound_stmts.html)
- [Python 3.11：Explicit line joining](https://docs.python.org/3.11/reference/lexical_analysis.html#explicit-line-joining)
- [Python 3.11：Implicit line joining](https://docs.python.org/3.11/reference/lexical_analysis.html#implicit-line-joining)
- [Python 3.11：Indentation](https://docs.python.org/3.11/reference/lexical_analysis.html#indentation)
- [Python 3.11：Expressions](https://docs.python.org/3.11/reference/expressions.html)
- [PEP 8：Indentation](https://peps.python.org/pep-0008/#indentation)
