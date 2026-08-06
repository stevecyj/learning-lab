# 3-3 `print()`、`input()` 與型別轉換

## 核心內容

### 這一節要學會什麼

完成這一節後，我應該能夠：

1. 使用 `print()` 清楚顯示文字、變數與運算結果。
2. 理解 `sep`、`end` 與 `\n` 如何影響輸出。
3. 使用 `input()` 接收使用者輸入。
4. 記住 `input()` 的回傳值永遠是 `str`。
5. 在計算前清理、驗證並轉換輸入。
6. 把輸入、計算與輸出分成容易檢查的步驟。

---

### 一、`print()` 會把物件轉成文字後輸出

```python
message = "Hello Python"
number = 10

print(message)
print(number)
```

`print()` 可以一次接收多個物件，預設以一個空白隔開：

```python
name = "Steve"
score = 95

print("姓名：", name, "分數：", score)
```

輸出：

```text
姓名： Steve 分數： 95
```

完整介面可以先認識成：

```python
print(*objects, sep=" ", end="\n")
```

- `objects`：要輸出的物件，可以有多個。
- `sep`：多個物件之間的分隔文字，預設為一個空白。
- `end`：整次輸出結束後接上的文字，預設為換行 `"\n"`。

例如：

```python
print("2026", "08", "07", sep="-")
```

輸出：

```text
2026-08-07
```

---

### 二、`end` 控制一次輸出如何結尾

兩次一般的 `print()` 會出現在不同行：

```python
print("abc")
print("def")
```

這等同於：

```python
print("abc", end="\n")
print("def", end="\n")
```

若將 `end` 設成空字串 `""`，第一次輸出後不會增加任何字元：

```python
print("Hello ", end="")
print("Python")
```

輸出：

```text
Hello Python
```

`""` 的準確名稱是「空字串」；它的長度為零。`" "` 則包含一個空白字元，兩者不同：

```python
print(len(""))   # 0
print(len(" "))  # 1
```

`end` 也可以使用其他字串：

```python
print("處理中", end="...")
print("完成")
```

---

### 三、`\n` 是換行跳脫序列

```python
print("第一行\n第二行")
```

輸出：

```text
第一行
第二行
```

若要在輸出中顯示反斜線與字母 `n`，要將反斜線本身跳脫：

```python
print("第一行\\n第二行")
```

輸出：

```text
第一行\n第二行
```

也可以使用 raw string：

```python
print(r"第一行\n第二行")
```

raw string 仍有自己的語法限制，不能簡化成「所有反斜線永遠失效」。現階段遇到單一反斜線時，先使用 `\\` 最清楚。

---

### 四、格式化輸出優先使用 f-string

教材中的 `.format()` 仍是有效語法：

```python
a = 3
b = 2
c = 1

print("a is {}, b is {}, c is {}".format(a, b, c))
```

在目前的 Python 程式中，簡單格式化通常優先使用 f-string。變數與對應位置更容易閱讀：

```python
print(f"a is {a}, b is {b}, c is {c}")
```

也可以直接放入運算式與格式規則：

```python
width = 5.5
height = 3.5
area = width * height

print(f"面積：{area:.2f}")
```

`:.2f` 表示以小數點後兩位顯示。它只改變顯示格式，不會改變 `area` 原本的值。

---

### 五、`input()` 永遠回傳字串

```python
name = input("請輸入姓名：")
print(f"你好，{name}")
```

提示文字會先顯示，而且不會自動換行。程式接著暫停，等待使用者輸入一行文字並按 Enter。

即使輸入 `123`，結果仍是 `str`：

```python
number_text = input("請輸入數字：")

print(number_text)
print(type(number_text))  # <class 'str'>
```

因此下面的結果是字串串接，不是數字加法：

```python
number_text = "123"
print(number_text + "1")  # 1231
```

若直接把字串與整數相加，會發生 `TypeError`：

```python
number_text = "123"
print(number_text + 1)
```

---

