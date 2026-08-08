# 6-2 Python 串列：索引、切片與常用方法

## 學習目標

完成這一節後，我應該能夠：

1. 使用 `[]` 或 `list()` 建立串列。
2. 說明串列具有順序、可變，也允許重複值與不同型別的元素。
3. 用正索引、負索引與 `[start:stop:step]` 讀取串列內容。
4. 分辨 `append()` 與 `extend()` 的用途。
5. 使用 `insert()`、`remove()`、`pop()` 和 `clear()` 修改串列。
6. 使用 `reverse()` 與 `sort()` 原地重新排列元素。
7. 分辨內建函式、串列方法，以及原地修改與回傳新值。

---

## 一、串列是有順序且可變的元素集合

Python 的串列型別是 `list`，以方括號 `[]` 建立，各元素之間用逗號分隔：

```python
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

print(type(weekdays))  # <class 'list'>
```

串列有四個重要特性：

- **有順序**：每個元素都有固定位置，可以用索引取得。
- **可變**（mutable）：建立後仍能新增、刪除、替換或重新排列元素。
- **允許重複**：相同的值可以出現多次，不會自動合併。
- **可混合型別**：同一個串列可以放入不同型別的物件。

```python
values = [10, "Python", True, 3.14, 10]

values[0] = 99
print(values)  # [99, 'Python', True, 3.14, 10]
```

雖然 Python 允許混合型別，但實務上，同一串列通常存放用途相近的資料，程式會更容易理解與處理。

> 教材稱「序列化型別」，正確名稱是「序列型別」（sequence type）。序列化是把資料轉成便於儲存或傳輸的格式，與此處的資料型別分類不同。臺灣通常把 `list` 譯為「串列」，也有人稱「列表」。

