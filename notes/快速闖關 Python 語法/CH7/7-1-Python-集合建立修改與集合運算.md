# 7-1 Python 集合：建立、修改與集合運算

## 學習目標

完成這一節後，你會學會：

1. 說明集合（`set`）與串列、元組的主要差異。
2. 使用集合字面值與 `set()` 建立集合。
3. 使用 `add()`、`update()`、`remove()`、`discard()` 與 `pop()` 修改集合。
4. 使用 `&`、`|`、`-`、`^` 完成交集、聯集、差集與對稱差集運算。
5. 用集合去除重複值，並判斷是否需要保留原本順序。
6. 說明哪些物件可以成為集合元素，以及 `set` 和 `frozenset` 的差別。

---

## 一、集合保存不重複且可雜湊的元素

Python 的集合型別是 `set`，有三個特點：

- **元素不重複**：加入相等的值多次，集合只保留一份。
- **沒有索引**：不能使用 `items[0]` 或切片讀取元素。
- **集合本身可變**：建立後可以加入或移除元素。

```python
fruits = {"apple", "banana", "banana", "cherry"}

print(fruits == {"apple", "banana", "cherry"})  # True
print(len(fruits))                                 # 3
print("banana" in fruits)                         # True
```

即使字面值中寫了兩次 `"banana"`，集合仍只有三個元素。集合適合用來：

- 判斷某個值是否出現過。
- 去除重複值。
- 計算兩批資料的共同、合併或相異項目。

集合是**無序集合**。「無序」表示它不記錄元素的位置或插入順序；顯示或走訪集合時，不應依賴特定排列方式。

```python
# 不要假設每次都會照 apple、banana、cherry 的順序顯示
print(fruits)

# 若展示結果時需要固定順序，可另外排序
print(sorted(fruits))  # ['apple', 'banana', 'cherry']
```

集合不是序列型別，因此下列操作會失敗：

```python
# fruits[0]  # TypeError: 'set' object is not subscriptable
```

參考：[Python 官方文件：Set Types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)

---

## 二、非空集合用 `{}`，空集合要用 `set()`

非空集合可以用大括號建立：

```python
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3}

print(type(fruits))   # <class 'set'>
print(type(numbers))  # <class 'set'>
```

空集合不能寫成 `{}`，因為 `{}` 代表空字典。應使用 `set()`：

```python
empty_set = set()
empty_dict = {}

print(type(empty_set))   # <class 'set'>
print(type(empty_dict))  # <class 'dict'>
```

`set()` 也能接收可迭代物件，逐一收集其中的元素並移除重複值：

```python
letters = set("banana")
numbers = set([1, 2, 2, 3])

print(letters == {"b", "a", "n"})  # True
print(numbers == {1, 2, 3})           # True
```

`set("banana")` 會逐字處理字串，不會把整個 `"banana"` 當成一個元素。若要保存完整字串，應寫成 `{"banana"}`。

參考：[Python 官方教學：Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)

---

## 三、集合元素必須可雜湊

集合以雜湊機制管理元素，因此每個元素都必須是**可雜湊**（hashable）的物件。初學時可以先這樣判斷：內容能原地改變的物件，通常不能放進集合。

常見可作為集合元素的型別：

- 整數、浮點數、布林值。
- 字串。
- 只包含可雜湊元素的元組。
- `frozenset`。

常見不可作為集合元素的型別：

- 串列 `list`。
- 字典 `dict`。
- 一般集合 `set`。

```python
valid = {42, "Python", (25.03, 121.56)}

# invalid = {[1, 2, 3]}  # TypeError: unhashable type: 'list'
# nested = {{1, 2}}      # TypeError: unhashable type: 'set'
```

如果要在集合裡放另一個集合，內層可以使用不可變且可雜湊的 `frozenset`：

```python
groups = {frozenset({"Ada", "Grace"}), frozenset({"Linus"})}
```

`set` 可修改，所以本身不可雜湊；`frozenset` 建立後不能修改，因此可作為另一個集合的元素或字典的鍵。

---

## 四、`add()` 加一個元素，`update()` 加入多個元素

### `add(value)`：把一個物件視為一個元素

```python
fruits = {"apple", "banana", "cherry"}
fruits.add("orange")

print(fruits == {"apple", "banana", "cherry", "orange"})  # True
```

