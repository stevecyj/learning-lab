# 6-1 Python 字串：索引、切片與常用方法

## 學習目標

完成這一節後，我應該能夠：

1. 使用單引號、雙引號與三引號建立字串。
2. 用正索引與負索引取得單一字元。
3. 使用 `[start:stop:step]` 切出需要的字串片段。
4. 使用 `+`、`*` 與 `len()` 組合、重複及計算字串長度。
5. 使用 `lower()`、`upper()`、`replace()`、`split()` 與 `strip()` 處理文字。
6. 說明字串不可變，並分辨函式與字串方法。

---

## 一、字串是不可變的文字序列

Python 的字串型別是 `str`。字串由一連串 Unicode 字元組成，可以使用單引號或雙引號建立：

```python
greeting = 'Hello'
name = "Isaac"

print(type(greeting))  # <class 'str'>
```

單引號和雙引號產生的型別及功能相同。可以依內容選擇較容易閱讀的寫法：

```python
message = "I'm learning Python."
quote = '他說：「早安。」'
```

空字串是長度為零的字串：

```python
empty_string = ""

print(len(empty_string))  # 0
print(bool(empty_string)) # False
```

### 三引號適合多行文字

三個單引號或三個雙引號都能建立三引號字串：

```python
paragraph = """第一行
第二行
第三行"""
```

三引號字串可以直接跨行，並保留換行。它也常用來撰寫函式、類別與模組的文件字串（docstring）。

> 教材稱「序列化類別」，正確名稱是「序列型別」（sequence types）。序列型別依順序存放元素，序列化則是把資料轉成便於儲存或傳輸的格式。字串、串列（`list`）和元組（`tuple`）都是序列型別。

參考：[Python 官方文件：Text Sequence Type — `str`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)

---

## 二、索引用位置取得一個字元

索引從 `0` 開始：

```python
s = "hello"

print(s[0])  # h
print(s[1])  # e
print(s[2])  # l
```

字串 `"hello"` 的索引如下：

| 字元 | `h` | `e` | `l` | `l` | `o` |
| --- | ---: | ---: | ---: | ---: | ---: |
| 正索引 | `0` | `1` | `2` | `3` | `4` |
| 負索引 | `-5` | `-4` | `-3` | `-2` | `-1` |

負索引從尾端開始計算，因此 `-1` 是最後一個字元：

```python
print(s[-1])  # o
print(s[-2])  # l
```

若單一索引超出範圍，Python 會拋出 `IndexError`：

```python
# print(s[5])  # IndexError: string index out of range
```

索引取得的結果仍然是 `str`，Python 沒有獨立的「單一字元型別」：

```python
print(type(s[0]))  # <class 'str'>
print(len(s[0]))   # 1
```

---

## 三、切片的範圍包含起點、不包含終點

切片（slicing）的完整語法是：

```python
sequence[start:stop:step]
```

- `start`：從哪個索引開始，包含這個位置。
- `stop`：在哪個索引前停止，不包含這個位置。
- `step`：每次移動幾格，省略時是 `1`。

這種「包含起點、不包含終點」的範圍也稱為半開區間。以 `s = "Python"` 為例：

```python
s = "Python"

print(s[2:])       # thon：從索引 2 到結尾
print(s[:-2])      # Pyth：從開頭到倒數第二字元之前
print(s[1:-1:2])   # yh：索引 1 開始，每次前進 2 格
print(s[:])        # Python：完整切片
print(s[::-1])     # nohtyP：反向切片
```

省略 `start` 代表從開頭開始；省略 `stop` 代表到結尾；省略兩者就是選取整段字串。

再看教材中的 `beautiful`：

```python
word = "beautiful"

print(word[3:7])    # utif
print(word[:3])     # bea
print(word[3:])     # utiful
print(word[3:7:2])  # ui
```

`word[3:7]` 會取得索引 `3、4、5、6`，不包含索引 `7`，所以正確結果是 `"utif"`。教材字幕中的 `"utis"` 是口誤。

切片超出邊界通常不會出錯，Python 只會取出實際存在的部分：

```python
print(word[:100])  # beautiful
```

但是 `step` 不能是 `0`，否則會得到 `ValueError`。

