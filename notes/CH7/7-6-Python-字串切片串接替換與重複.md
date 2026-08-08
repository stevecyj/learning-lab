# 7-6 Python 字串練習：串接、切片、替換與重複

## 學習目標

這一節練習五種常見的字串操作。完成後，我應該能夠：

1. 使用 `join()` 將多個字串元素串接成一個字串。
2. 使用 `len()` 計算字串的字元數。
3. 用正索引與負索引取得字串開頭、結尾的字元。
4. 使用切片取出前兩個與後兩個字元。
5. 只替換第一個字元之後的重複字元。
6. 使用 `*` 重複字串，並核對結果的長度與次數。

---

## 一、用 `join()` 把字串串列黏起來

先把串列裡的字串接成一個字串：

```python
characters = ["a", "b", "c", "d"]

result = "".join(characters)

print(result)  # abcd
```

寫在 `join()` 前面的字串，會成為元素之間的**分隔字串**：

```python
characters = ["a", "b", "c", "d"]

print("@".join(characters))   # a@b@c@d
print("-".join(characters))   # a-b-c-d
print("".join(characters))    # abcd
```

`separator.join(strings)` 的意思是：「用 `separator` 串接 `strings` 裡的每個字串。」分隔字串只放在相鄰元素之間，開頭和結尾不會多出一份。

### `join()` 要求每個元素都是字串

```python
values = ["age", 18]

# print(" ".join(values))
# TypeError: sequence item 1: expected str instance, int found
```

串列若混有其他型別，要先把它們轉成字串：

```python
values = ["age", 18]
text_values = [str(value) for value in values]

print(" ".join(text_values))  # age 18
```

串列長度固定且很短時，也能用 `+`：

```python
characters = ["a", "b", "c", "d"]
result = characters[0] + characters[1] + characters[2] + characters[3]
```

元素數量不固定時，用 `join()` 就不必逐一寫索引。

