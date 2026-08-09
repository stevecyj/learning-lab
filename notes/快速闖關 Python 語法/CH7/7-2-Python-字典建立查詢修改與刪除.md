# 7-2 Python 字典：建立、查詢、修改與刪除

## 學習目標

完成這一節後，我應該能夠：

1. 用 `{key: value}` 建立字典，並說明鍵和值各自的用途。
2. 使用 `len()` 計算字典中的鍵值對數量。
3. 用 `dictionary[key]` 查詢、加入與修改資料。
4. 使用 `keys()`、`values()` 與 `items()` 取得不同的字典檢視。
5. 使用 `pop()` 刪除指定鍵值對，並保存被刪除的值。
6. 分辨 `dictionary[key]` 與 `get()` 在鍵不存在時的差異。

---

## 一、字典用「鍵」找到對應的「值」

字典（dictionary，型別名稱是 `dict`）是一種映射（mapping）：每個**鍵**（key）對應一個**值**（value）。鍵和值合起來稱為一組**鍵值對**（key-value pair）。

```python
scores = {
    "Isaac": 100,
    "Judy": 60,
    "Andy": 80,
}
```

這個字典有三組鍵值對：

| 鍵 key | 值 value |
| --- | ---: |
| `"Isaac"` | `100` |
| `"Judy"` | `60` |
| `"Andy"` | `80` |

可以把它想成「姓名 → 成績」的查詢表。程式用姓名這個鍵找到對應的成績；串列則使用位置索引。

```python
print(scores["Isaac"])  # 100
```

值不一定是數字，也可以是字串、串列、另一個字典或其他物件。把 value 一律稱作「數值」容易讓人誤解，稱為「值」較精確。

```python
student = {
    "name": "Isaac",
    "score": 100,
    "passed": True,
    "courses": ["Python", "Git"],
}
```

參考：[Python 官方文件：Mapping Types — `dict`](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)

---

## 二、用大括號建立字典

字典字面值使用大括號 `{}`，每組資料寫成 `key: value`，多組資料用逗號分隔：

```python
scores = {"Isaac": 100, "Judy": 60, "Andy": 80}
empty_scores = {}

print(type(scores))       # <class 'dict'>
print(type(empty_scores)) # <class 'dict'>
```

資料較多時，分成多行通常更容易閱讀與修改：

```python
scores = {
    "Isaac": 100,
    "Judy": 60,
    "Andy": 80,
}
```

`len()` 回傳鍵值對的數量，而不是把鍵和值分開計算：

```python
print(len(scores))  # 3
```

### 每個鍵都必須唯一

同一個字典不能同時保存兩個相等的鍵。字典字面值中若重複寫同一個鍵，後面的值會覆蓋前面的值：

```python
scores = {
    "Amy": 10,
    "Amy": 20,
}

print(scores)       # {'Amy': 20}
print(len(scores))  # 1
```

學生姓名只有在確定不會重複時才適合當鍵；實際的系統通常會使用學號等唯一識別資料。

---

## 三、用鍵查詢值，鍵不存在時要留意 `KeyError`

在中括號中放入鍵，就能取得對應的值：

```python
scores = {
    "Isaac": 100,
    "Judy": 60,
    "Andy": 80,
}

print(scores["Isaac"])  # 100
print(scores["Judy"])   # 60
```

字典不是用位置查詢。`scores[0]` 的意思是尋找鍵 `0`，不是取得第一組資料。

如果中括號中的鍵不存在，會出現 `KeyError`：

```python
# print(scores["Amy"])  # KeyError: 'Amy'
```

不確定鍵是否存在時，可以先用 `in` 檢查：

```python
if "Amy" in scores:
    print(scores["Amy"])
else:
    print("尚未登記 Amy 的成績")
```

也可以使用 `get()`。找不到鍵時，`get()` 預設回傳 `None`，或回傳指定的預設值，不會拋出 `KeyError`：

```python
print(scores.get("Amy"))       # None
print(scores.get("Amy", 0))    # 0
```

選擇方式：

- 資料照理一定存在，缺少時應視為錯誤：使用 `scores[key]`。
- 缺少資料是合理情況：使用 `scores.get(key, default)` 或先用 `in` 檢查。

---

## 四、相同的指定語法可以新增或修改資料

把一個不存在的鍵放在中括號左側，會新增一組鍵值對：

```python
scores = {
    "Isaac": 100,
    "Judy": 60,
    "Andy": 80,
}

scores["Amy"] = 10

print(scores)
# {'Isaac': 100, 'Judy': 60, 'Andy': 80, 'Amy': 10}
```