### 六、輸入後要清理、驗證、轉型

整數轉換：

```python
age_text = input("請輸入年齡：")
age = int(age_text)
```

浮點數轉換：

```python
width_text = input("請輸入寬度：")
width = float(width_text)
```

也可以合併成一行：

```python
width = float(input("請輸入寬度："))
```

但拆開後比較容易檢查原始輸入，也方便顯示精確的錯誤訊息。專業程式常把輸入邊界寫成四步：

```text
1. 讀取文字
2. 清理空白
3. 驗證與轉型
4. 使用轉型後的值
```

例如：

```python
width_text = input("請輸入寬度：").strip()
width = float(width_text)
area = width * 2

print(f"面積：{area}")
```

`strip()` 會移除字串開頭與結尾的空白。它不會判斷內容是否為有效數字。

---

### 七、轉型可能失敗

下面的輸入無法轉成 `float`：

```python
float("abc")
```

Python 會引發 `ValueError`。互動程式應對這個可預期的錯誤給出明確回饋：

```python
width_text = input("請輸入寬度：").strip()

try:
    width = float(width_text)
except ValueError:
    print("輸入錯誤：寬度必須是數字。")
else:
    print(f"寬度為 {width}")
```

只捕捉預期的 `ValueError`，不要用空泛的 `except:` 隱藏其他程式錯誤。

`input()` 遇到輸入串流結束時也可能引發 `EOFError`。初學互動練習通常不會遇到，但在管線、測試或自動化環境中需要留意。

---

### 八、完整範例：計算長方形面積

先寫最直接的版本：

```python
width = float(input("請輸入寬度："))
height = float(input("請輸入高度："))
area = width * height

print(f"長方形面積：{area:.2f}")
```

再加入輸入驗證：

```python
width_text = input("請輸入寬度：").strip()
height_text = input("請輸入高度：").strip()

try:
    width = float(width_text)
    height = float(height_text)
except ValueError:
    print("輸入錯誤：寬度與高度都必須是數字。")
else:
    if width <= 0 or height <= 0:
        print("輸入錯誤：寬度與高度必須大於 0。")
    else:
        area = width * height
        print(f"長方形面積：{area:.2f}")
```

這裡包含兩種不同驗證：

- 格式驗證：能不能轉成 `float`。
- 業務規則：長度是否大於零。

---

### Python 專家最注重的事

1. **把輸入視為不可信任的字串**：先清理、驗證、轉型，再進行計算。
2. **錯誤訊息要能幫助使用者修正**：說明需要什麼格式，不只顯示「發生錯誤」。
3. **分開輸入、計算與輸出**：每一步都能獨立檢查，之後也容易寫測試。
4. **輸出格式要明確**：使用 f-string、單位與合理的小數位數。
5. **只捕捉預期的例外**：數字轉換處理 `ValueError`，不要用 `except:` 隱藏問題。
6. **選擇適合資料的型別**：`int` 適合整數，`float` 適合一般小數近似值；金額等精確十進位資料不應草率依賴 `float`。
7. **除錯輸出與正式紀錄不同**：`print()` 適合學習與簡單 CLI；正式應用的事件紀錄通常使用 `logging`。
8. **不要對使用者輸入使用 `eval()`**：它會執行輸入內容，可能造成嚴重安全問題。

## 開發上可採取的行動步驟

### 1. 啟動 Python 互動環境

在專案根目錄執行：

```bash
uv run python
```

看到 `>>>` 後逐行輸入：

```python
name = input("請輸入姓名：")
print(f"你好，{name}")
type(name)
```

輸入 `exit()` 離開。

### 2. 啟動 JupyterLab

```bash
uv run jupyter lab
```

在 Notebook 中執行：

```python
a = 3
b = 2
c = 1

print(a, b, c)
print(a, b, c, sep=" | ")
print(f"a={a}, b={b}, c={c}")
```

### 3. 比較 `end` 的三種結果

```python
print("A")
print("B")

print("A", end="")
print("B")

print("A", end=" -> ")
print("B")
```