參考：[Python 官方文件：`str.join()`](https://docs.python.org/3/library/stdtypes.html#str.join)

---

## 二、`len()` 計算字串中的字元數

`len(text)` 會回傳 `text` 的字元數：

```python
text = "Isaac"

print(len(text))  # 5
```

空白和標點也都是字元：

```python
print(len("Hi!"))    # 3
print(len("Hi !"))   # 4，中間的空白也算一個字元
print(len(""))       # 0
```

`len()` 回傳整數，也能拿來檢查輸入長度：

```python
text = input("請輸入至少兩個字元：")

if len(text) < 2:
    print("輸入太短")
else:
    print("長度符合要求")
```

> `len()` 計算 Python 字串中的 Unicode 碼位（code point），不一定等於畫面上看到的字形數，也不是編碼後的位元組數。英文字母通常沒有這個差異；表情符號、組合字元和某些 emoji 則可能有。

參考：[Python 官方文件：`len()`](https://docs.python.org/3/library/functions.html#len)

---

## 三、用切片取出前兩個與後兩個字元

輸入一個至少有 `2` 個字元的字串，再串接前兩個和後兩個字元：

```python
text = input("請輸入至少兩個字元：")
result = text[:2] + text[-2:]

print(result)
```

輸入 `"w3resource"` 時：

```text
text[:2]   -> "w3"
text[-2:]  -> "ce"
結果       -> "w3ce"
```

輸入 `"Isaac"` 時，結果是 `"Isac"`。Python 字串區分大小寫，所以開頭仍是大寫 `I`。

### 切片的停止位置不包含在結果中

切片的寫法是：

```python
text[start:stop]
```

- `start` 是開始位置，包含在結果內。
- `stop` 是停止位置，不包含在結果內。
- 省略 `start` 表示從開頭開始。
- 省略 `stop` 表示一路取到結尾。
- 負索引從尾端計算，`-1` 是最後一個字元，`-2` 是倒數第二個字元。

若輸入剛好只有兩個字元，例如 `"ab"`：

```python
text = "ab"
print(text[:2] + text[-2:])  # abab
```

前兩個和後兩個指向同一段內容，因此會重複一次。

切片超出邊界通常不會出現 `IndexError`：

```python
text = "a"
print(text[:2] + text[-2:])  # aa
```

程式雖然能執行，輸入仍不符合「至少兩個字元」的規格，所以要先用 `len(text)` 驗證。

參考：[Python 官方文件：Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

---

## 四、保留第一個字元，只替換後面相同的字元

保留第一個字元，後面相同的字元全部改成 `$`。

以 `"restart"` 為例，第一個字元是 `r`，後面再次出現的 `r` 要替換：

```text
restart -> resta$t
```

先保存第一個字元，再對索引 `1` 之後的切片呼叫 `replace()`：

```python
text = input("請輸入一個非空字串：")

first_character = text[0]
remaining_text = text[1:].replace(first_character, "$")
result = first_character + remaining_text

print(result)
```

也可以合併成一個運算式：

```python
result = text[0] + text[1:].replace(text[0], "$")
```

### 直接替換會連第一個字元一起改掉

```python
text = "restart"
result = text.replace(text[0], "$")

print(result)  # $esta$t
```

`replace()` 會處理整個字串，連第一個 `r` 也會換掉。要保留它，就只替換 `text[1:]`。

影片採用另一種寫法：先替換整個字串，再把原本的第一個字元加回來。

```python
text = "restart"
replaced = text.replace(text[0], "$")
result = text[0] + replaced[1:]

print(result)  # resta$t
```

### `replace()` 不會原地修改原字串

Python 字串是不可變物件。`replace()` 會回傳新字串，原本的 `text` 不會改變：

```python
text = "restart"
new_text = text.replace("r", "$")

print(text)      # restart
print(new_text)  # $esta$t
```

要保留替換結果，就把回傳值指派給變數，或直接拿去做下一個運算。

`replace()` 也區分大小寫。第一個字元若是大寫 `A`，後面的小寫 `a` 不會被替換。

> 輸入不能是空字串，否則 `text[0]` 會引發 `IndexError`。不確定輸入內容時，先用 `if not text:` 檢查。

參考：[Python 官方文件：`str.replace()`](https://docs.python.org/3/library/stdtypes.html#str.replace)

---

## 五、使用 `*` 重複最後兩個字元

取出最後兩個字元，再重複四次：

```python
text = input("請輸入至少兩個字元：")
last_two = text[-2:]
result = last_two * 4

print(result)
```

若輸入 `"Isaac"`：

```text
last_two       -> "ac"
last_two * 4   -> "acacacac"
```

影片結尾口述的 `acacac` 只有三組 `ac`。程式寫的是 `* 4`，結果應為 `acacacac`。

字串乘上非負整數代表重複：

```python
print("ha" * 3)  # hahaha
print("ha" * 1)  # ha
print("ha" * 0)  # 空字串
```

字串的 `*` 是序列重複運算。最後兩個字元的長度是 `2`，重複 `4` 次後，結果長度應為 `8`：

```python
assert len(last_two * 4) == 8
```

這個 `assert` 假設輸入至少有兩個字元。輸入較短時，`text[-2:]` 只會回傳實際取得的部分。

---

## 六、五題完整參考程式

```python
# 1. 串接字串串列
characters = ["a", "b", "c", "d"]
print("".join(characters))

# 2. 計算字串長度
text = "Isaac"
print(len(text))

# 3. 串接前兩個與後兩個字元
text = "w3resource"
print(text[:2] + text[-2:])

# 4. 保留第一個字元，替換後面相同的字元
text = "restart"
print(text[0] + text[1:].replace(text[0], "$"))

# 5. 將最後兩個字元重複四次
text = "Isaac"
print(text[-2:] * 4)
```

預期輸出：

```text
abcd
5
w3ce
resta$t
acacacac
```

---

## 七、動手練習

請在 Notebook 或 `.py` 檔案中依序「先預測、再執行、最後核對」。

1. 預測 `"@".join(["A", "B", "C"])` 的結果。
2. 預測 `len("A B")` 的結果，並說明空白是否計入。
3. 預測 `"Python"[:2] + "Python"[-2:]` 的結果。
4. 將 `"babble"` 中第一個字元之後的 `b` 全部換成 `$`。
5. 預測 `"Python"[-2:] * 4` 的結果與長度。
6. 嘗試執行 `"-".join([1, 2, 3])`，觀察錯誤訊息，再修正程式。

<details>
<summary>參考答案</summary>

1. `"A@B@C"`。
2. `3`；中間的空白也是一個字元。
3. `"Pyon"`，因為前兩個字元是 `"Py"`，後兩個是 `"on"`。
4. `"ba$$le"`：

   ```python
   text = "babble"
   result = text[0] + text[1:].replace(text[0], "$")
   print(result)
   ```

5. `"onononon"`，長度為 `8`。
6. 原程式會出現 `TypeError`，因為 `join()` 需要字串元素：

   ```python
   numbers = [1, 2, 3]
   result = "-".join(str(number) for number in numbers)
   print(result)  # 1-2-3
   ```

</details>