加入已存在的元素不會報錯，也不會新增第二份：

```python
fruits.add("banana")
print(len(fruits))  # 4
```

但 `add()` 的參數必須可雜湊，所以不能直接加入串列：

```python
# fruits.add(["mango", "lemon"])  # TypeError
```

### `update(iterable)`：逐一加入多個元素

`update()` 會走訪傳入的可迭代物件，將其中產生的元素逐一加入原集合：

```python
fruits = {"apple", "banana", "cherry"}
fruits.update(["orange", "mango", "banana"])

expected = {"apple", "banana", "cherry", "orange", "mango"}
print(fruits == expected)  # True
```

它不只接受串列，也能接收元組、集合、字串或多個可迭代物件：

```python
letters = {"A"}
letters.update("BC")

print(letters == {"A", "B", "C"})  # True
```

若想加入完整字串 `"BC"`，應使用 `letters.add("BC")`；`update("BC")` 會加入 `"B"` 和 `"C"`。

`add()` 和 `update()` 都直接修改原集合，呼叫成功後回傳 `None`：

```python
result = fruits.add("pear")
print(result)  # None
```

---

## 五、依值移除時，分清楚 `remove()` 與 `discard()`

### `remove(value)`：元素不存在會出錯

```python
fruits = {"apple", "banana", "cherry"}
fruits.remove("banana")

print(fruits == {"apple", "cherry"})  # True
```

若指定值不在集合中，`remove()` 會拋出 `KeyError`：

```python
# fruits.remove("orange")  # KeyError: 'orange'
```

### `discard(value)`：元素不存在也沒關係

```python
fruits.discard("orange")
print(fruits == {"apple", "cherry"})  # True
```

如果找不到元素就代表資料異常，使用 `remove()` 可以及早發現問題。如果只需要「有就刪、沒有也沒關係」，使用 `discard()` 比先檢查再刪除更直接。

```python
# 可以，但做了兩次查找
if "orange" in fruits:
    fruits.remove("orange")

# 意圖更直接
fruits.discard("orange")
```

---

## 六、`pop()` 移除並回傳任意元素

`pop()` 不接收索引或指定值。它會移除並回傳集合中的**任意元素**：

```python
fruits = {"apple", "banana", "cherry"}

removed = fruits.pop()

print(removed not in fruits)  # True
print(len(fruits))            # 2
```

這裡的「任意」不代表均勻或不可預測的「隨機」。不要用 `pop()` 實作抽獎，也不要預測它會移除哪一個元素。若集合為空，則會拋出 `KeyError`：

```python
empty = set()
# empty.pop()  # KeyError: 'pop from an empty set'
```

若需要指定移除哪個值，應使用 `remove()` 或 `discard()`；若只想清空集合，可用 `clear()`：

```python
fruits.clear()
print(fruits)  # set()
```

---

## 七、兩個集合可以計算交集、聯集、差集與對稱差集

假設兩門課的修課名單如下：

```python
python_students = {"Ada", "Grace", "Linus"}
sql_students = {"Grace", "Linus", "Guido"}
```

### 交集 `&`：兩邊都有

```python
both = python_students & sql_students
print(both == {"Grace", "Linus"})  # True
```

方法寫法是 `python_students.intersection(sql_students)`。

### 聯集 `|`：至少一邊有

```python
either = python_students | sql_students
expected = {"Ada", "Grace", "Linus", "Guido"}
print(either == expected)  # True
```

方法寫法是 `python_students.union(sql_students)`。

### 差集 `-`：左邊有、右邊沒有

```python
python_only = python_students - sql_students
sql_only = sql_students - python_students

print(python_only == {"Ada"})   # True
print(sql_only == {"Guido"})    # True
```

差集有方向性，`a - b` 和 `b - a` 通常不同。方法寫法是 `a.difference(b)`。

### 對稱差集 `^`：只出現在其中一邊

```python
one_course_only = python_students ^ sql_students
print(one_course_only == {"Ada", "Guido"})  # True
```

方法寫法是 `a.symmetric_difference(b)`。

| 問題 | 運算子 | 方法 |
| --- | :---: | --- |
| 兩邊共同有哪些？ | `a & b` | `a.intersection(b)` |
| 兩邊合起來有哪些？ | `a \| b` | `a.union(b)` |
| `a` 有而 `b` 沒有的有哪些？ | `a - b` | `a.difference(b)` |
| 只出現在其中一邊的有哪些？ | `a ^ b` | `a.symmetric_difference(b)` |