執行前先畫出自己預期的三組輸出。

### 4. 比較字串與數字運算

```python
number_text = "10"
number = int(number_text)

print(number_text + number_text)  # 1010
print(number + number)            # 20
print(type(number_text))
print(type(number))
```

### 5. 直接執行一行格式化練習

```bash
uv run python -c 'width = 5.5; height = 3.5; print(f"面積：{width * height:.2f}")'
```

預期輸出：

```text
面積：19.25
```

### 6. 完成輸入驗證挑戰

將長方形範例貼入 Notebook 或 Python 檔案，依序測試：

```text
寬 5.5，高 3.5
寬 abc，高 3.5
寬 -2，高 3.5
寬為空字串，高 3.5
```

每次執行前先預測會走進 `except`、`if` 或 `else` 的哪一條路徑。

## 我可以立刻採取的實作清單

- [ ] 執行 `uv run python`
- [ ] 用 `input()` 接收姓名並用 f-string 輸出
- [ ] 比較 `end="\n"`、`end=""` 與 `end=" -> "`
- [ ] 使用 `sep` 自訂多個輸出值的分隔方式
- [ ] 比較 `"10" + "10"` 與 `10 + 10`
- [ ] 用 `type()` 確認 `input()` 的結果是 `str`
- [ ] 使用 `int()` 與 `float()` 轉換有效輸入
- [ ] 輸入 `abc`，觀察並處理 `ValueError`
- [ ] 完成含正數驗證的長方形面積程式
- [ ] 不看筆記回答下方複習題

### 複習題

先從記憶回答：

1. `print()` 的 `sep` 與 `end` 分別控制什麼？
2. `print()` 的 `end` 預設值是什麼？
3. `""` 與 `" "` 有什麼差別？
4. 如何輸出字面上的 `\n`，而不是換行？
5. 使用者輸入 `123` 後，`input()` 回傳什麼型別？
6. `int("abc")` 會發生什麼事？
7. 為什麼輸入格式正確後，還要檢查長度是否大於零？
8. `.format()` 與 f-string 都能格式化字串，簡單情況為什麼通常優先使用 f-string？

<details>
<summary>參考答案</summary>

1. `sep` 控制多個輸出物件之間的分隔文字；`end` 控制整次輸出結束後接上的文字。
2. 預設是換行字串 `"\n"`。
3. `""` 長度為零；`" "` 包含一個空白字元，長度為一。
4. 在一般字串中寫成 `"\\n"`，或在適合情況下使用 raw string。
5. 回傳 `str`，內容是 `"123"`。
6. 無法完成轉換，會引發 `ValueError`。
7. 轉型只驗證數字格式；大於零是長方形尺寸的業務規則。
8. f-string 讓變數或運算式直接出現在對應位置，通常更容易閱讀與維護。

</details>

## 總結

這一節最重要的流程是：

> `input()` 取得文字 → 清理與驗證 → 轉成需要的型別 → 計算 → 用 `print()` 清楚呈現。

`print()` 與 `input()` 看似簡單，卻是程式與外界互動的第一個邊界。可靠的程式不會假設使用者一定輸入正確，也不會讓格式化與計算混成難以檢查的一行。若實際結果與預測不同，可以把輸入內容、程式碼、錯誤訊息與預期結果一起交給教學助理分析。

## 官方參考資料

- [Python 3.11：`print()`](https://docs.python.org/3.11/library/functions.html#print)
- [Python 3.11：`input()`](https://docs.python.org/3.11/library/functions.html#input)
- [Python 3.11：`int()`](https://docs.python.org/3.11/library/functions.html#int)
- [Python 3.11：`float()`](https://docs.python.org/3.11/library/functions.html#float)
- [Python 3.11：Formatted string literals](https://docs.python.org/3.11/reference/lexical_analysis.html#f-strings)
- [Python 3.11：Errors and Exceptions](https://docs.python.org/3.11/tutorial/errors.html)
