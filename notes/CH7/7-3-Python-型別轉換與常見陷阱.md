# 7-3 Python 型別轉換：數字、字串與容器

## 學習目標

完成這一節後，我應該能夠：

1. 使用 `type()` 確認物件目前的型別。
2. 使用 `int()`、`float()`、`str()` 轉換常見的數字與字串。
3. 使用 `list()`、`tuple()`、`set()` 轉換可迭代物件。
4. 解釋為什麼 `list("1000")` 會逐字拆開。
5. 看懂轉換失敗時常見的 `ValueError` 與 `TypeError`。
6. 辨認資料遺失、千分位逗號與 `bool("False")` 等常見陷阱。

---

## 一、型別轉換會根據目標型別解讀資料

Python 內建的 `int`、`float`、`str`、`list`、`tuple`、`set` 等名稱，既是 `type()` 可能顯示的型別名稱，也可以像函數一樣呼叫，用來建立該型別的物件：

```python
integer_value = int("42")
float_value = float("42.5")
text_value = str(42)
list_value = list("Python")
tuple_value = tuple([1, 2, 3])
set_value = set([1, 1, 2, 3])
```

常見形式如下：

```python
目標型別(要轉換的值)
```

型別轉換仍有限制。傳入的資料必須符合目標型別能接受的格式，而且不同型別會用不同規則解讀資料。

| 寫法 | 結果 | 說明 |
| --- | --- | --- |
| `int("42")` | `42` | 解析整數格式的字串 |
| `float("42")` | `42.0` | 解析浮點數格式的字串 |
| `str(42)` | `"42"` | 建立文字表示 |
| `list("abc")` | `["a", "b", "c"]` | 逐一收集字串中的字元 |
| `tuple([1, 2])` | `(1, 2)` | 逐一收集串列元素 |
| `set([1, 1, 2])` | `{1, 2}` | 收集元素並移除重複值 |