這些寫法會建立新集合，不會修改原本的 `a` 與 `b`。若需要原地更新，另有 `intersection_update()`、`update()`、`difference_update()` 與 `symmetric_difference_update()`。

### `and`、`or` 不是集合運算子

交集不能寫成 `a and b`，聯集也不能寫成 `a or b`。`and` 和 `or` 是布林運算子，會依物件的真值直接回傳其中一個運算元：

```python
a = {1, 2}
b = {2, 3}

print(a and b)  # {2, 3}，直接回傳 b，不是交集
print(a or b)   # {1, 2}，直接回傳 a，不是聯集

print(a & b)    # {2}
print(a | b)    # {1, 2, 3}
```

集合非空時真值為 `True`，空集合的真值為 `False`；因此 `and`、`or` 的結果還會隨集合是否為空而改變。集合運算請使用 `&`、`|` 或對應方法。

---

## 八、子集與無交集也是常見問題

集合除了計算新結果，也能回答集合之間的關係：

```python
backend = {"Python", "SQL"}
skills = {"Python", "SQL", "Git"}
frontend = {"HTML", "CSS"}

print(backend <= skills)                 # True：backend 是 skills 的子集
print(skills >= backend)                 # True：skills 是 backend 的超集
print(backend.isdisjoint(frontend))      # True：沒有共同元素
```

- `a <= b` 或 `a.issubset(b)`：`a` 的每個元素是否都在 `b` 中。
- `a >= b` 或 `a.issuperset(b)`：`a` 是否包含 `b` 的每個元素。
- `a.isdisjoint(b)`：兩個集合是否完全沒有共同元素。

可以用這些寫法檢查「使用者是否具備所有必要權限」或「一份資料是否包含全部必要欄位」。

---

## 九、用集合去重時，先判斷是否要保留順序

若只在意唯一值，可以先轉成集合，再視需要轉回串列：

```python
numbers = [1, 2, 2, 3, 1, 4]
unique_numbers = list(set(numbers))

print(set(unique_numbers) == {1, 2, 3, 4})  # True
```

這樣可以去除重複值，但**不保證保留原串列的出現順序**。不要假設結果一定是 `[1, 2, 3, 4]`。

若需要「保留第一次出現的順序」，可以利用字典鍵不重複且保留插入順序的特性：

```python
numbers = [3, 1, 3, 2, 1]
unique_in_order = list(dict.fromkeys(numbers))

print(unique_in_order)  # [3, 1, 2]
```

依需求選擇寫法：

| 需求 | 寫法 |
| --- | --- |
| 只在意唯一值，不在意順序 | `set(data)` |
| 要串列結果，但不在意順序 | `list(set(data))` |
| 去重且保留第一次出現順序 | `list(dict.fromkeys(data))` |

這些寫法都要求資料中的元素可雜湊。若串列元素本身也是串列或字典，就不能直接套用。

---

## 十、動手練習

在 Notebook 或 `.py` 檔案中完成「先預測、再執行、最後核對」。

### 步驟 1：建立集合並觀察去重

先不要執行，預測每一個布林運算的結果：

```python
fruits = {"apple", "banana", "banana", "cherry"}

print(len(fruits) == 3)
print("banana" in fruits)
print(fruits == {"cherry", "banana", "apple"})
```

執行後說明：為什麼第三行不需要讓兩側元素排列相同？

### 步驟 2：比較單一加入與批次加入

```python
tags = {"python"}

tags.add("data")
tags.update(["api", "python"])
tags.update("AI")

print(sorted(tags))
```

先寫下你預測的元素，再執行核對。特別解釋為什麼結果中會出現 `"A"` 與 `"I"`。

### 步驟 3：比較 `remove()` 與 `discard()`

```python
permissions = {"read", "write"}

permissions.discard("admin")
print(permissions)

try:
    permissions.remove("admin")
except KeyError as error:
    print(type(error).__name__)
```

先預測最後會顯示哪一種例外名稱，再執行核對。`try` 和 `except` 的細節之後再學，這裡只用來保留錯誤資訊，避免程式中途停止。

### 步驟 4：找出兩份資料的關係

