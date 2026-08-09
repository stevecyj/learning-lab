# 6-3 Python 元組：索引、串接與不可變性

## 學習目標

完成這一節後，我應該能夠：

1. 建立空元組、單元素元組與多元素元組。
2. 使用正索引、負索引與 `len()` 讀取元組資料。
3. 使用 `+` 串接兩個元組，並說明結果是新的元組。
4. 比較元組與串列在可變性和用途上的差異。
5. 看懂修改元組元素時出現的 `TypeError`。
6. 說明元組的不可變性是「淺層不可變」。

---

## 一、元組是有順序且不可變的序列

元組（tuple）是 Python 的序列型別。它會依照放入的順序保存元素，也允許：

- 重複的元素。
- 不同型別的元素。
- 使用索引、切片與 `len()` 等常見序列操作。

```python
data = ("hello", "hi", 33, 44, "55")

print(type(data))  # <class 'tuple'>
print(data)        # ('hello', 'hi', 33, 44, '55')
```

「不可變」（immutable）表示元組建立後，不能替換、加入或刪除其中的元素。它適合表示結構固定、不希望被意外修改的一組資料，例如座標、RGB 色彩或函式回傳的多個結果。

```python
point = (120, 35)
rgb = (255, 128, 0)
```

元組和串列都是序列，但不能說兩者「一模一樣，只差不可變」。兩者也有不同的語法、方法與慣用情境：串列常用來保存會增刪或更新的一批項目；元組常用來表達欄位數量和位置固定的一筆資料。