參考：[Python 官方文件：Built-in Functions](https://docs.python.org/3/library/functions.html)

---

## 二、先用 `type()` 確認目前的型別

引號中的數字仍然是字串：

```python
my_string = "1000"

print(type(my_string))
# <class 'str'>
```

`type()` 回傳物件的型別。當輸出和預期不同時，可以先用它檢查資料目前的型別：

```python
print(type(1000))       # <class 'int'>
print(type(1000.0))     # <class 'float'>
print(type("1000"))     # <class 'str'>
print(type(["1000"]))   # <class 'list'>
```

`"1000"` 和 `1000` 顯示時很像，但前者是文字，後者才是可以直接進行數值運算的整數。

```python
print("1000" + "50")  # 100050，字串串接
print(1000 + 50)        # 1050，整數加法
```

---

## 三、`int()`、`float()` 與 `str()` 轉換數字和文字

### 字串轉成整數或浮點數

```python
count_text = "1000"
price_text = "49.5"

count = int(count_text)
price = float(price_text)

print(count)        # 1000
print(type(count))  # <class 'int'>
print(price)        # 49.5
print(type(price))  # <class 'float'>
```

`int()` 要求字串符合整數格式，因此不能直接解析帶小數點的字串：

```python
# int("49.5")  # ValueError: invalid literal for int()
```

若資料本來表示小數，可以先轉成 `float`；但是否再轉成整數，必須先判斷捨去小數是否符合需求：

```python
value = float("49.5")
whole = int(value)

print(whole)  # 49，小數部分直接被截掉，不是四捨五入
```

### 數字轉成字串

`str()` 常用於把數值放入文字內容：

```python
score = 95
message = "分數：" + str(score)

print(message)        # 分數：95
print(type(message))  # <class 'str'>
```

也可以改用 f-string，省去字串串接和 `str()`：

```python
message = f"分數：{score}"
```

---

## 四、千分位逗號不是 `float()` 預設接受的格式

教材字幕把範例說成字串 `"1,000"`，同時又說它能直接轉成浮點數、轉成串列後有四個元素。這兩件事只有在原始程式其實使用 `"1000"` 時才成立：

```python
my_string = "1000"

my_float = float(my_string)
my_list = list(my_string)

print(my_float)  # 1000.0
print(my_list)   # ['1', '0', '0', '0']
```

真正含有千分位逗號的 `"1,000"` 不能直接交給 `float()`：

```python
# float("1,000")  # ValueError: could not convert string to float

text = "1,000"
number = float(text.replace(",", ""))

print(number)      # 1000.0
print(list(text))  # ['1', ',', '0', '0', '0']，共 5 個元素
```

`replace()` 適合格式來源已知、規則簡單的資料。若處理使用者輸入、不同地區格式或財務資料，逗號和小數點的意義可能不同，不能未經驗證就全部刪除。

---

## 五、`list()` 與 `tuple()` 會逐一讀取可迭代物件

字串是可迭代物件；走訪字串時，每次取得一個字元。因此 `list()` 不會把整個字串包成單一元素，而是逐字建立串列：

```python
digits = list("1000")

print(digits)       # ['1', '0', '0', '0']
print(len(digits))  # 4
```

若要讓完整字串成為唯一元素，應直接使用串列字面值：

```python
whole_text = ["1000"]

print(whole_text)       # ['1000']
print(len(whole_text))  # 1
```

把串列轉成元組時，`tuple()` 也會逐一收集元素：

```python
my_list = [10, 20, 30]
my_tuple = tuple(my_list)

print(my_tuple)        # (10, 20, 30)
print(type(my_tuple))  # <class 'tuple'>
print(my_list)         # [10, 20, 30]
```

`tuple(my_list)` 會建立新的元組，所以要把結果指派給變數。它不會把 `my_list` 原地改成元組，原本的串列仍然是 `list`。

容器間常見的轉換如下：

```python
numbers = [3, 1, 3, 2]

as_tuple = tuple(numbers)  # (3, 1, 3, 2)
as_set = set(numbers)      # {1, 2, 3}，去重且不保證順序
back_to_list = list(as_tuple)  # [3, 1, 3, 2]
```

從 `list` 轉成 `tuple` 會保留元素順序與重複值；轉成 `set` 則會去除重複值，而且不應依賴顯示順序。因此，轉成 `set` 可能失去原本的順序與重複次數。

參考：[Python 官方教學：Data Structures](https://docs.python.org/3/tutorial/datastructures.html)

---

## 六、轉換失敗時，分辨 `ValueError` 與 `TypeError`

### `ValueError`：型別可以接收，但內容格式不合規則

```python
# int("hello")    # ValueError
# float("1,000") # ValueError
```

兩個參數都是字串，而 `int()`、`float()` 確實能解析某些字串；問題在於字串內容不是它們接受的數字格式。

### `TypeError`：傳入的物件種類或呼叫方式不被接受

```python
# int([1, 2, 3])  # TypeError
# list(1000)      # TypeError: 'int' object is not iterable
```

整數不是可迭代物件，所以 `list(1000)` 無法逐一取得元素。若要得到各個數字字元，可以先明確轉成字串：

```python
digits = list(str(1000))
print(digits)  # ['1', '0', '0', '0']
```

處理外部輸入時，不要假設轉換一定成功。應預留失敗時的處理，讓程式給出清楚的回饋：

```python
text = "49.5"

try:
    number = float(text)
    print(number)
except ValueError:
    print("請輸入有效的數字")
```

`try` 與 `except` 之後會再完整介紹；這裡先知道它們可以處理格式不符的輸入。

---

## 七、兩個容易誤判的轉換

### `int(float_value)` 會截掉小數部分

```python
print(int(3.9))   # 3
print(int(-3.9))  # -3
```

`int()` 轉換有限浮點數時會朝零截斷，不會自動四捨五入。需要四捨五入時，可依需求使用 `round()`；它的規則和 `int()` 不同。

### 非空字串轉成 `bool` 幾乎都是 `True`

```python
print(bool("False"))  # True
print(bool("0"))      # True
print(bool(""))       # False
```

`bool()` 判斷的是物件的真值，不是解析字串中文字的意思。非空字串為 `True`，空字串才為 `False`。若要解析使用者輸入，應明確比對允許的文字：

```python
answer = "false"
is_enabled = answer.strip().lower() == "true"

print(is_enabled)  # False
```

參考：[Python 官方文件：Truth Value Testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)

---

## 八、動手練習

請在 Notebook 或 `.py` 檔案中依序「先預測、再執行、最後核對」。

### 步驟 1：比較外觀相似的值

```python
values = [1000, 1000.0, "1000"]

for value in values:
    print(value, type(value))
```

執行前，先寫下三次 `type()` 分別會顯示什麼。

### 步驟 2：觀察容器如何讀取字串

```python
text = "2026"

print(list(text))
print(tuple(text))
print([text])
```

說明前兩個結果為何有四個元素，而最後一個結果只有一個元素。

### 步驟 3：找出可以成功的轉換

先預測每一行會成功、出現 `ValueError`，還是出現 `TypeError`，再逐行執行：

```python
int("25")
int("25.0")
float("25.0")
float("2,500")
list(2500)
list(str(2500))
```

### 步驟 4：整理簡單的外部輸入

```python
raw_price = "1,280.50"
clean_price = raw_price.replace(",", "")
price = float(clean_price)

print(price)        # 1280.5
print(type(price))  # <class 'float'>
```

指出每個變數負責哪一步：保存原始資料、清理格式、轉成數值。分開保存這三個階段，比覆蓋同一個變數更容易檢查問題。

### 步驟 5：隔天再憑記憶作答

不看筆記，寫出：

- 將整數格式字串轉成 `int` 的語法。
- 將串列轉成元組的語法。
- 讓完整字串成為串列中唯一元素的語法。
- `ValueError` 和 `TypeError` 的差別。
- `bool("False")` 的結果與原因。

---

## 九、複習題

請先不看答案，直接從記憶回答。

1. `"1000"`、`1000`、`1000.0` 分別是什麼型別？
2. `type()` 的用途是什麼？
3. `float("1000")` 的結果是什麼？
4. 為什麼 `float("1,000")` 會失敗？簡單格式下可如何處理？
5. `list("1000")` 有幾個元素？內容是什麼？
6. 如何建立只包含完整字串 `"1000"` 的串列？
7. 把 `my_list` 轉成元組的寫法是什麼？原本的串列會變成元組嗎？
8. `int(3.9)` 的結果是什麼？它是否使用四捨五入？
9. `bool("False")` 為什麼是 `True`？
10. 轉成集合可能失去哪些資訊？
11. `int("hello")` 和 `list(1000)` 分別常見哪一類例外？

<details>
<summary>參考答案</summary>

1. 依序是 `str`、`int`、`float`。
2. 取得物件目前的型別。
3. 浮點數 `1000.0`。
4. `float()` 預設不接受千分位逗號。來源格式確定時，可以先用 `replace(",", "")` 移除逗號再轉換。
5. 4 個，內容是 `["1", "0", "0", "0"]`。
6. `["1000"]`。
7. `my_tuple = tuple(my_list)`；不會，`my_list` 仍是串列，轉換結果由 `my_tuple` 參照。
8. `3`；不是四捨五入，而是朝零截斷。
9. 因為它是非空字串；`bool()` 判斷真值，不解析字串所寫的布林意義。
10. 重複值會被移除，也不應依賴元素順序。
11. `int("hello")` 是 `ValueError`；`list(1000)` 是 `TypeError`。

</details>

---

## 本節教材補充

| 教材說法 | 修正或補充 |
| --- | --- |
| 型別名稱加上小括號就能轉換 | 這是常見形式，但資料仍須符合目標型別接受的格式，並非任意型別都能互轉 |
| 字串 `"1,000"` 能用 `float()` 轉換 | 若真的含有逗號，直接轉換會拋出 `ValueError`；能直接轉換的是 `"1000"` |
| `"1,000"` 轉成串列會有 4 個元素 | `list()` 逐字拆分；`"1000"` 有 4 個字元，`"1,000"` 則有 5 個字元 |
| 把字串丟到 `list()` 就得到 `list` 型別 | 正確，但結果是每個字元各成為一個元素；若要保存完整字串，應寫 `[my_string]` |
| 用 `tuple(my_list)` 把串列變成元組 | 會建立轉換結果，但不會把原本的 `my_list` 原地改成元組，應將結果指派給另一個變數 |
| `int()` 可把浮點數變整數 | 可以，但會朝零截掉小數部分，可能造成資訊損失 |

## 延伸閱讀

- [Python 官方文件：Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python 官方文件：Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Python 官方教學：Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
