# 9-2 Python `for` 迴圈：走訪序列資料與 `range()`

## 這堂課在講什麼

`for` 迴圈用來逐一走訪資料，例如字串、`list`、`tuple` 和 `dictionary`。每跑一圈，Python 會把目前走訪到的一個元素放進變數，再執行縮排的程式區塊。

```python
for 變數 in 序列資料:
    程式區塊
```

## 學完要會什麼

- 用 `for` 逐一取出字串、串列與元組中的元素。
- 用 `range()` 控制迴圈執行的次數、起點與間隔。
- 分辨 `range()` 的結束值不會被包含。
- 用索引取得串列元素，或用 `enumerate()` 同時取得索引和值。
- 走訪 `dictionary` 的 key 或 value。

## 重點整理

### 逐一走訪字串與串列

字串會一個字元一個字元地被取出：

```python
for c in "Python":
    print(c)
```

第一圈的 `c` 是 `P`，第二圈是 `y`，之後依序是 `t`、`h`、`o`、`n`。

串列也是同樣的用法。若 `fruits` 是一個 `list`，每一圈的 `f` 就會是其中一個元素：

```python
for f in fruits:
    print(f)
```

### `range()`：依數字範圍執行迴圈

`for` 常和 `range()` 一起使用。`range()` 可以指定迴圈執行的次數，也可以指定起點、結束值和每次前進的間隔。

```python
for i in range(10):
    print(i, end=" ")
```

`range(10)` 會產生從 `0` 到 `9` 的數字，不包含 `10`。上例的 `end=" "` 讓每次 `print()` 輸出後接一個空白，而不是預設的換行。

`range()` 的常見寫法：

| 寫法 | 走訪結果 |
| --- | --- |
| `range(10)` | `0` 到 `9` |
| `range(1, 3)` | `1`、`2` |
| `range(1, 5)` | `1`、`2`、`3`、`4` |
| `range(1, 10, 2)` | `1`、`3`、`5`、`7`、`9` |

第三個參數是每次前進的步長。以 `range(1, 10, 2)` 為例，從 `1` 開始，每次加 `2`，直到結束值 `10` 之前。

### 直接取值與用索引取值

走訪串列時，通常可以直接取得元素：

```python
my_list = [10, -20, 15]

for i in my_list:
    print(i)
```

輸出會依序是 `10`、`-20`、`15`。

若需要知道目前走訪到第幾個位置，可以用 `range(len(my_list))` 取得索引，再用索引讀取元素：

```python
my_list = [10, -20, 15]

for i in range(len(my_list)):
    print(i, my_list[i])
```

第一圈的 `i` 是 `0`，會取出 `my_list[0]`；第二圈的 `i` 是 `1`；第三圈的 `i` 是 `2`。

### `enumerate()`：同時取得索引和值

`enumerate()` 會在走訪串列時，同時提供索引和元素，因此通常用兩個變數接收：

```python
my_list = [10, -20, 15]

for index, i in enumerate(my_list):
    print(index, i)
```

第一圈的 `index` 是 `0`、`i` 是 `10`；第二圈的 `index` 是 `1`、`i` 是 `-20`。

### 走訪 `tuple`、字串與 `dictionary`

`tuple` 和字串都可以直接用 `for` 逐一走訪：

```python
for i in (10, -20, 15):
    print(i)

for i in "test123":
    print(i)
```

走訪 `dictionary` 時，預設會逐一取得 key：

```python
for i in my_dictionary:
    print(i)
```

若要取得 value，使用 `.values()`：

```python
for i in my_dictionary.values():
    print(i)
```

課堂示例中，value 會依序取出 `50`、`80`、`20`。

## 常見誤解／注意事項

- `range()` 的結束值不包含在結果內；`range(1, 3)` 只會跑到 `2`。
- `range(10)` 的起點預設是 `0`。
- `for i in my_list` 時，`i` 是元素本身；`for i in range(len(my_list))` 時，`i` 是索引。
- `print()` 預設會換行。要讓輸出接在同一行，可設定 `end=" "`。
- `for i in my_dictionary` 預設取出的是 key，不是 value。

## 一句話回顧

用 `for` 可以逐一處理序列中的元素；搭配 `range()`、索引或 `enumerate()`，就能依需要控制走訪方式。