參考：[Python 官方文件：Tuples](https://docs.python.org/3/library/stdtypes.html#tuples)

---

## 二、建立元組時，真正關鍵的是逗號

多元素元組通常寫在小括號內，元素之間用逗號分隔：

```python
numbers = (1, 2, 3)
mixed = ("hello", 33, True)
empty = ()
```

元組實際上由逗號形成，小括號主要讓結構更容易辨認。下列兩行都會建立元組：

```python
with_parentheses = (1, 2, 3)
without_parentheses = 1, 2, 3

print(type(with_parentheses))     # <class 'tuple'>
print(type(without_parentheses))  # <class 'tuple'>
```

初學時建議保留小括號，意圖比較清楚。

### 單元素元組一定要有逗號

只有一個元素時，元素後面的逗號不能省略：

```python
not_a_tuple = (1)
one_item = (1,)

print(type(not_a_tuple))  # <class 'int'>
print(type(one_item))     # <class 'tuple'>
```

`(1)` 只是把整數 `1` 放在分組括號中；`(1,)` 才是單元素元組。

也可以用 `tuple()` 把可迭代物件轉成元組：

```python
letters = tuple("abc")
numbers = tuple([1, 2, 3])

print(letters)  # ('a', 'b', 'c')
print(numbers)  # (1, 2, 3)
```

參考：[Python 官方教學：Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)

---

## 三、正索引從前面數，負索引從後面數

元組和字串、串列一樣，索引從 `0` 開始；`-1` 代表最後一個元素：

```python
values = ("hello", "hi", 33, 44, "55")

print(values[0])   # hello
print(values[1])   # hi
print(values[-1])  # 55
print(values[-2])  # 44
print(len(values)) # 5
```

索引對照如下：

| 元素 | `"hello"` | `"hi"` | `33` | `44` | `"55"` |
| --- | ---: | ---: | ---: | ---: | ---: |
| 正索引 | `0` | `1` | `2` | `3` | `4` |
| 負索引 | `-5` | `-4` | `-3` | `-2` | `-1` |

若單一索引超出範圍，會出現 `IndexError`：

```python
# print(values[5])  # IndexError: tuple index out of range
```

元組也支援切片。切片會回傳一個新的元組：

```python
print(values[1:4])  # ('hi', 33, 44)
print(values[::-1]) # ('55', 44, 33, 'hi', 'hello')
```

參考：[Python 官方文件：Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

---

## 四、`+` 會建立串接後的新元組

兩個元組可以用 `+` 串接：

```python
tuple1 = (1, 2)
tuple2 = (3, 4)
tuple3 = tuple1 + tuple2

print(tuple3)  # (1, 2, 3, 4)
print(tuple1)  # (1, 2)
print(tuple2)  # (3, 4)
```

因為元組不可變，這項操作不會擴充 `tuple1` 或 `tuple2`，而是建立新的元組並讓 `tuple3` 指向它。

左右兩側都必須是元組。即使只有一個新元素，也要寫成單元素元組：

```python
numbers = (1, 2)
extended = numbers + (3,)

print(extended)  # (1, 2, 3)

# numbers + 3    # TypeError
# numbers + (3)  # TypeError，因為 (3) 是 int
```

若資料需要頻繁新增、刪除或替換，應先使用串列處理，最後有需要時再用 `tuple()` 轉換。反覆用 `+` 加長元組會一直建立新物件，不適合累積大量資料。

---

## 五、串列能修改元素，元組不能

比較內容相同的串列與元組：

```python
my_list = [1, 2, 3]
my_tuple = (1, 2, 3)

my_list[1] = 100
print(my_list)  # [1, 100, 3]
```

串列是可變物件，因此可以把索引 `1` 的第二個元素改為 `100`。對元組做相同操作則會失敗：

```python
my_tuple[1] = 100
```

Python 會拋出：

```text
TypeError: 'tuple' object does not support item assignment
```

這裡的 item assignment 是「對其中一個元素指定新值」。錯誤訊息表示元組不支援這項操作。

如果真的需要改變內容，可以依需求採用以下做法：

```python
old_values = (1, 2, 3)

# 建立一個新的元組
new_values = old_values[:1] + (100,) + old_values[2:]
print(new_values)  # (1, 100, 3)

# 或暫時轉成串列修改，再轉回元組
editable = list(old_values)
editable[1] = 100
new_values = tuple(editable)
```

這兩種方法都沒有修改原本的元組，而是建立新的物件。若程式經常需要這樣轉換，通常代表資料本來就更適合使用串列。

---

## 六、不可變不代表內部所有物件都不能變

元組不能更換自己所保存的物件參照，但其中的物件本身可能是可變的。例如元組可以包含串列：

```python
record = ("Isaac", [80, 90])

record[1].append(100)
print(record)  # ('Isaac', [80, 90, 100])
```

這段程式沒有把 `record[1]` 換成另一個物件，而是修改該位置所指向的串列。因此它不違反元組本身不可變的規則。

但下面仍然不允許：

```python
# record[1] = [80, 90, 100]  # TypeError
```

這種特性可稱為「淺層不可變」：元組的長度與每個位置保存的參照固定，卻不保證內部物件也不可變。

這也影響元組能否當作字典鍵或放進集合。只有當元組內的每個元素都可雜湊（hashable）時，整個元組才可雜湊：

```python
locations = {(25.03, 121.56): "Taipei"}  # 可以

# hash(("Isaac", [80, 90]))  # TypeError：內含不可雜湊的 list
```

參考：[Python 官方文件：Immutable Sequence Types](https://docs.python.org/3/library/stdtypes.html#immutable-sequence-types)

---

## 七、固定欄位資料常用打包與拆包

元組經常用來把多個相關值打包在一起：

```python
student = ("Ada", 95)
```

知道每個位置的意義時，可以用拆包（unpacking）一次取出：

```python
name, score = student

print(name)   # Ada
print(score)  # 95
```

這通常比反覆寫 `student[0]`、`student[1]` 更容易閱讀。左右兩側的數量必須相符，否則會出現 `ValueError`。

```python
# name, score, rank = student  # ValueError
```

欄位一多，純索引會難以理解。例如 `student[3]` 無法直接說明該值代表什麼。這時可改用字典、`namedtuple` 或資料類別（dataclass）；目前先知道「固定且少量的位置資料」是元組的常見用途即可。

---

## 八、動手練習

在 Notebook 或 `.py` 檔案中完成預測—執行—核對。

### 步驟 1：先預測型別和輸出

先不要執行，寫下每一行的結果：

```python
a = (7)
b = (7,)
c = ("hello", 33, "hello")

print(type(a))
print(type(b))
print(c[0])
print(c[-1])
print(len(c))
print(c[1:])
```

執行後，特別核對 `a` 與 `b` 的型別為什麼不同。

### 步驟 2：比較可變與不可變

```python
my_list = [1, 2, 3]
my_tuple = (1, 2, 3)

my_list[1] = 100
print(my_list)

try:
    my_tuple[1] = 100
except TypeError as error:
    print(type(error).__name__)
    print(error)
```

先預測最後兩行會顯示什麼，再執行核對。`try` 與 `except` 的細節之後再學，這裡只用它保留錯誤訊息，避免程式在中途停止。

### 步驟 3：用元組表示固定資料

```python
point_a = (10, 20)
point_b = (3, 4)

x1, y1 = point_a
x2, y2 = point_b
delta = (x1 - x2, y1 - y2)

print(delta)
```

先算出 `delta`，再執行核對。接著嘗試用索引改寫一次，觀察拆包和索引哪一種比較容易讀懂。

### 步驟 4：隔一天再做記憶提取

不看筆記寫出：

- 空元組。
- 只有整數 `5` 的單元素元組。
- 取得元組最後一個元素的語法。
- 串接 `(1, 2)` 與單元素 `3` 的語法。
- 元組無法用索引修改時的例外類型。

---

## 九、文末示範解答

逐字稿最後比較串列和元組的元素指定：

```python
my_list = [1, 2, 3]
my_tuple = (1, 2, 3)

my_list[1] = 100
print(my_list)  # [1, 100, 3]

my_tuple[1] = 100
```

最後一行不會產生修改後的元組，而是拋出：

```text
TypeError: 'tuple' object does not support item assignment
```

字幕前段的其他操作可整理為：

```python
a = (1, 2, 3)

print(a[0])   # 1
print(a[-1])  # 3
print(len(a)) # 3

tuple1 = (1, 2)
tuple2 = (3, 4)
tuple3 = tuple1 + tuple2

print(tuple3) # (1, 2, 3, 4)
```

---

## 十、複習題

請先不看答案，直接從記憶回答。

1. 元組是否有順序？能否有重複元素？
2. 建立單元素元組 `(5,)` 時，哪個符號不能省略？
3. `(5)` 與 `(5,)` 的型別分別是什麼？
4. `("a", "b", "c")[-1]` 的結果是什麼？
5. `(1, 2) + (3,)` 的結果是什麼？
6. 為什麼 `(1, 2) + 3` 會出錯？
7. 執行 `my_tuple[1] = 100` 會出現哪一種例外？
8. 元組包含串列時，可以呼叫該串列的 `append()` 嗎？為什麼？
9. 所有元組都能當字典鍵嗎？
10. 哪一種資料較適合用元組：會持續新增的待辦清單，還是固定的二維座標？

<details>
<summary>參考答案</summary>

1. 有順序，也能包含重複元素。
2. 逗號；真正形成單元素元組的是逗號。
3. `(5)` 是 `int`；`(5,)` 是 `tuple`。
4. `"c"`。
5. `(1, 2, 3)`。
6. `+` 串接元組時，左右兩側都必須是元組；`3` 是 `int`。
7. `TypeError`，訊息會指出 tuple 不支援 item assignment。
8. 可以。元組保存的物件參照沒有被替換，只是內部的可變串列被修改；這是淺層不可變。
9. 不一定。元組內所有元素都可雜湊時才可以；含有串列等不可雜湊物件時不行。
10. 固定的二維座標適合元組；會持續變動的待辦清單適合串列。

</details>

---

## 本節教材補充

| 教材說法 | 修正或補充 |
| --- | --- |
| 「弧角括號」 | 一般稱為「小括號」或「圓括號」 |
| tuple 跟 list 基本上一模一樣 | 兩者都是序列，也都支援索引等操作；但語法、方法、可變性與慣用情境不同 |
| 唯一差別是 tuple 不可變 | 這是最主要差異之一，不是唯一差異；元組也沒有 `append()`、`remove()` 等原地修改方法 |
| 用小括號建立 tuple | 多元素元組常用小括號書寫，但真正形成元組的是逗號；單元素元組必須寫成 `(value,)` |
| tuple 裡面的元素不能改變 | 更精確地說，不能替換元組各位置所指向的物件；若元素本身是串列等可變物件，其內部仍可改變 |
| 兩個 tuple 用 `+` 連在一起 | 結果是新元組，原本的兩個元組不會被修改 |
| 「更換元素時出現 error」 | 具體例外是 `TypeError`：`'tuple' object does not support item assignment` |

## 延伸閱讀

- [Python 官方文件：Tuples](https://docs.python.org/3/library/stdtypes.html#tuples)
- [Python 官方文件：Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)
- [Python 官方文件：Immutable Sequence Types](https://docs.python.org/3/library/stdtypes.html#immutable-sequence-types)
- [Python 官方教學：Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)

遇到元組相關錯誤時，先用 `type()` 確認物件型別，再用 `repr()` 檢查逗號是否存在。若程式需要頻繁更動內容，回頭判斷串列是否更適合這份資料。