參考：[Python 官方文件：Lists](https://docs.python.org/3/library/stdtypes.html#lists)

---

## 二、建立串列與空串列

最常見的建立方式是串列字面值：

```python
numbers = [1, 2, 3]
empty_list = []
```

也可以呼叫 `list()`：

```python
empty_list = list()
letters = list("abc")

print(empty_list)  # []
print(letters)     # ['a', 'b', 'c']
```

`list()` 可以把可迭代物件中的元素依序收集成新串列。沒有傳入資料時，就建立空串列。

兩個串列可以使用 `+` 串接，但結果是新的串列：

```python
a = [1, 2]
b = [3, 4]
c = a + b

print(c)  # [1, 2, 3, 4]
print(a)  # [1, 2]
print(b)  # [3, 4]
```

---

## 三、用索引取得單一元素

串列和字串一樣，索引從 `0` 開始：

```python
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

print(weekdays[0])  # Monday
print(weekdays[1])  # Tuesday
print(weekdays[2])  # Wednesday
```

負索引從尾端開始，`-1` 代表最後一個元素：

```python
print(weekdays[-1])  # Friday
print(weekdays[-2])  # Thursday
```

| 元素 | `Monday` | `Tuesday` | `Wednesday` | `Thursday` | `Friday` |
| --- | ---: | ---: | ---: | ---: | ---: |
| 正索引 | `0` | `1` | `2` | `3` | `4` |
| 負索引 | `-5` | `-4` | `-3` | `-2` | `-1` |

單一索引超出範圍會拋出 `IndexError`：

```python
# print(weekdays[5])  # IndexError: list index out of range
```

因為串列可變，所以索引也能出現在指定運算的左側：

```python
weekdays[0] = "星期一"
print(weekdays[0])  # 星期一
```

---

## 四、切片一次取得多個元素

切片的完整語法是：

```python
sequence[start:stop:step]
```

- `start`：開始位置，包含這個索引。
- `stop`：停止位置，不包含這個索引。
- `step`：每次移動幾格，預設為 `1`。

```python
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

print(weekdays[2:4])
# ['Wednesday', 'Thursday']

print(weekdays[1:])
# ['Tuesday', 'Wednesday', 'Thursday', 'Friday']

print(weekdays[::2])
# ['Monday', 'Wednesday', 'Friday']
```

`weekdays[2:4]` 包含索引 `2`，但不包含索引 `4`。`weekdays[::2]` 省略起點和終點，代表巡覽整個串列，每次前進兩格。

切片會建立新串列，不會直接修改原串列：

```python
workdays = weekdays[0:5]

print(workdays == weekdays)  # True：內容相等
print(workdays is weekdays)  # False：不是同一個串列物件
```

參考：[Python 官方文件：Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)

---

## 五、`append()` 加入一個元素，`extend()` 加入多個元素

`append(x)` 會把 **一個物件** 放到串列尾端：

```python
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekdays.append("Saturday")

print(weekdays)
# ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
```

如果傳入的物件本身是串列，整個串列仍只算一個元素：

```python
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekend = ["Saturday", "Sunday"]

weekdays.append(weekend)
print(weekdays)
# ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
#  ['Saturday', 'Sunday']]

print(len(weekdays))  # 6
print(weekdays[-1])   # ['Saturday', 'Sunday']
```

此時形成的是巢狀串列：最後一個元素本身也是串列。

若希望把 `weekend` 中的兩個元素分別加入，應使用 `extend()`：

```python
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
weekend = ["Saturday", "Sunday"]

weekdays.extend(weekend)
print(weekdays)
# ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
#  'Saturday', 'Sunday']

print(len(weekdays))  # 7
```

| 寫法 | 傳入資料如何處理 | 增加幾個元素 |
| --- | --- | ---: |
| `items.append(x)` | 把 `x` 當成單一元素 | 1 個 |
| `items.extend(data)` | 逐一加入 `data` 產生的元素 | 視內容而定 |

`extend()` 接受的是可迭代物件，不限於串列：

```python
letters = ["A"]
letters.extend("BC")

print(letters)  # ['A', 'B', 'C']
```

這也表示字串會被逐字加入；若想把完整字串當成一個元素，應使用 `append("BC")`。

---

## 六、插入與刪除元素

### `insert(index, value)`：在指定位置前插入

```python
items = ["A", "B", "C"]
items.insert(1, "AA")

print(items)  # ['A', 'AA', 'B', 'C']
```

`insert(1, "AA")` 是在原本索引 `1` 的元素之前插入 `"AA"`，不是替換原元素。

### `remove(value)`：依值刪除第一個符合項目

```python
days = ["Monday", "Tuesday", "Monday"]
days.remove("Monday")

print(days)  # ['Tuesday', 'Monday']
```

如果有重複值，`remove()` 只移除第一個；找不到指定值時會拋出 `ValueError`。

### `pop(index)`：依位置移除並回傳元素

省略索引時，`pop()` 會移除並回傳最後一個元素：

```python
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

removed_day = weekdays.pop()
print(removed_day)  # Friday
print(weekdays)     # ['Monday', 'Tuesday', 'Wednesday', 'Thursday']

weekdays.pop()
print(weekdays)     # ['Monday', 'Tuesday', 'Wednesday']
```

也可以指定要移除的位置：

```python
numbers = [10, 20, 30]
removed_number = numbers.pop(1)

print(removed_number)  # 20
print(numbers)         # [10, 30]
```

空串列不能執行 `pop()`，否則會拋出 `IndexError`。

### `clear()`：移除全部元素

```python
numbers = [1, 2, 3]
numbers.clear()

print(numbers)  # []
```

| 方法 | 根據什麼刪除 | 是否回傳被刪元素 |
| --- | --- | --- |
| `remove(value)` | 值 | 否，回傳 `None` |
| `pop(index)` | 索引，預設最後一格 | 是 |
| `clear()` | 全部元素 | 否，回傳 `None` |

參考：[Python 官方教學：More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

---

## 七、`reverse()` 反轉，`sort()` 排序

`reverse()` 會把目前順序原地反轉：

```python
numbers = [1, 100, -2, 8, 9, -10]
numbers.reverse()

print(numbers)  # [-10, 9, 8, -2, 100, 1]
```

它只是把順序前後顛倒，不是依數值大小排序。

`sort()` 預設會把元素由小到大原地排序：

```python
numbers.sort()

print(numbers)  # [-10, -2, 1, 8, 9, 100]
```

反向排序可以設定 `reverse=True`：

```python
numbers.sort(reverse=True)
print(numbers)  # [100, 9, 8, 1, -2, -10]
```

`sort()` 要求元素之間可以互相比較。像數字和字串混在一起時，通常不能直接排序：

```python
mixed = [1, "2", 3]
# mixed.sort()  # TypeError
```

### 原地排序與建立新串列

`list.sort()` 修改原串列並回傳 `None`；內建函式 `sorted()` 則回傳排好序的新串列：

```python
numbers = [3, 1, 2]

result = numbers.sort()
print(numbers)  # [1, 2, 3]
print(result)   # None

numbers = [3, 1, 2]
new_numbers = sorted(numbers)
print(numbers)      # [3, 1, 2]
print(new_numbers)  # [1, 2, 3]
```

不要寫成 `numbers = numbers.sort()`，否則 `numbers` 最後會變成 `None`。

---

## 八、內建函式與串列方法的差別

教材把 `append()`、`remove()` 等統稱為「Python 內建函數」，這不夠精確：

- `len(items)`、`list()`、`sorted(items)` 是 Python 內建函式。
- `items.append(x)`、`items.pop()`、`items.sort()` 是 `list` 物件的方法。

常見操作可整理如下：

| 寫法 | 用途 | 是否修改原串列 | 回傳值 |
| --- | --- | --- | --- |
| `len(items)` | 計算元素數量 | 否 | `int` |
| `items.append(x)` | 尾端加入一個元素 | 是 | `None` |
| `items.extend(data)` | 尾端加入多個元素 | 是 | `None` |
| `items.insert(i, x)` | 在索引 `i` 前插入 | 是 | `None` |
| `items.remove(x)` | 移除第一個等於 `x` 的元素 | 是 | `None` |
| `items.pop(i)` | 移除並回傳索引 `i` 的元素 | 是 | 被移除的元素 |
| `items.clear()` | 清空全部元素 | 是 | `None` |
| `items.reverse()` | 原地反轉順序 | 是 | `None` |
| `items.sort()` | 原地排序 | 是 | `None` |
| `sorted(items)` | 建立排好序的新串列 | 否 | 新 `list` |

修改串列但沒有特定結果需要回傳的方法，通常回傳 `None`。這項設計能提醒開發者：操作已經直接改變原物件。

---

## 九、Python 開發者會留意的串列特性

1. **變數保存的是串列參照。** 單純指定不會複製串列，兩個名稱可能指向同一物件：

   ```python
   a = [1, 2]
   b = a
   b.append(3)

   print(a)  # [1, 2, 3]
   ```

   若只需淺層複製，可使用 `b = a.copy()` 或 `b = a[:]`。

2. **`append()` 不會展開容器。** 傳入串列時會形成巢狀結構；這有時正是需要的資料形狀，並不一定是錯誤。

3. **避免覆蓋內建名稱。** 不要把變數命名為 `list`、`len` 或 `sorted`，否則稍後可能無法正常呼叫同名內建工具。

4. **不要一邊巡覽一邊任意刪除原串列。** 索引移動後可能漏掉元素。篩選資料時通常建立新串列會更清楚。

5. **重複串列包含可變物件時要小心共享參照。** 例如 `rows = [[]] * 3` 的三個位置指向同一個內層串列；較安全的寫法是 `rows = [[] for _ in range(3)]`。

---

## 十、動手練習

### 步驟 1：先預測，再執行

```python
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
weekend = ["Sat", "Sun"]

print(days[1:4])
print(days[::2])

days.append(weekend)
print(len(days))
print(days[-1])
```

先寫下四行結果，再到 Notebook 執行核對。特別留意最後一個元素的型別。

### 步驟 2：修正資料形狀

重新建立 `days`，改用 `extend()` 加入週末，再依序完成：

1. 在索引 `1` 前插入 `"Holiday"`。
2. 使用 `remove()` 移除 `"Holiday"`。
3. 使用 `pop()` 移除最後一個元素，並將它保存成 `removed_day`。
4. 印出 `removed_day` 和最後的 `days`。

### 步驟 3：隔一天做記憶提取

不看筆記寫出：

- 取得最後一個元素的方法。
- 取得索引 `2` 到 `4`、但不包含 `4` 的切片。
- 一次跳兩格的完整串列切片。
- 將另一串列的元素逐一加入的方法。
- 移除並取得最後一個元素的方法。
- 不改變原串列而取得排序結果的方法。

---

## 十一、文末示範解答

逐字稿結尾沒有獨立題目，最後一段是常見串列操作的示範。以下是一段可以直接執行、逐步觀察狀態的版本：

```python
b = [1, 3, -2, 8, 9, -10]

b.append(20)
print(b)  # [1, 3, -2, 8, 9, -10, 20]

b.remove(3)
print(b)  # [1, -2, 8, 9, -10, 20]

removed = b.pop()
print(removed)  # 20
print(b)        # [1, -2, 8, 9, -10]

b.insert(1, 100)
print(b)  # [1, 100, -2, 8, 9, -10]

b.reverse()
print(b)  # [-10, 9, 8, -2, 100, 1]

b.sort()
print(b)  # [-10, -2, 1, 8, 9, 100]
```

---

## 十二、複習題

請先不看答案，直接從記憶回答。

1. Python 的 `list` 為什麼稱為可變型別？
2. 串列是否允許重複值與不同型別的元素？
3. `weekdays[2:4]` 會包含索引 `4` 嗎？
4. `weekdays[::2]` 的最後一個 `2` 表示什麼？
5. `append(["Sat", "Sun"])` 會增加幾個最外層元素？
6. `extend(["Sat", "Sun"])` 會增加幾個元素？
7. `remove()` 與 `pop()` 分別依照值還是索引刪除？
8. 無參數的 `pop()` 除了修改串列，還會回傳什麼？
9. `reverse()` 和 `sort()` 的用途有何不同？
10. 為什麼不應寫 `numbers = numbers.sort()`？

<details>
<summary>參考答案</summary>

1. 因為串列建立後，仍可原地新增、刪除、替換或重新排列元素。
2. 兩者都允許。
3. 不會；切片包含 `start`，不包含 `stop`。
4. `step` 是 `2`，所以每次前進兩個索引位置。
5. 一個；傳入的串列本身成為一個巢狀元素。
6. 兩個；`"Sat"` 和 `"Sun"` 會分別加入。
7. `remove()` 依值；`pop()` 依索引，省略索引時刪除最後一個。
8. 回傳被移除的最後一個元素。
9. `reverse()` 顛倒目前順序；`sort()` 依元素的比較結果排序。
10. 因為 `sort()` 原地修改串列並回傳 `None`，指定後 `numbers` 會變成 `None`。

</details>

---

## 本節教材補充

| 教材說法 | 修正或補充 |
| --- | --- |
| 序列化型別 | 應稱「序列型別」；序列化是另一個概念 |
| 列表 | 臺灣常稱「串列」，英文型別名稱為 `list` |
| 用直角括號建立 | 一般稱「方括號」`[]`；也可使用 `list()` |
| `append(weekend)` 不是我們想要的 | 它會建立巢狀串列；是否正確取決於需要的資料形狀 |
| `pop()` 把元素丟掉 | `pop()` 不只移除，還會回傳被移除的元素 |
| `remove()` 把指定元素去掉 | 若有重複值，只移除第一個；找不到會拋出 `ValueError` |
| `insert(1, "AA")` 在 index 1 加入 | 更精確地說，是在原索引 `1` 的元素之前插入 |
| `reverse()` 是反過來念 | 它會原地顛倒串列目前的元素順序 |
| `sort()` 是由小排到大 | 這是預設行為；元素必須可比較，也可設定 `reverse=True` |
| 這些是內建函數 | `append()` 等是串列方法；`len()`、`list()`、`sorted()` 才是內建函式 |

## 延伸閱讀

- [Python 官方教學：Lists](https://docs.python.org/3/tutorial/introduction.html#lists)
- [Python 官方教學：More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Python 官方文件：Sequence Types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
- [Python 官方文件：Mutable Sequence Types](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types)

遇到預測與實際結果不同時，先用 `print()`、`type()` 和 `len()` 檢查串列本身與各元素，再判斷操作改變的是資料內容、元素位置，還是最外層的資料形狀。