如果鍵已經存在，指定新值會更新原本的值：

```python
scores["Amy"] = 20
print(scores["Amy"])  # 20
```

要在原本的數字上增加 `10`，可以使用擴增指定：

```python
scores["Amy"] += 10
print(scores["Amy"])  # 30
```

這行程式可以展開成：

```python
scores["Amy"] = scores["Amy"] + 10
```

兩種寫法都要求 `"Amy"` 已經存在，否則讀取舊值時會出現 `KeyError`。

---

## 五、`keys()`、`values()` 與 `items()` 取得不同部分

字典提供三個常用方法：

```python
scores = {
    "Isaac": 100,
    "Judy": 60,
    "Andy": 80,
    "Amy": 20,
}

print(scores.keys())
# dict_keys(['Isaac', 'Judy', 'Andy', 'Amy'])

print(scores.values())
# dict_values([100, 60, 80, 20])

print(scores.items())
# dict_items([('Isaac', 100), ('Judy', 60), ('Andy', 80), ('Amy', 20)])
```

| 方法 | 取得內容 | 常見用途 |
| --- | --- | --- |
| `keys()` | 所有鍵 | 檢查或走訪姓名 |
| `values()` | 所有值 | 計算成績總和、最高分 |
| `items()` | 所有 `(鍵, 值)` | 同時處理姓名與成績 |

它們回傳的是動態的檢視物件（view objects），不是一般串列。若確實需要串列，可以明確轉換：

```python
names = list(scores.keys())
points = list(scores.values())

print(names)   # ['Isaac', 'Judy', 'Andy', 'Amy']
print(points)  # [100, 60, 80, 20]
```

使用迴圈時，可以透過 `items()` 同時走訪鍵和值：

```python
for name, score in scores.items():
    print(name, score)
```

---

## 六、用 `pop()` 刪除並取得指定鍵的值

`pop(key)` 會刪除指定鍵值對，並回傳被刪除的值：

```python
scores = {
    "Isaac": 100,
    "Judy": 60,
    "Andy": 80,
    "Amy": 20,
}

removed_score = scores.pop("Judy")

print(removed_score)  # 60
print(scores)
# {'Isaac': 100, 'Andy': 80, 'Amy': 20}
```

若鍵不存在，`pop(key)` 也會出現 `KeyError`。可以傳入第二個引數作為預設回傳值：

```python
removed_score = scores.pop("Merry", None)
print(removed_score)  # None
```

若只要刪除，不需要使用回傳值，也可以用 `del`：

```python
del scores["Andy"]
```

---

## 七、字典的其他特性

### 字典可變

建立字典後，可以加入、修改及刪除鍵值對。這和串列相似，與不可變的字串、元組不同。

### 鍵必須可雜湊

常見的字串、整數與內容皆可雜湊的元組都能當鍵；串列、字典與集合不能直接當鍵：

```python
valid = {
    "name": "Amy",
    101: "student id",
    (25.03, 121.56): "Taipei",
}

# invalid = {["Amy"]: 100}  # TypeError: unhashable type: 'list'
```

初學時，使用字串或整數作為鍵即可。

### 字典依插入順序走訪，但用途仍是映射

現代 Python 的字典會保留鍵加入時的順序。不過，字典主要用來「透過鍵找到值」；若要依位置處理資料，串列通常更合適。