```python
expected_columns = {"name", "email", "age"}
actual_columns = {"name", "email", "city"}

missing = expected_columns - actual_columns
unexpected = actual_columns - expected_columns
shared = expected_columns & actual_columns

print(missing)
print(unexpected)
print(shared)
```

先從變數名稱推測三個結果，再執行核對。這種集合運算常用於資料匯入與 API 驗證。

### 步驟 5：隔一天再做記憶提取

不看筆記寫出：

- 空集合的建立語法。
- 加入一個元素和加入多個元素的方法。
- 安全移除可能不存在元素的方法。
- 交集、聯集、差集、對稱差集的四個運算子。
- 能保留第一次出現順序的去重寫法。

---

## 十一、複習題

請先不看答案，直接從記憶回答。

1. 集合是否允許重複元素？是否支援索引？
2. `{}` 與 `set()` 分別建立什麼型別？
3. `{"banana"}` 與 `set("banana")` 的內容有何不同？
4. `add()` 與 `update()` 的用途有何不同？
5. `remove()` 和 `discard()` 在找不到元素時有何差異？
6. `pop()` 移除的是隨機元素嗎？空集合呼叫它會發生什麼？
7. 集合交集與聯集的運算子分別是什麼？
8. 為什麼不能用 `a and b` 計算集合交集？
9. `a - b` 與 `b - a` 一定相同嗎？
10. `list(set(data))` 去重後是否保證保留原順序？
11. 串列能否成為集合元素？為什麼？
12. 若要去重並保留第一次出現順序，可以使用什麼寫法？

<details>
<summary>參考答案</summary>

1. 不允許重複元素，也不支援索引或切片。
2. `{}` 建立空字典；`set()` 建立空集合。
3. `{"banana"}` 只有完整字串這一個元素；`set("banana")` 逐字收集，內容相當於 `{"b", "a", "n"}`。
4. `add()` 把一個可雜湊物件當成單一元素加入；`update()` 走訪一個或多個可迭代物件，逐一加入其中的元素。
5. 找不到時，`remove()` 拋出 `KeyError`；`discard()` 不會報錯。
6. 它移除並回傳任意元素，不保證隨機。空集合呼叫 `pop()` 會拋出 `KeyError`。
7. 交集是 `&`，聯集是 `|`。
8. `and` 是布林運算子，會依真值回傳其中一個運算元，不會計算共同元素。
9. 不一定。差集有方向性，代表左邊有而右邊沒有的元素。
10. 不保證。集合不記錄元素的插入位置或順序。
11. 不能，因為串列可變而且不可雜湊。
12. `list(dict.fromkeys(data))`。

</details>

---

## 本節教材補充

| 教材說法 | 修正或補充 |
| --- | --- |
| 模組介紹「雜湊類別」 | `set` 的確以雜湊機制管理元素；依 Python 官方分類，本節主題稱為集合型別（set type）較精確 |
| set 是無序且無索引的元素集合 | 正確；更精確地說，它不記錄元素位置或插入順序，因此不支援索引與切片 |
| 重複元素都會被消掉 | 相等的元素只保留一份；顯示順序也不應作為程式依據 |
| 用大括號建立 set | 只適用於非空集合；空集合必須用 `set()`，因為 `{}` 是空字典 |
| `update()` 把一個 list 的元素全部加入 | 正確，但它接受任何可迭代物件，也可以一次傳入多個可迭代物件 |
| `remove()` 移除某個元素 | 正確；元素不存在時會拋出 `KeyError`，若不希望報錯可用 `discard()` |
| `pop()` 隨機丟掉某個元素 | 應說「移除並回傳任意元素」；Python 不承諾它是隨機選取 |
| `a and b` 是交集 | 錯誤；交集使用 `a & b` 或 `a.intersection(b)` |
| `a or b` 是聯集 | 錯誤；聯集使用 `a \| b` 或 `a.union(b)` |
| `list(set(data))` 可去除重複 | 可以，但不保留原順序；要保留第一次出現順序可用 `list(dict.fromkeys(data))` |

## 延伸閱讀

- [Python 官方文件：Set Types — `set`, `frozenset`](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
- [Python 官方教學：Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)
- [Python 官方文件：Mapping Types — `dict`](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)

遇到集合結果和預期不同時，先檢查三件事：是否誤把 `{}` 當成空集合、是否誤用 `and`／`or`、是否不小心依賴了集合的顯示順序。