參考：[Python 官方文件：Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

---

## 四、`+` 是串接，`*` 是重複

兩個字串可以使用 `+` 串接：

```python
greeting = "Hello"
name = "Isaac"

print(greeting + " " + name)  # Hello Isaac
```

字串乘上整數會重複指定次數：

```python
marks = "!!!"

print(greeting + marks)      # Hello!!!
print(greeting + marks * 2)  # Hello!!!!!!
print("ha" * 3)             # hahaha
```

`*` 的優先順序高於 `+`，所以 `marks * 2` 會先執行，再與 `greeting` 串接。

換行字元寫成 `\n`：

```python
morning = "Good morning"
title = "Sir"

print(morning + "\n" + title)
```

輸出：

```text
Good morning
Sir
```

字串不能直接和數字相加。若要串接，需先把數字轉成字串；組合不同型別的值時，通常使用 f-string：

```python
age = 20

# print("Age: " + age)  # TypeError
print("Age: " + str(age))
print(f"Age: {age}")
```

---

## 五、`len()` 計算長度，字串方法轉換內容

`len()` 是 Python 內建函式，會回傳字串的長度：

```python
word = "hello"
print(len(word))  # 5
```

教材字幕中的 `lem` 是辨識錯誤，正確名稱是 `len`。

字串本身也提供許多方法。方法以 `字串.方法()` 的形式呼叫：

```python
text = "Hello I am Isaac"

print(text.lower())            # hello i am isaac
print(text.upper())            # HELLO I AM ISAAC
print(text.replace(" ", "@")) # Hello@I@am@Isaac
print(text.split())            # ['Hello', 'I', 'am', 'Isaac']
```

| 寫法 | 用途 | 回傳型別 |
| --- | --- | --- |
| `len(text)` | 計算字串長度 | `int` |
| `text.lower()` | 英文字母轉小寫 | `str` |
| `text.upper()` | 英文字母轉大寫 | `str` |
| `text.replace(old, new)` | 取代符合的片段 | `str` |
| `text.split()` | 依空白拆成多個片段 | `list[str]` |
| `text.strip()` | 移除字串兩端的空白字元 | `str` |

`split()` 回傳的是串列，不是字串。沒有傳入分隔符號時，它會把連續空白視為一組，並忽略字串兩端的空白：

```python
text = "  Hello   Python  "

print(text.split())      # ['Hello', 'Python']
print(text.split(" "))  # ['', '', 'Hello', '', '', 'Python', '', '']
```

---

## 六、`strip()` 不會取消 `print()` 的換行

`strip()` 會移除字串開頭和結尾的空白字元，包括空格、Tab 與換行：

```python
message = "  Hello I am Isaac\n"

print(repr(message))          # '  Hello I am Isaac\n'
print(repr(message.strip()))  # 'Hello I am Isaac'
```

`strip()` 會移除字串兩端連續的空白字元，不限於最後一個換行。只處理右側或左側時，分別使用 `rstrip()` 或 `lstrip()`。

教材把 `print(message.strip())` 說成「不會換行」，這不精確。`strip()` 只改變交給 `print()` 的字串內容，`print()` 預設仍會在輸出結尾加上換行。若不想讓 `print()` 自動換行，應設定 `end`：

```python
print(message.strip(), end="")
```

當字串本身以 `\n` 結尾時，直接 `print(message)` 看起來會多出一個空白行：一個換行來自字串，另一個來自 `print()`。

---

## 七、Python 開發者會留意的字串特性

1. **字串不可變（immutable）。** 建立後不能直接修改其中一個位置：

   ```python
   word = "cat"
   # word[0] = "b"  # TypeError

   word = "b" + word[1:]
   print(word)  # bat
   ```

2. **字串方法通常回傳新值。** `lower()`、`replace()` 與 `strip()` 不會原地改變原字串：

   ```python
   text = " Hello "
   cleaned = text.strip().lower()

   print(repr(text))     # ' Hello '
   print(cleaned)        # hello
   ```

3. **索引與切片操作的是 Unicode 字串元素，不一定等於畫面上的完整符號。** 某些 emoji、旗幟或由組合字元構成的文字，`len()` 的結果可能和畫面上看到的字數不同。一般英數及多數單一中文字不會遇到這個問題。

4. **大量字串不要在迴圈中反覆使用 `+`。** 要組合許多片段時，先收集到串列，再用 `"".join(parts)` 一次合併。這能避免反覆建立中間字串，也直接表達「合併所有片段」的用途。

5. **`strip(chars)` 的參數不是完整前綴或後綴。** 它會從兩端移除「參數中任一字元」。要移除固定前綴或後綴，使用 `removeprefix()` 或 `removesuffix()`。

6. **命名避免覆蓋內建名稱。** 不要把變數命名成 `str` 或 `len`，否則稍後可能無法正常呼叫同名內建工具。

參考：[Python 官方文件：String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)

---

## 八、動手練習

在 Notebook 或 `.py` 檔案中完成下面的預測—執行—核對練習。

### 步驟 1：先預測，不要立刻執行

```python
text = "  Beautiful Python\n"

print(repr(text[2:11]))
print(repr(text[-7:-1]))
print(repr(text.strip()))
print(text.strip().lower().replace(" ", "-"))
print(text.split())
```

先寫下五行輸出，再執行程式核對。`repr()` 會把空格和 `\n` 顯示出來，適合觀察字串的實際內容。

### 步驟 2：做一個可重用的文字清理流程

```python
raw_name = "  Ada LOVELACE\n"
clean_name = raw_name.strip().lower()
slug = clean_name.replace(" ", "-")

print(f"原始內容：{raw_name!r}")
print(f"清理結果：{clean_name!r}")
print(f"網址名稱：{slug!r}")
```

整理表單欄位、CSV 欄位或檔名時，也可以沿用「清除兩端空白 → 統一大小寫 → 替換分隔符號」這三步。

### 步驟 3：隔一天再做一次記憶提取

不看筆記寫出：

- 取得最後一個字元的方法。
- 反轉字串的切片。
- 移除兩端空白的方法。
- 依空白拆分字串的方法。
- 讓 `print()` 不在結尾換行的方法。

忘記時先嘗試執行小範例觀察，再回來核對答案。

---

## 九、文末示範解答

逐字稿結尾沒有獨立列出題目。最後一段示範要釐清的是：為什麼直接 `print()` 會多出一行，以及 `strip()` 做了什麼。

```python
message = "Hello I am Isaac\n"

print(message)
```

`message` 自帶一個 `\n`，而 `print()` 顯示完內容後又加一個換行，因此後方會出現空白行。

```python
print(message.strip())
```

`strip()` 回傳不含結尾 `\n` 的新字串，所以畫面不再多出空白行。`print()` 本身依舊會在最後換行。要讓游標停在同一行，可以這樣寫：

```python
print(message.strip(), end="")
```

教材中的其他示範結果如下：

```python
a = "beautiful"

print(a[3:7])    # utif
print(a[:3])     # bea
print(a[3:])     # utiful
print(a[3:7:2])  # ui
```

---

## 十、複習題

請先不看答案，直接從記憶回答。

1. 單引號、雙引號與三引號建立的值都是什麼型別？
2. `"Python"[-1]` 的結果是什麼？
3. 切片的 `stop` 位置會不會包含在結果中？
4. `"beautiful"[3:7]` 和 `"beautiful"[3:7:2]` 分別是什麼？
5. `"ha" * 3` 的結果是什麼？
6. `split()` 回傳字串還是串列？
7. 為什麼只執行 `text.lower()` 不會改變原本的 `text`？
8. `strip()` 和 `print(..., end="")` 解決的是同一個問題嗎？
9. 單一索引和超出範圍的切片，對邊界錯誤的反應有何不同？
10. 如何用切片反轉字串 `s`？

<details>
<summary>參考答案</summary>

1. 都是 `str`。
2. `"n"`。
3. 不會；切片包含 `start`，不包含 `stop`。
4. 分別是 `"utif"` 與 `"ui"`。
5. `"hahaha"`。
6. 回傳串列，也就是 `list[str]`。
7. 因為字串不可變；`lower()` 會回傳新字串，不會原地修改舊字串。若需要結果，必須指定給名稱或直接使用回傳值。
8. 不是。`strip()` 移除字串兩端的空白；`end=""` 控制 `print()` 顯示後是否額外輸出換行。
9. 超出範圍的單一索引會拋出 `IndexError`；切片通常會自動限制在有效邊界內。
10. `s[::-1]`。

</details>

---

## 本節教材補充

| 教材說法 | 修正或補充 |
| --- | --- |
| 序列化類別 | 應稱「序列型別」；序列化是另一個概念 |
| 列表與元祖 | 臺灣常用名稱為「串列」與「元組」 |
| 三引號是很長的字串 | 三引號支援多行內容，也可用作 docstring |
| `s[起點:終點]` | 完整形式是 `s[start:stop:step]`，而且不包含 `stop` |
| `beautiful[3:7]` 得到 `utis` | 正確結果是 `utif` |
| 把字串丟到 `lem` | 正確內建函式名稱是 `len()` |
| 字串的內建函數 | `lower()` 等是字串方法；`len()` 才是內建函式 |
| `strip()` 拿掉最後面的換行 | 它會移除字串兩端的空白字元，不只處理結尾換行 |
| `strip()` 後 `print()` 不會換行 | `print()` 仍會換行，只是不再因字串內的 `\n` 多出空白行 |

## 延伸閱讀

- [Python 官方文件：Text Sequence Type — `str`](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
- [Python 官方文件：Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)
- [Python 官方文件：String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [Python 官方教學：Strings](https://docs.python.org/3/tutorial/introduction.html#strings)

遇到預測與實際輸出不同時，先保留兩份答案，再用 `repr()`、`type()` 和 `len()` 檢查內容與型別，找出推理從哪一步開始不同。