參考：[Python 官方教學：Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

---

## 八、動手練習

在 Notebook 或 `.py` 檔案中練習時，先預測結果，再執行程式核對。

### 步驟 1：預測查詢與更新結果

先不要執行，寫下每一行的結果：

```python
scores = {"Isaac": 100, "Judy": 60, "Andy": 80}

print(len(scores))
print(scores["Judy"])

scores["Amy"] = 10
scores["Amy"] += 10

print(scores["Amy"])
print(len(scores))
```

### 步驟 2：比較中括號與 `get()`

```python
scores = {"Isaac": 100}

print(scores.get("Amy"))
print(scores.get("Amy", 0))

try:
    print(scores["Amy"])
except KeyError as error:
    print(type(error).__name__)
    print(error)
```

先預測四次輸出，再執行程式核對。`try` 與 `except` 的細節之後再學；這裡先用它捕捉例外，避免程式中途停止。

### 步驟 3：完成一個小型成績簿

從以下資料開始：

```python
scores = {"Isaac": 100, "Judy": 60, "Andy": 80}
```

請依序完成：

1. 新增 `Amy`，成績為 `10`。
2. 將 Amy 的成績增加 `10` 分。
3. 印出所有姓名。
4. 印出所有成績。
5. 刪除 Judy，並印出被刪除的成績。
6. 印出最後的字典與鍵值對數量。

### 步驟 4：隔天再練一次

不看筆記寫出：

- 一個含兩組鍵值對的字典。
- 讀取指定鍵的值。
- 新增或更新一組資料。
- 安全查詢可能不存在的鍵。
- 刪除指定鍵並保存其值。
- 同時取得所有鍵和值的方法。

---

## 九、文末示範解答

前面示範的成績簿操作如下：

```python
scores = {
    "Isaac": 100,
    "Judy": 60,
    "Andy": 80,
}

print(scores)
print(len(scores))          # 3
print(scores["Isaac"])    # 100

scores["Amy"] = 10        # 新增
scores["Amy"] += 10       # 更新為 20

print(scores.values())     # dict_values([100, 60, 80, 20])
print(scores.keys())       # dict_keys(['Isaac', 'Judy', 'Andy', 'Amy'])

removed_score = scores.pop("Judy")
print(removed_score)       # 60
print(scores)
# {'Isaac': 100, 'Andy': 80, 'Amy': 20}
```

步驟 3 的小型成績簿可寫成：

```python
scores = {"Isaac": 100, "Judy": 60, "Andy": 80}

scores["Amy"] = 10
scores["Amy"] += 10

print(scores.keys())
print(scores.values())

removed_score = scores.pop("Judy")
print(removed_score)

print(scores)
print(len(scores))
```

---

## 十、複習題

請先不看答案，直接從記憶回答。

1. 字典中的 key 與 value 分別扮演什麼角色？
2. `len({"Amy": 20, "Andy": 80})` 的結果是多少？
3. `scores["Amy"] = 10` 在 `"Amy"` 不存在和已存在時，各有什麼效果？
4. `scores["Amy"] += 10` 的正確完整寫法可如何展開？
5. 使用 `scores["Merry"]` 查詢不存在的鍵時，會發生什麼事？
6. `scores.get("Merry", 0)` 找不到鍵時會得到什麼？
7. `keys()`、`values()` 與 `items()` 分別取得什麼？
8. `pop("Judy")` 除了刪除資料，還會做什麼？
9. 為什麼串列不能直接當字典鍵？
10. 若同一個字典字面值重複出現 `"Amy"`，最後保留哪一個值？

<details>
<summary>參考答案</summary>

1. key 是查找資料的鍵；value 是該鍵所對應保存的值。
2. `2`，因為字典中有兩組鍵值對。
3. 鍵不存在時會新增資料；鍵已存在時會覆蓋原值。
4. `scores["Amy"] = scores["Amy"] + 10`。
5. 拋出 `KeyError`。
6. `0`，也就是傳給 `get()` 的預設值。
7. `keys()` 取得鍵，`values()` 取得值，`items()` 取得 `(鍵, 值)` 配對。
8. 回傳被刪除的值，因此可以將結果指定給變數。
9. 串列是可變且不可雜湊的物件；字典鍵必須可雜湊。
10. 後面出現的值會覆蓋前面的值。

</details>

---

## 本節教材補充

| 教材說法 | 修正或補充 |
| --- | --- |
| 字典集結一堆「鍵值以及數值」 | 更精確地說，是「鍵與值」的映射；value 不限於數字 |
| `Jason: 19` 是鍵值對 | Python 字串鍵必須加引號，完整語法應為 `"Jason": 19` |
| `a` 括號把 key 丟進去 | 正式語法是 `a[key]`；中括號裡放的是鍵，不是串列的位置索引 |
| `a` 括號 Amy 等於 10 | 若 Amy 是姓名字串，應寫成 `a["Amy"] = 10` |
| 「`a` 括號 Amy 加 10 等於 Amy」 | 字幕語序有誤；增加 10 分應寫成 `a["Amy"] += 10` |
| `values()`、`keys()` 把內容 print 出來 | 方法本身回傳檢視物件；範例是再由 `print()` 顯示它 |
| `pop()` 指定 key，該資料就不見 | `pop(key)` 也會回傳被刪除的值；鍵不存在且未給預設值時會拋出 `KeyError` |

## 延伸閱讀

- [Python 官方文件：Mapping Types — `dict`](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
- [Python 官方教學：Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Python 官方文件：Dictionary view objects](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
- [Python 官方文件：`KeyError`](https://docs.python.org/3/library/exceptions.html#KeyError)

實作時若查詢結果不如預期，先用 `print(scores)` 檢查整份字典，再用 `type(key)` 確認鍵的型別。`"101"` 和 `101` 是不同的鍵；拼字、大小寫與型別都必須吻合。
